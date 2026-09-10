---
name: impedance-gain-tuning
description: Tune or debug robot hand and arm kp/kd, PD/PID, or impedance behavior when the request involves overshoot, settling, stiffness, damping, step response, oscillation, saturation, or control-loop gains.
---

# Impedance and gain tuning

Use this skill after geometry and IK are stable enough that a control response is meaningful. It covers software outer loops, hand/arm command shaping and impedance behavior; it does not assume that the vendor SDK exposes the same loop or units.

## Identify the actual loop first

Record the active checkout and configuration, control layer (position, velocity or torque), vendor inner-loop gains, command and feedback units, sample period `dt`, delay, filtering, saturation, rate limits and watchdog behavior. Check whether a derivative term uses measured velocity; differentiating a setpoint step can cause derivative kick. Do not tune an outer PID on top of an unknown inner PID.

For a torque impedance loop, use the model as a reference:

`tau = Kp * (qd - q) + Kd * (qd_dot - q_dot) + tau_ff`.

The usual units are `N m/rad` and `N m s/rad`, subject to the drive's actual interface. An estimate such as `Kd ≈ 2*zeta*sqrt(M*Kp)` is only an initial value; identify or bound the effective inertia `M` and then measure the response.

## Tuning procedure

1. Establish a safe offline, replay, simulator or fake baseline with identical input, timing and limits.
2. Tune an inner loop before an outer loop. Within one loop, change one variable at a time; do not use larger `Kp` to hide retargeting or IK errors.
3. Sweep `Kp` over a bounded range, then `Kd` and derivative filtering. Keep position, velocity, acceleration, jerk, torque/current and workspace limits active.
4. Evaluate step and representative trajectory responses using rise time, settling time, overshoot, steady-state error, RMS tracking error, oscillation spectrum, delay, saturation rate and jerk.
5. Keep a reversible parameter record and rollback point. Stop on instability, repeated saturation, watchdog trips or limit violations.
6. Only after the offline/fake result is stable should a separately authorized HIL review consider a physical run.

Report whether each result is source, static, replay/simulation, runtime, HIL or physical-safety evidence. Never present a gain sweep or a stable simulator response as proof that a real robot is safe.
