---
name: dex-robotics-engineering
description: Route dexterous-robotics work among retargeting, IK, impedance tuning, and HIL evidence review when the primary domain needs selection.
---

# Dexterous robotics engineering router

Select one primary route and read its matching skill below; load another route only when evidence shows it is needed. Existing generic skills are helpers for the relevant branch:

- `codebase-design` supports a new module, interface or algorithm architecture;
- `diagnosing-bugs` is the outer loop for a concrete failure, slowness or regression;
- `tdd` is used only at a confirmed public seam for a regression test;
- `visualize` is optional for offline plots and what-if comparisons;
- `teleop-hil-review` is a separate read-only review for HIL or physical-safety claims.

## Route priority

Use this order when multiple signals appear:

1. **Evidence route** — a request to connect a robot, run HIL, prove physical safety or declare real-robot readiness. Do not start hardware or ROS work automatically. Use `teleop-hil-review` for an identified Planner/Reviewer evidence audit; if the role or scoped provenance is missing, report the exact gap. This audit does not operate hardware.
2. **Retargeting route** — read [dex-retargeting-debug](../dex-retargeting-debug/SKILL.md) for MANUS/Wuji/Sharpa, landmarks and actions, frames, scale, calibration, pinch or aperture. Resolve geometry and representation issues before gain tuning.
3. **IK route** — read [dex-ik-design-debug](../dex-ik-design-debug/SKILL.md) for FK/Jacobians, solver stability and continuity, constraints, virtual walls or stale async results.
4. **Gain route** — read [impedance-gain-tuning](../impedance-gain-tuning/SKILL.md) for `kp/kd`, PD/PID, impedance, response dynamics or saturation.

If a prompt contains only generic “debug”, “broken”, “jitter” or “slow”, use `diagnosing-bugs` and ask which of the three domain routes is load-bearing only when the evidence cannot distinguish them. Do not activate all three domain routes in parallel.

## Conflict rules

- Retargeting plus `kp/kd`: make Retargeting primary; defer gains until coordinates, scale, aperture and output continuity are established.
- IK plus `kp/kd`: make IK primary when the symptom is residual, singularity, constraint violation or stale result; tune gains only after the solver target is trustworthy.
- New design plus bug report: use `codebase-design` for the seam, then `diagnosing-bugs` and the selected domain route.
- HIL plus implementation: keep implementation in the normal Coder workflow; use `teleop-hil-review` only for the independent Planner/Reviewer evidence audit.
- Replay, simulation, static tests and runtime health must be labeled separately; none automatically proves HIL or physical safety.

## Shared operating boundary

Before editing, identify the real checkout and dirty state. Establish install/runtime paths before runtime claims, and model, SDK, calibration artifact, units and control rate before interpreting data or changing control behavior. Preserve existing worktrees and running services. Default to read-only source inspection and offline/replay/fake evaluation; do not connect hardware (including VUT, ROKAE, MANUS or Wuji) or alter a live robot unless the user gives a concrete, authorized operation and the applicable review gate is satisfied.

Every completion claim must include the exact scope, fresh command or artifact evidence, and the highest evidence class actually established.
