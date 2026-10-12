# Routing examples

Use these examples when more than one domain appears relevant. Establish the failing stage from current data; the examples are not a fixed priority order.

| Observation | First investigation | What would change the route |
| --- | --- | --- |
| A hand or arm solver stalls at a joint bound despite a feasible witness | IK: task residual, active bounds and branch | Incorrect target coordinates move the investigation upstream |
| Mapped posture looks wrong with low sensor residual | Retargeting/calibration: observability, morphology and objective | Correct estimate/target with a bad numerical solution points to IK |
| Smooth proposal becomes a discontinuous final command | Execution and IK: state transitions, filtering and the final feasible window | Smooth commands with oscillating feedback point to control dynamics |
| Device appears in discovery but does not follow | Execution: identity, admission, enable state, fresh commands, feedback and faults | Diagnose gains only after this chain works and targets are valid |
| User asks to inspect existing run evidence | Read-only assessment of the specified claim | Running a missing experiment is a separate operation with its own scope |
| User requests a specific device status operation | Matching device tool/runbook | Operation results alone do not prove mapping, actuation or safety |

For “slow” or “jittery,” first locate the variation: source noise, target changes, solver branch, queue/age, command shaping or measured dynamics. Compare corresponding timestamps and stage outputs before adding smoothing or changing gains.
