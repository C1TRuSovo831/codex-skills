---
name: dex-robotics-engineering
description: Diagnose and route robotics work across sensing and calibration, retargeting, IK, control response, and execution when the failing layer is unclear.
---

# Robotics engineering

Locate the first stage that violates the requested behavior, then use one primary domain workflow. Device brands, joint counts and words such as “jitter” do not determine that stage. Load another domain only when the evidence requires it.

## Establish the chain

Identify the active checkout, dirty state, installed/running code when relevant, model and calibration identity, units, coordinate frames, and the input/solve/command/feedback clocks. Trace the stages that actually exist, for example:

`observation -> state or geometry estimate -> task target -> kinematic proposal -> command shaping -> device command -> measured response`.

The order and ownership come from the current implementation. Align a failing sample across stages by source/session identity and time; find where it first becomes wrong. Source data, estimated state, proposed motion and measured response are distinct evidence.

Before changing an algorithm or architecture, consult the project's approach history and retry conditions. Reuse established results under matching conditions; record a changed assumption or acceptance target when proposing a different route.

## Select the workflow

| Failure or request | Primary workflow |
| --- | --- |
| Input frames, calibration, morphology, source-to-target mapping or task objectives | [Retargeting](../dex-retargeting-debug/SKILL.md); use its calibration reference for sensing/geometry diagnosis |
| FK/Jacobian, residual formulation, constrained solving, solution branch or virtual fixture | [IK](../dex-ik-design-debug/SKILL.md), even when the solver is inside a retargeter |
| Tracking dynamics, oscillation, saturation or gains with trustworthy targets | [Impedance and gains](../impedance-gain-tuning/SKILL.md) |
| Freshness, asynchronous ordering, fault response or command/feedback mismatch | Trace the responsible runtime using [execution contracts](references/execution-contract.md) |
| Existing logs or a claim of success/readiness | Inspect the scoped evidence; use [replay validation](references/replay-validation.md) for temporal or numerical claims |
| An authorized device operation | Follow the current project runbook or matching device tool/skill within the authorized scope |

For ambiguous mixed symptoms, see [routing examples](references/route-matrix.md). Use `diagnosing-bugs` for a concrete failure and `codebase-design` when an interface decision is needed. Add a regression at the affected public boundary when it can capture the failure. Do not impose an architecture redesign or a complete test suite on every diagnostic task.

Resolve an upstream target error before tuning downstream gains. If the task requests both analysis and implementation, keep its remaining acceptance criteria open after a partial fix or passing unit test.

## Scope and evidence

Inspection, replay, visualization, device connection and physical execution are different operations. Follow existing user authorization and applicable project procedures; a mention of hardware or a command in documentation does not authorize motion. A read-only evidence question needs no invented role or approval workflow.

For each material conclusion, state the supporting revision/configuration/session and evidence actually inspected. Software tests, replay, connected hardware, correlated physical response and safeguard validation support different claims; one does not automatically establish the others. Bound a review to its requested acceptance criteria rather than requiring physical evidence for a source-only claim.
