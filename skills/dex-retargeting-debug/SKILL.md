---
name: dex-retargeting-debug
description: Debug or design dexterous-hand retargeting when the request involves MANUS, Wuji, Sharpa, 21x3 landmarks, 20 DOF actions, pinch, aperture, hand coordinates, calibration artifacts, or retargeting replay.
---

# Dexterous-hand retargeting debug

Use this skill for the hand-input and retargeting portion of a teleoperation stack. Keep the work bounded to the active checkout and artifact; do not infer runtime or hardware behavior from source alone.

## Route and first checks

If the request reports a failure, use the `diagnosing-bugs` discipline first: build a tight, red-capable replay or fixture, reproduce the exact symptom, minimize it, and rank falsifiable hypotheses. If a new module or seam is being designed, use `codebase-design` before implementation. Use `tdd` only after the public seam is confirmed.

Before interpreting a frame, record:

- active source checkout, revision or content hash, dirty state, and the running/install path if relevant;
- hand side, MANUS/Wuji/Sharpa model, SDK version, calibration artifact and model limits;
- timestamp, sequence, units, sample rate, frame name and coordinate convention.

The observed production shape to trace is:

`ManusGlove -> dex_manus_source -> CanonicalObservation.manus_hands -> MANUS raw to 21x3 -> RetargetSession.step() -> 20 DOF HandAction -> CanonicalAction -> hand_command -> manager -> hand worker -> StreamTracker`.

Treat the exact current checkout and local artifact as authoritative; v1 and v2 require their own model specification, adapter, limits and calibration artifact.

## Required diagnostic coverage

1. **Representation and frames**: verify `(21, 3)` shape, finite values, landmark order, wrist-relative origin, MANUS `xyz` versus Wuji `xzy`, `input_transform`, scale and offsets. Do not call 3D landmarks joint angles.
2. **Calibration versus motion control**: keep geometric calibration such as `uniform_scale` and wrist/thumb offsets separate from motion gains, smoothing and rate limits. Calibration scores are not controller gains.
3. **Losses and pinch**: identify tip-position, direction, full-hand, coupling, temporal and joint-bound terms. Distinguish human pinch detection, robot FK thumb-finger aperture and physical contact. A pinch mode weight is not an aperture constraint; if aperture matters, define an explicit FK-based pair term and its priority.
4. **Output and safeguards**: require a finite 20-element result, model-limit handling and clear behavior for NaN, infinity, wrong shape, expired input or SDK failure. Keep the last valid target rather than clamping arbitrary invalid data. Check downstream speed, acceleration and jerk limits.
5. **Replay acceptance**: compare identical input and configuration across variants. Report aperture error, pinch success and false contact, threshold jitter, solver latency, limit violations, jerk and task success. Record whether evidence is source, static, replay/simulation, runtime or HIL.

Do not use a larger `kp` to compensate for wrong coordinates, scale, point order or an incorrect aperture objective. Do not claim real contact, physical safety or HIL from geometric replay.
