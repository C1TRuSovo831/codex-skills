# Design selection and structural risks

Read the sections relevant to the requested workflow. Paths and command examples
are relative to the skill directory unless stated otherwise.

## Overview

The design of a study — how units are assigned to conditions, what is held constant, what is varied, and in what structure — determines what questions the data can answer. No analysis can rescue a confounded or pseudoreplicated design after the fact. This skill is about the decisions made *before* data collection: picking a design that isolates the effect of interest, randomizing to license causal claims, blocking to remove known nuisance variation, and structuring multi-factor experiments so effects are estimable rather than tangled together.

The three ideas behind almost every good design (Fisher's principles):
- **Randomization** — assign treatments at random so that confounders, known and unknown, are balanced in expectation. This is what turns a comparison into a causal claim.
- **Replication** — independent repetition at the right level, so you can estimate variability and your effects aren't artifacts of a single unit. The most common fatal error is **pseudoreplication**: counting repeated measurements on the same unit as independent replicates.
- **Blocking / local control** — group similar units (by batch, day, site, litter) and randomize within blocks, removing that nuisance variation from the error term instead of letting it inflate noise.

This skill helps you choose among design types, generate the actual randomization or DOE layout (with reproducible scripts), and avoid the structural mistakes that make data uninterpretable.

## Choosing a design

Start from the question and the structure of your units, not from a favorite design.

```
What are you trying to learn?
│
├─ Compare a few predefined conditions (A vs B vs C)?
│   ├─ Units independent, possibly with a known nuisance factor (day, batch, site)?
│   │     → Completely randomized (no nuisance) or RANDOMIZED BLOCK design.
│   ├─ Each unit can receive every condition in sequence (washout possible)?
│   │     → CROSSOVER / repeated-measures design (more power, watch carry-over).
│   └─ You can only randomize groups, not individuals (schools, clinics)?
│         → CLUSTER-randomized design (analyze at the cluster level; see pseudoreplication).
│
├─ Screen MANY factors (5+) to find the few that matter?
│     → FRACTIONAL FACTORIAL or PLACKETT-BURMAN screening design.
│
├─ Quantify main effects AND interactions among a handful of factors?
│     → FULL 2^k FACTORIAL design.
│
├─ Find the settings that OPTIMIZE a response (curvature matters)?
│     → RESPONSE-SURFACE design: central composite or Box-Behnken.
│
└─ Explore a simulation/computer model over a continuous space?
      → SPACE-FILLING design: Latin hypercube.
```

Detailed guidance per branch:
- **Randomization, blocking, stratification, controls** → `references/randomization_and_blocking.md`
- **Factorial, fractional-factorial, screening, response-surface, DOE concepts (aliasing, resolution)** → `references/factorial_and_doe.md`
- **Crossover, repeated-measures, split-plot, Latin-square, cluster, nested designs** → `references/design_types.md`
- **Sequential, group-sequential, and adaptive designs (interim analyses)** → `references/sequential_and_adaptive.md`

---

## The mistakes that ruin studies

These are structural — they can't be fixed in analysis, only in design.

1. **Pseudoreplication.** Treating repeated measurements of one unit as independent
   replicates: 3 mice with 100 cells each is n = 3 (mice), not n = 300 (cells), for
   any treatment applied to the mouse. The replicate must be at the level the
   treatment is randomized. This single error invalidates a large share of published
   experiments. Randomize and replicate at the right level; analyze with the nesting
   respected (mixed model). See `references/design_types.md`.
2. **Confounding by a nuisance variable.** Running all treatment samples on Monday
   and all controls on Tuesday confounds treatment with day. Randomize across, or
   block on, every nuisance factor you can name (batch, day, plate, technician,
   instrument, position).
3. **No or broken randomization.** Convenience assignment (first-come → treatment)
   lets confounders sneak in. Use a seeded schedule and follow it.
4. **No proper control.** Without a concurrent control (and, where relevant, a
   vehicle/sham and blinding), you can't separate the treatment effect from time,
   placebo, or handling effects.
5. **Batch effects mistaken for biology.** In omics especially, process samples in a
   randomized/blocked order across batches; never let batch align with the condition.
6. **Edge/position effects on plates.** Evaporation and thermal gradients make plate
   edges differ. Randomize or block sample positions; don't put all controls in
   column 1.
7. **Aliasing ignored in fractional designs.** A low-resolution fractional factorial
   confounds main effects with interactions; know your alias structure before
   concluding a factor "has no effect."
8. **Optimizing without curvature.** A two-level factorial can't detect a curved
   response; you'll miss an interior optimum. Use a response-surface design.

---
