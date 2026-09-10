---
name: dex-ik-design-debug
description: Design or debug dexterous-teleoperation IK when the request involves FK, Jacobians, DLS, damping, seeds, null-space posture, singularities, QP/CBF constraints, virtual walls, stale async IK, or trajectory continuity.
---

# Dexterous-teleoperation IK design and debug

Use this skill for the robot-side kinematics and safety-constraint portion of a teleoperation stack. Keep upstream tracking, hand retargeting and hardware evidence as separate concerns.

## Route and first checks

For an observed failure, apply `diagnosing-bugs`: create a deterministic replay or fixture that asserts the wrong pose, residual, discontinuity, stale result or constraint violation. For a new solver interface, apply `codebase-design` first; use `tdd` at the agreed public seam.

Record the active checkout, revision or hash, URDF/model, base and tool frames, units, limits, controller rate, current joint state, target provenance and whether the result is synchronous or asynchronous. Never infer the running path from a similarly named directory.

## Solver checks

For the current URDF-driven numerical path, make the math explicit:

- compute FK and a 6-by-N geometric Jacobian in a named frame;
- form position error and orientation error such as `rotvec(R_target @ R_current.T)`;
- solve the damped least-squares step `dq = J.T @ solve(J @ J.T + damping**2 * I, error)`;
- verify damping, task weights, step limits, iteration and residual tolerances against the active configuration;
- compare current-q, URDF-midpoint and zero seeds; check reference-q continuity and null-space posture preferences;
- use finite-difference FK/Jacobian checks and log condition number or singular values before changing the algorithm.

Treat joint position, velocity, acceleration and jerk limits as constraints, not as post-hoc clipping. Reject stale or failed asynchronous results and hold the last valid command when input quality, calibration, watchdog, feedback or IK validity is lost.

## Constraint and virtual-wall design

For a constrained velocity formulation, make the objective, frame and constraint source explicit, for example:

`min_qdot ||J(q) qdot - vcmd||^2 + lambda ||qdot||^2`

with a safety condition such as:

`grad_q h(q,t)^T qdot + partial h / partial t >= -alpha h(q,t)`.

A usable virtual fixture for this stack must preserve tangential motion, prevent deeper normal violation, use a hard boundary `h=0`, recover toward a positive margin `h=delta>0`, add hysteresis and bound recovery velocity, acceleration and jerk. A penalty wall or an ordinary boundary damper alone does not establish inward recovery.

Separate evidence classes: source implementation, static checks, replay/simulation, runtime observation, hardware connection, HIL and physical-safety validation. A paper, static result or simulator run is not HIL proof.
