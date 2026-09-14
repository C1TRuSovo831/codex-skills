---
name: statistical-power
description: Calculate study sample size, power, minimum detectable effects, and sensitivity curves for a planned analysis. Use experimental-design to choose or lay out the study; use an analysis workflow for collected data.
allowed-tools: Read Write Edit Bash
compatibility: Requires Python >=3.10. Examples target statsmodels >=0.14.6, scipy >=1.11, pingouin >=0.6, numpy >=1.26, and matplotlib. Optional extras are statsmodels mixed models and lifelines for simulation-based power.
license: MIT license
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
---

# Statistical Power & Sample Size

Calculate required sample size, power, or MDE for the planned analysis. For a fixed
test and its assumptions, sample size, effect size, significance level (α), and
power (1 − β) determine one another. State assumptions and report sensitivity to
plausible effects rather than presenting an unsupported single sample size.

Choose the study structure with **experimental-design** before calculating power;
return to it when laying out the final allocation. Analysis of collected data is
a separate workflow; use the relevant analysis skill if available.

## The one decision that drives everything: the effect size

Power calculations are only as trustworthy as the effect size you feed them. **Do not invent a number.** Use, in rough order of preference:

1. A **minimally important effect** — the smallest effect that would actually change a decision or matter scientifically/clinically (the "smallest effect size of interest", SESOI). This is the most defensible basis: you power to detect what matters, not what you hope to see.
2. A **pilot or prior-study estimate**, but shrink it — published and pilot effects are inflated by publication bias and the winner's curse. Powering on a raw pilot estimate routinely underpowers the real study.
3. A **convention** (Cohen's small/medium/large) only as a last resort, and say so explicitly.

Whatever you pick, run a **sensitivity analysis**: report how required n changes across a plausible range of effect sizes, not a single point. A power analysis presented as one number hides its biggest source of uncertainty. See `references/effect_sizes.md` for benchmarks and conversions between d, f, r, η², odds ratios, and Cohen's h/w.

> **Avoid post-hoc ("observed") power.** Computing power from the effect size you just estimated is circular: it is a deterministic function of the p-value and tells you nothing new. If a study is already done and you want to know what it could have detected, report a **sensitivity analysis** (MDE at the achieved n) or, better, the confidence interval around the observed effect. This is a common reviewer complaint — do not produce observed power even if asked without flagging the issue.

---

## Select the calculation

| Task | Read |
| --- | --- |
| Choose or convert an effect size | [Effect sizes](references/effect_sizes.md) |
| Standard t-tests, ANOVA, proportions, correlations, chi-square, or linear regression | [Closed-form argument tables and recipes](references/closed_form_recipes.md) |
| GLMs, mixed/repeated-measures models, cluster trials, survival, mediation, interactions, or other nonstandard analyses | [Simulation-based power](references/simulation_based_power.md) |
| Install dependencies or call bundled `power.py` / `simulate_power.py` | [Calculation setup and examples](references/calculation_workflow.md) |
| Write or audit a sample-size justification | [Reporting template, pitfalls, and sources](references/reporting.md) |

For simulation, generate realistic data and analyze each replicate with the exact
planned test/model. Report assumptions, simulation count, and the Monte Carlo
confidence interval; small power differences may be simulation noise.

## Adjustments people forget

These routinely make the difference between an adequately powered study and an underpowered one. Apply them explicitly and state that you did.

- **Multiple comparisons.** If the analysis tests *m* hypotheses with a Bonferroni-style correction, power each test at the corrected α (e.g. α/m), which raises n. Better: power on the family-wise or FDR-controlled procedure directly via simulation. Ignoring this silently underpowers every secondary endpoint.
- **Attrition / dropout / unusable samples.** Power gives the n you need *analyzed*. Inflate the *enrolled* n: `n_enroll = ceil(n_analyzed / (1 − dropout_rate))`. A 20% dropout rate means enrolling 25% more than the formula returns.
- **Clustering (design effect).** When observations are nested (patients within clinics, cells within animals, repeated measures within subject), the effective sample size is smaller than the raw count. Inflate by the design effect `DEFF = 1 + (m − 1)·ICC`, where *m* is cluster size and ICC the intraclass correlation. Treating clustered data as independent is **pseudoreplication** and badly overstates power — for cluster-randomized designs, simulate instead.
- **One- vs. two-sided.** Two-sided is the default and almost always the right choice; a one-sided test buys power only by refusing to detect an effect in the unexpected direction. Justify any one-sided test.
- **Unequal allocation.** Equal groups are most efficient for a fixed total n. If allocation is fixed by design (e.g. 2:1 treatment:control), pass `ratio=` so the calculation reflects it.

---

## Workflow

1. **State the design and the planned analysis.** The test you will run determines the power method. If the analysis is a mixed model or GLM, go straight to simulation.
2. **Choose the effect size** on a defensible basis (SESOI > shrunk pilot > convention) and write down the justification.
3. **Set α and target power.** Conventional defaults are α = 0.05 (two-sided) and power = 0.80; 0.90 is common for confirmatory/clinical work. State them.
4. **Compute** with `scripts/power.py` (closed-form) or `scripts/simulate_power.py` (simulation).
5. **Sensitivity analysis.** Recompute across a range of plausible effect sizes and produce a power curve. This is the deliverable, not a single number.
6. **Apply adjustments** for dropout, clustering, and multiplicity.
7. **Report** with the inputs and reproducibility details in [the reporting template](references/reporting.md).

---

## Scripts and completion

- `scripts/power.py`: `sample_size`, `power`, `mde`, and `power_curve` for standard tests.
- `scripts/simulate_power.py`: `simulate_power` and `find_sample_size`, with worked
  two-group, logistic, cluster-randomized, and linear mixed-model examples.

The deliverable includes the planned analysis, justified effect-size range, α and
sidedness, target power, allocation, required analyzed/enrolled sample sizes,
dropout/clustering/multiplicity adjustments, and sensitivity results. Include the
data-generating assumptions and Monte Carlo interval for simulations.

When this skill materially contributes to a manuscript, report, presentation, or
code release, follow [the current-version citation procedure](references/reporting.md#citing-scientific-agent-skills).
