---
name: impedance-gain-tuning
description: Tune or diagnose robot PD/PID, impedance, and command-response dynamics once targets, feedback semantics, and the controlled loop are understood.
---

# Impedance and gain tuning

Use this skill after geometry and IK are trustworthy enough to interpret the control response. Identify the actual loop exposed by the system; position-command shaping, a vendor servo and torque impedance need different evidence and parameters.

## Identify the actual loop first

Record the active code/configuration, control layer, command and measured-feedback units, inner-loop behavior, sample periods, delays, filtering, saturation, limits and watchdogs. Establish the supported interfaces before changing gains. Check whether a derivative term uses measured velocity; differentiating a setpoint step can cause derivative kick. For an integral term, inspect windup and reset behavior under saturation or mode changes.

Verify what telemetry fields mean. A field called `effort` may be current, estimated torque or a placeholder conversion. Force inference requires the applicable motor/transmission/friction model, contact geometry and load calibration; a numerical field name or a Jacobian transform is insufficient. Keep commanded achievement, measured tracking and physical contact/force distinct.

For a torque impedance loop, use the model as a reference:

`tau = Kp * (qd - q) + Kd * (qd_dot - q_dot) + tau_ff`.

For revolute coordinates and torque output, gains have units `N m/rad` and `N m s/rad`; translational or normalized interfaces use their own units. In a scalar second-order approximation, `Kd ≈ 2*zeta*sqrt(M*Kp)` is an initial estimate only. Identify or bound effective inertia and account for coupling, delay and the actual inner loop before interpreting it.

## Tuning procedure

1. Consult previous tuning results and retry conditions. Establish a baseline with known input, timing, load and limits. Replay can verify software shaping; evaluating changed feedback gains requires a suitable plant model or an authorized measured response. A fake interface without dynamics cannot demonstrate settling or stability.
2. Characterize inner-loop behavior before tuning an outer loop. Tune accessible loops in the appropriate order; do not assume vendor gains can or should be changed. Choose a bounded sweep or controlled experiment that can distinguish the suspected cause.
3. Keep the applicable motion, current/torque and workspace limits active. Record a reversible parameter set and stop/rollback criteria for instability, sustained saturation, faults or violated limits. For physical work follow the user's authorized scope and the actual project procedure.
4. Evaluate representative trajectories and, where appropriate, step responses using tracking error, rise/settling time, overshoot, oscillation, delay, saturation and command/response derivatives. Account for sampling, load and noise; do not attribute limiter or stale-input effects to gains without checking them.
5. For timing, fault response or output shaping, use [execution contracts](../dex-robotics-engineering/references/execution-contract.md). For paired dynamic comparisons and measurement definitions, use [replay validation](../dex-robotics-engineering/references/replay-validation.md). Preserve separate policies for source gaps, feedback loss and device faults.

Report the supported behavior, parameter range, load/configuration and evidence boundary. A stable model or software replay does not establish physical stability or contact force. Return upstream when incorrect geometry, target objectives or IK branches explain the symptom.
