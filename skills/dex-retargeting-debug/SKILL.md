---
name: dex-retargeting-debug
description: Design or debug motion retargeting across articulated models, including input frames, calibration, morphology, task objectives, contact intent, and replay.
---

# Motion retargeting design and debug

Use this skill for mapping observations or a source articulation into a target model's task or motion. It applies to hands and other articulated systems without assuming a sensor vendor, skeleton layout, joint count or optimizer.

## Locate the error

Identify the active checkout/runtime, source and target models, calibration provenance, adapter configuration and versioned contracts. Trace the stages actually present: raw observation, estimated articulation/keypoints, mapped task, kinematic proposal, final output and measured response. Compare corresponding samples to find the first incorrect stage.

For a concrete failure, use `diagnosing-bugs` to reproduce and minimize it. Consult project approach history before a new algorithm or retry; use `codebase-design` only when an interface decision is needed. A numerical solving defect inside the mapping can use [IK](../dex-ik-design-debug/SKILL.md) as its primary workflow.

## Representation and calibration

- Declare each boundary's representation: sensor poses, landmark arrays, articulated coordinates, task targets or actuator commands. Derive dimensions and ordering from the active contract. Verify finite values, identities, side/limb mapping and version compatibility; qualify whether a version names hardware, a model, an artifact schema or an algorithm.
- Verify units, origin, handedness, quaternion ordering, transform direction and composition. Distinguish transforming a point, direction and orientation. Confirm whether observations are already body-relative before applying a root/wrist transform. Test the actual conversion with known configurations; never infer an axis swap from a vendor name or reuse a display transform for control.
- Keep sensor mounting, body geometry and coordinate registration separate from mapping preferences, filtering and controller gains. For fitting, remounting, implausible geometry or low residual with wrong motion, read [calibration and observability](references/calibration-observability.md).

## Mapping objectives and morphology

State the behavior the user wants to preserve: endpoint position, relative pose, shape, direction, task-space motion or contact intent. Source and target can differ in scale, link lengths, topology, available degrees of freedom and range; exact joint-angle or absolute-point matching may not preserve that behavior.

Inspect the active loss and constraints: residual units/scales, endpoint and direction terms, topology/shape terms, posture/coupling priors, temporal terms and limits. Check how morphology changes the tradeoff. Use normalized shape or a task hierarchy when justified by the requested behavior and evidence; do not add a universal coupling ratio or simply raise a global weight to repair one pose.

For contact-related tasks, separate source intent/detection, model-based target proximity and physical contact. Define the relevant pair/region, frame, desired separation and priority, including object geometry if available. A “pinch” mode weight does not establish an aperture constraint, and zero endpoint distance is not a universal contact target.

Where modes exist, inspect entry/release, target selection, dwell, reset and continuity. Check required branch/posture constraints through all downstream solves. For filtering, limiting, asynchronous output or failure handling, use [execution contracts](../dex-robotics-engineering/references/execution-contract.md) and evaluate the final output, not only the optimized proposal.

## Acceptance

Use [replay validation](../dex-robotics-engineering/references/replay-validation.md) for stateful or numerical changes. Compare matching original inputs, timing and initial state with the intended configuration difference; include the affected transitions and protected behaviors. Report task error/completion and relevant shape, continuity, latency and limit metrics with failures and denominators.

Label root-cause corrections, task-specific compensation and diagnostic alternatives accurately. A compensation can be useful when explicitly chosen, but its activation, tradeoffs and non-regression scope must be visible. Do not close unresolved task criteria because a local test passed or a rendered posture looks better.

Calibrated estimates, mirrored samples and geometric replay have bounded evidential scope. Larger gains cannot repair wrong geometry or mapping objectives; physical tracking/contact claims need corresponding measurements.
