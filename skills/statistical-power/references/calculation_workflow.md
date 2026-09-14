# Power calculation setup and script examples

Read the sections relevant to the requested workflow. Paths and command examples
are relative to the skill directory unless stated otherwise.

## Installation

Use **uv**. Pin versions in production; unpinned is fine for exploration.

```bash
uv pip install "statsmodels>=0.14.6" "scipy>=1.11" "pingouin>=0.6" "numpy>=1.26" matplotlib pandas
# For simulation-based power of advanced models (optional, add as needed):
uv pip install lifelines            # survival
# mixed models and GLMs come with statsmodels
```

**Compatibility note:** use `statsmodels>=0.14.6` with `scipy>=1.11` to avoid `_lazywhere` import errors on SciPy 1.16+. Pingouin 0.5+ renamed power-function arguments to match the names used below.

---

## Quick recipes (closed-form)

The bundled `scripts/power.py` wraps statsmodels into one consistent interface so you don't have to remember which solver belongs to which test. Run from the skill directory or add `scripts/` to `sys.path`.

```python
from power import sample_size, power, mde, power_curve

# 1. How many per group to detect Cohen's d = 0.5, two-sided, 80% power?
sample_size(test="t_ind", effect_size=0.5, power=0.80, alpha=0.05)
# -> required n per group

# 2. Two groups, 3:1 allocation (e.g. more controls than cases)
sample_size(test="t_ind", effect_size=0.5, power=0.80, ratio=3.0)

# 3. Fixed n=30/group — what's the minimum detectable d at 80% power?
mde(test="t_ind", nobs1=30, power=0.80, alpha=0.05)

# 4. One-way ANOVA, 4 groups, detect Cohen's f = 0.25
sample_size(test="anova", effect_size=0.25, k_groups=4, power=0.80)

# 5. Two proportions: 0.40 vs 0.55 (auto-converts to Cohen's h)
sample_size(test="two_proportions", prop1=0.40, prop2=0.55, power=0.80)

# 6. Correlation: detect r = 0.30
sample_size(test="correlation", effect_size=0.30, power=0.80)

# 7. Power curve for the grant figure
power_curve(test="t_ind", effect_size=0.5, n_range=range(10, 120, 5),
            save="power_curve.png")
```

Supported `test=` values: `t_ind` (two independent means), `t_paired`/`t_one` (paired or one-sample mean), `anova` (one-way), `two_proportions`, `one_proportion`, `correlation`, `chi2` (goodness-of-fit / contingency via effect size *w*), `linear_regression` (R² increment / f²). Full argument tables and the underlying statsmodels calls are in `references/closed_form_recipes.md`.

---

## When there is no formula: simulate

Closed-form power exists only for a handful of simple tests. For **logistic/Poisson regression, mixed-effects / repeated-measures models, cluster-randomized trials, survival analysis, mediation, multi-way interactions, or any non-standard analysis**, the right tool is simulation. The logic is always the same three steps:

1. **Simulate** a dataset from your assumed truth (the effect you want to detect, plus realistic noise, baseline rates, cluster structure, etc.).
2. **Analyze** it with the *exact* test/model you plan to use on the real data.
3. **Repeat** many times (≥1,000; 5,000–10,000 for a stable estimate near 80%). Power is the fraction of replicates in which the test is significant.

`scripts/simulate_power.py` provides a reusable harness plus worked examples (two-group difference, logistic regression, cluster-randomized trial with an ICC, and a linear mixed model). The core is just:

```python
from simulate_power import simulate_power

def gen_and_test(n, rng):
    # build a dataset of size n under the assumed effect, run the planned test,
    # return True if the result is significant
    ...

est = simulate_power(gen_and_test, n=200, n_sims=2000, alpha=0.05)
print(f"Power at n=200: {est.power:.3f} (95% CI {est.ci_low:.3f}-{est.ci_high:.3f})")
```

Report the **Monte Carlo confidence interval** on the estimate (the harness returns it) so the reader knows whether 0.81 vs. 0.79 is signal or simulation noise. See `references/simulation_based_power.md` for the full patterns, including how to search for the n that hits target power and how to model dropout and clustering.

---
