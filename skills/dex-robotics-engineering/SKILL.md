---
name: dex-robotics-engineering
description: Route natural-language engineering requests about dexterous-hand retargeting, teleoperation IK, impedance kp/kd tuning, and HIL or safety evidence into the correct bounded workflow.
---

# Dexterous robotics engineering router

You do not need to name a skill. Select exactly one primary route from the request and apply the matching domain procedure. Existing generic skills remain lower-level helpers:

- `codebase-design` comes before a new module, interface or algorithm architecture;
- `diagnosing-bugs` is the outer loop for a concrete failure, slowness or regression;
- `tdd` is used only at a confirmed public seam for a regression test;
- `visualize` is optional for offline plots and what-if comparisons;
- `teleop-hil-review` is a separate read-only review for HIL or physical-safety claims.

## Route priority

Use this order when multiple signals appear:

1. **Evidence route** — a request to connect a robot, run HIL, prove physical safety or declare real-robot readiness. Do not start hardware or ROS work automatically. If the Planner/Reviewer role or scoped provenance is missing, report the exact evidence gap.
2. **Retargeting route** — MANUS, Wuji, Sharpa, 21x3, 20 DOF, point order, coordinates, wrist-relative frames, scale, calibration, pinch or aperture. Geometry and representation issues must be resolved before gain tuning.
3. **IK route** — FK, Jacobian, DLS, damping, seeds, null-space, singularity, QP, CBF, virtual wall, stale async results or trajectory continuity.
4. **Gain route** — `kp`, `kd`, PD/PID, impedance, stiffness, damping, overshoot, settling, oscillation, step response or saturation.

If a prompt contains only generic “debug”, “broken”, “jitter” or “slow”, use `diagnosing-bugs` and ask which of the three domain routes is load-bearing only when the evidence cannot distinguish them. Do not activate all three domain routes in parallel.

## Conflict rules

- Retargeting plus `kp/kd`: make Retargeting primary; defer gains until coordinates, scale, aperture and output continuity are established.
- IK plus `kp/kd`: make IK primary when the symptom is residual, singularity, constraint violation or stale result; tune gains only after the solver target is trustworthy.
- New design plus bug report: use `codebase-design` for the seam, then `diagnosing-bugs` and the selected domain route.
- HIL plus implementation: keep implementation in the normal Coder workflow; use `teleop-hil-review` only for the independent Planner/Reviewer evidence audit.
- Replay, simulation, static tests and runtime health must be labeled separately; none automatically proves HIL or physical safety.

## Shared operating boundary

Before editing, identify the real checkout, dirty state, install/runtime path, model, SDK, calibration artifact, units and control rate. Preserve existing worktrees and running services. Default to read-only source inspection and offline/replay/fake evaluation; do not connect VUT, ROKAE or MANUS or alter a live robot unless the user gives a concrete, authorized operation and the applicable review gate is satisfied.

Every completion claim must include the exact scope, fresh command or artifact evidence, and the highest evidence class actually established.
