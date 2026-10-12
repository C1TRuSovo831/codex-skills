---
name: dex-ik-design-debug
description: Design or debug inverse kinematics for articulated models, including FK/Jacobians, constrained solving, solution continuity, and virtual fixtures.
---

# Inverse kinematics design and debug

Use this skill for the numerical kinematics of an articulated model, including a solver embedded in retargeting. Establish the target's meaning separately from whether the solver reaches it; estimated skeletal coordinates and actuator coordinates may describe different models.

## Establish the problem

Record the active source/runtime revision, model, configuration and tangent dimensions, joint order, frames, units, limits, current state, target provenance and relevant clocks. Use the actual model format; a URDF, fixed base, six-dimensional task or particular joint count is not assumed.

For a failure, reproduce the affected residual, discontinuity or constraint violation with a focused fixture or replay. Use `diagnosing-bugs` when the cause needs investigation, and `codebase-design` when a new interface decision is required. Consult the project's approach history before changing the method or retrying a rejected approach.

## Residuals and derivatives

- Define the task: position, orientation, relative pose, direction, multiple endpoints or a hierarchy. Derive residual dimension from that task; a three-dimensional position target does not require an orientation objective.
- Name the frame and perturbation convention for each residual/Jacobian. A geometric velocity Jacobian is not automatically the derivative of an orientation-log residual; include the appropriate rotation differential when required. Use the model's tangent/update operation for non-Euclidean configurations.
- Separate unit normalization from task preference. Document residual scales before comparing metres, radians or dimensionless shape terms; a weight alone does not define a hard constraint or strict priority.
- Check FK and the actual residual Jacobian against finite differences in representative configurations, including near relevant limits or orientation branch cuts. Inspect scaled singular values or conditioning when diagnosing rank or sensitivity; do not infer rank from mixed-unit magnitudes alone.

## Solve within the actual constraints

Inspect the existing formulation before selecting DLS, bounded least squares, QP or nonlinear optimization. For an unconstrained, consistently scaled residual `r` with Jacobian `J = dr/dq`, a DLS example is `dq = -J.T @ solve(J @ J.T + damping**2 * I, r)`. This example is not a constrained solver or a required implementation.

Verify damping, step acceptance, evaluation budgets, task tolerances and termination status against the active configuration. Incorporate the required joint/task bounds into the solve where they affect feasibility. An unconstrained step followed by componentwise clipping can stall at a reachable boundary and can change task priorities; retain final validation even with a bounded solver.

Distinguish geometric reachability, reachability within the current motion window, insufficient action time, and local numerical failure. A failed local solve is not an infeasibility certificate. Use a known feasible witness, alternative admissible seeds or an independent bounded solve when that distinction matters; multiple failed starts alone still do not prove global infeasibility.

Check continuity and branch selection using the last accepted state, appropriate posture preferences and application constraints. Equal endpoint poses may have different intermediate geometry and future motion. Do not prescribe zero seeds, anatomical coupling or one preferred bend direction for every model. If a branch must recover, preserve the existing motion limits during recovery.

## Composition and runtime

For postprocessing, asynchronous solving or fault handling, read [execution contracts](../dex-robotics-engineering/references/execution-contract.md). Validate task semantics on the final accepted output after filters, shaping and mode transitions. A later solver must inherit the constraints that remain applicable; an earlier proposal is not the executed command.

Reject obsolete or invalid results according to session/sequence and validity rules. Map recoverable source gaps, feedback loss, malformed data and device faults to the actual controller's distinct responses. HOLD, stop and disable are not interchangeable universal fallbacks.

Use [replay validation](../dex-robotics-engineering/references/replay-validation.md) for dynamic or performance changes. Compare the affected continuous transitions and protected behaviors, and separate computation time from action duration and physical response.

## Virtual fixtures, when requested

State whether the requirement is boundary avoidance, inward recovery, tangential freedom or another behavior. For a velocity formulation, one example is minimizing `||J qdot - vcmd||^2 + lambda ||qdot||^2` subject to a condition such as `grad_q h(q,t)^T qdot + partial h / partial t >= -alpha h(q,t)`, with an explicitly defined safe set `h >= 0`.

Explain feasibility, model assumptions, sampling and delay, actuator limits and the fallback when constraints conflict. A continuous-time condition alone does not establish sampled hardware safety. If positive-margin recovery is required, verify recovery speed and interaction with other tasks; a penalty or boundary damper alone does not establish that behavior. Add hysteresis only where switching behavior calls for it.

Scope conclusions to the model, inputs and evidence tested. Software, replay and physical validation support different claims.
