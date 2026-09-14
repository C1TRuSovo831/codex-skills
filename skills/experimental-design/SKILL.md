---
name: experimental-design
description: Plan experiments before data collection, including study designs, randomization, blocking, replication, and DOE layouts. Use statistical-power for sample size or MDE; use an analysis workflow for collected data.
allowed-tools: Read Write Edit Bash
compatibility: Requires Python >=3.10. Scripts use numpy, pandas, and pyDOE3 (DOE matrices). Install with uv as shown below.
license: MIT license
metadata:
  version: "1.2"
  skill-author: K-Dense Inc.
---

# Experimental Design

Choose the study structure before data collection, then produce an auditable,
seeded allocation or DOE layout. Use **statistical-power** for sample size or MDE
after choosing the design. For already-collected data, use the available analysis
workflow; related skills are optional and do not block this workflow if absent.

## Design invariants

- Identify the experimental unit, treatment assignment level, response, and true
  independent replicate. Repeated measurements are not independent replication;
  preserve clusters, nesting, and repeated-measures structure in the analysis.
- Randomize treatment assignment and run/processing order, and block or stratify
  known nuisance factors such as batch, day, site, operator, or plate position.
- Use appropriate concurrent controls and, where relevant, sham/vehicle controls
  and blinding. Keep condition separate from nuisance factors.
- Establish the effects and interactions to estimate, alias structure, and whether
  curvature matters before choosing a factorial, screening, or response-surface design.
- Preserve the design, random seed, schedule, and analysis plan so the assignment
  is reproducible and auditable.

## Choose the relevant guidance

Read only the branch needed for the current design:

| Task | Reference |
| --- | --- |
| Choose a design or audit confounding, pseudoreplication, aliasing, or curvature | [Design selection and structural risks](references/design_selection.md) |
| Assign treatments, block/stratify, choose controls, or lay out plates/batches | [Randomization and blocking](references/randomization_and_blocking.md) |
| Factorial/fractional designs, screening, resolution/aliasing, or response surfaces | [Factorial and DOE](references/factorial_and_doe.md) |
| Crossover, repeated measures, split plot, Latin square, cluster, or nested design | [Design types](references/design_types.md) |
| Interim analyses, sequential stopping, or adaptation | [Sequential and adaptive designs](references/sequential_and_adaptive.md) |
| Generate an allocation schedule or DOE matrix | [Layout generation, installation, and script examples](references/generating_layouts.md) |

## Workflow

1. **State the question, the unit, and the response.** What is randomized? What is
   measured? At what level is a true independent replicate? This determines everything.
2. **List nuisance factors** (batch, day, site, operator, position) — plan to block,
   stratify, or randomize across each.
3. **Pick the design** using the relevant design references.
4. **Decide replication** at the correct level (and get n from the
   **statistical-power** skill for the chosen design).
5. **Generate the layout** with `randomization.py` / `doe_designs.py`, seeded.
6. **Randomize run/processing order** and plate/batch positions.
7. **Document** the design, seed, and schedule (pre-register if possible) so the
   analysis is confirmatory and the layout is auditable.
8. **Match the analysis to the design** — blocks, strata, clusters, and nesting must
   appear in the model. Use **statistical-analysis** / **statsmodels** if available.

---

## Attribution

For methodological source references, or when this skill materially contributes to a
manuscript, report, presentation, or code release, follow
[source notes and the current-version citation procedure](references/source_notes.md).
