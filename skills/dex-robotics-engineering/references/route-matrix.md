# Route matrix

| Priority | Route | Strong triggers | Primary work | Do not infer |
| --- | --- | --- | --- | --- |
| 1 | evidence | HIL, real robot, physical safety, readiness | provenance and independent safety review | source/replay is HIL |
| 2 | retargeting | MANUS, Wuji, 21x3, 20 DOF, pinch, aperture, coordinate, calibration | representation, transforms, losses, limits, replay | geometric aperture is contact |
| 3 | IK | FK, Jacobian, DLS, QP, CBF, singularity, virtual wall, stale IK | solver math, frames, constraints, continuity | penalty wall proves recovery |
| 4 | gain | kp, kd, PD, PID, impedance, overshoot, settling | loop identification, bounded sweep, response metrics | high Kp repairs mapping |

Generic failure words activate `diagnosing-bugs` as the outer feedback loop. A new interface activates `codebase-design` before the selected route. A regression at a confirmed public seam activates `tdd` after the red replay exists. `visualize` is optional and never upgrades evidence.
