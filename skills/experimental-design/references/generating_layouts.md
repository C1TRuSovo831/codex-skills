# Generate reproducible allocation and DOE layouts

Read the sections relevant to the requested workflow. Paths and command examples
are relative to the skill directory unless stated otherwise.

## Installation

```bash
uv pip install "numpy>=1.26" "pandas>=2.0" pyDOE3
```

`pyDOE3` is the maintained successor to pyDOE/pyDOE2 and supplies factorial,
fractional-factorial, Plackett-Burman, central-composite, Box-Behnken, and
Latin-hypercube generators. The bundled scripts wrap it to return designs in real
factor units with named columns and randomized run order.

---

## Generating the design

Two scripts produce ready-to-use, reproducible layouts. Run them from the skill's
`scripts/` directory or add it to `sys.path`. Everything is seeded so the exact
schedule can be archived and regenerated — a requirement for trial registration
and good lab practice.

### Randomization / allocation schedules — `scripts/randomization.py`

```python
from randomization import (
    simple_randomization, block_randomization,
    stratified_block_randomization, cluster_randomization,
    assign_factorial_runs, arm_balance,
)

# Permuted blocks keep the arms balanced throughout enrollment (use for n < ~100
# or sequential intake — simple randomization can drift out of balance with small n)
sched = block_randomization(n=60, arms=["treatment", "control"], seed=42)

# Balance a prognostic variable across arms by randomizing within each stratum
sched = stratified_block_randomization({"siteA": 30, "siteB": 30},
                                       arms=["drug", "placebo"], ratio=(2, 1), seed=42)

# Randomize whole clusters, not individuals (the cluster is the unit)
sched = cluster_randomization(["clinic1", "clinic2", "clinic3", "clinic4"], seed=42)

arm_balance(sched)            # sanity-check the counts per arm
sched.to_csv("allocation_schedule.csv", index=False)
```

Choosing among them: **simple** is fine for large n but can produce imbalance with
small n; **block** guarantees balance throughout; **stratified block** additionally
balances a known prognostic factor; **cluster** is mandatory when the intervention
is delivered at a group level. See `references/randomization_and_blocking.md`.

### DOE matrices — `scripts/doe_designs.py`

```python
from doe_designs import (
    full_factorial, two_level_factorial, fractional_factorial,
    plackett_burman, central_composite, box_behnken, latin_hypercube,
)

# Factors as real-world (low, high) ranges -> design comes back in real units
factors = {"temp_C": (20, 60), "conc_mM": (1, 10), "pH": (6, 8)}

# Full 2^3: all main effects + all interactions (8 runs), run order randomized
design = two_level_factorial(factors, seed=42)

# Screen 7 factors cheaply (main effects only)
many = {f"factor_{i}": (0, 1) for i in range(7)}
design = plackett_burman(many, seed=42)

# Optimize over 2 factors with curvature (response-surface)
design = central_composite({"temp_C": (20, 60), "conc_mM": (1, 10)}, seed=42)

design.to_csv("experimental_runs.csv", index=False)
```

Run order is randomized by default so factors aren't confounded with time/drift
(machine warm-up, reagent aging). See `references/factorial_and_doe.md` for picking
generators, reading the alias structure, and choosing resolution.

---

### Scripts
- `scripts/randomization.py` — seeded allocation schedules: `simple_randomization`,
  `block_randomization`, `stratified_block_randomization`, `cluster_randomization`,
  `assign_factorial_runs`, `arm_balance`.
- `scripts/doe_designs.py` — DOE matrices in real units: `full_factorial`,
  `two_level_factorial`, `fractional_factorial`, `plackett_burman`,
  `central_composite`, `box_behnken`, `latin_hypercube`.
