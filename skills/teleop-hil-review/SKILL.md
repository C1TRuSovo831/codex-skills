---
name: teleop-hil-review
description: Audit a scoped teleoperation hardware-in-the-loop or physical-safety evidence claim when the active role is unambiguously Herdr Planner or Reviewer. Use for HIL, real-robot readiness, physical motion, calibration provenance, or safety acceptance reviews; skip implementation tasks and other roles.
metadata:
  short-description: Audit scoped teleoperation HIL evidence
---

# Teleoperation HIL Review

Audit the evidence for a claim. Do not operate the teleoperation system.

## Entry gate

1. Read the current role contract. Proceed only as `Planner` or `Reviewer`.
2. If the role is missing, ambiguous, `Coder`, or any other role, reply `NOT RUN — teleop-hil-review requires the Planner or Reviewer role.` and stop.
3. Keep this invocation self-contained. Inspect evidence directly with read-only tools; do not spawn or delegate to another agent, contact Coder, or send Herdr handoffs.

Operate in inspection-only mode. Read source, configuration, diffs, existing logs, recorded telemetry, videos, and operating-system status through queries known to be non-mutating. Return the review in the conversation. Keep repository, process, ROS graph, calibration, and hardware state unchanged: do not write files, run commands that may emit artifacts, start or stop services, invoke ROS commands or service APIs, publish messages, command motion, use hardware control or calibration tools, or perform a physical safety test.

If the requested conclusion would require an operation, identify the missing evidence and bound the conclusion. Do not perform the operation.

## Classify every material claim

Use these evidence classes independently; a later class does not imply the earlier ones were established:

| Class | What it establishes | What it does not establish |
|---|---|---|
| `SOURCE IMPLEMENTED` | The inspected revision contains the relevant path or logic. | That it builds, runs, reaches hardware, or behaves correctly. |
| `STATIC VERIFIED` | Provenance-bearing lint, typecheck, unit, or static results support the exact revision. | A running service or physical data path. |
| `RUNTIME OBSERVED` | A process, service, endpoint, or live data stream was observed. | That the intended hardware generated the data or that a robot moved. |
| `SIM/FAKE CHAIN OBSERVED` | The scoped chain ran with a simulator, fake arm, replay, or mock component. | Physical robot HIL. |
| `HARDWARE CONNECTED` | Identified physical devices were enumerated or connected. | Fresh pose, correct mapping, actuation, closed-loop behavior, or safety. |
| `REAL HIL OBSERVED` | The intended current code/config carried fresh physical input through the scoped chain to correlated physical robot response. | Safety outside the tested scenario or readiness for broader operation. |
| `PHYSICAL SAFETY VALIDATED` | The scoped run has evidence for its stated safeguards and supervision. | General safety certification or safety in untested conditions. |

Attach a provenance grade to each item:

- `OBSERVED NOW`: inspected directly during this review through a non-mutating source or status query.
- `ARTIFACT OBSERVED`: inspected in a saved log, telemetry capture, video, or report with traceable identity and time.
- `REPORTED`: stated by the user, another agent, or an unverified transcript.
- `NOT SHOWN` or `CONTRADICTED`: absent or inconsistent evidence.

A user report is evidence of what was reported, not an observation of the hardware event. Never upgrade `REPORTED` to `OBSERVED NOW` or `ARTIFACT OBSERVED` without corroborating material inspected in this review.

## Require scoped HIL provenance

Use `REAL HIL OBSERVED` only when the evidence identifies all material parts of the claim:

- the exact scenario and acceptance criterion, including which physical input, mapping/controller path, robot output, and feedback path are in scope;
- repository revision and dirty state, relevant configuration, and component versions;
- hardware model, role, serial or other stable identity, firmware where material, and mounting/provenance where pose interpretation depends on it;
- map/session identity and calibration provenance for the tested run;
- fresh, time-correlated input, command, and measured physical response, with stale-data handling visible where relevant;
- actual physical robot motion or actuation corresponding to the command, not only a command publication, health check, or device-presence signal;
- the safety envelope claimed for the run: reachable E-stop, applicable software/hardware limits, speed/torque restrictions, cleared workspace, and named human supervision;
- for a haptic or bilateral claim, the physical return-feedback path and its observed response.

Treat `common_map_valid` (and `valid_6dof`) as VUT localization/common-map evidence only. `common_map_valid` is not robot extrinsic calibration, and it does not prove guided mapping, IK correctness, robot motion, or physical safety.

When provenance is incomplete, record only the narrower classes actually supported and list the exact missing evidence. Scope every conclusion to the tested hardware identities, revision, configuration, session, time window, and motion scenario; do not generalize one successful case to system-wide readiness.

## Review workflow

1. Restate the requested acceptance boundary and separate implementation, runtime, HIL, and safety claims.
2. Inspect the available evidence without changing state. Record provenance before interpreting results.
3. Build a claim-by-claim evidence table with: claim, evidence class, provenance grade, supporting artifact, gap, and scope.
4. Challenge the strongest claimed class first. Look for revision mismatch, stale timestamps, simulator substitution, hardware identity ambiguity, session mismatch, missing robot feedback, and safety evidence gaps.
5. Decide against the requested acceptance criteria, not against an unstated broader standard. Missing real HIL blocks a request to prove HIL, but does not by itself fail a source-only or static-only review; that narrower review must still state that HIL was not established.

## Authority and output

As `Reviewer`, the first line must be exactly `PASS` or `CHANGES_REQUIRED`:

- Return `PASS` only when the requested review boundary is satisfied with no blocking finding. State the evidence classes supported and the unverified boundaries. This is not final approval.
- Return `CHANGES_REQUIRED` when a blocking claim is unsupported, evidence is missing or contradictory, or the review basis is insufficient. Name the missing evidence precisely.

As `Planner`, the first line must be exactly `APPROVED` or `NOT APPROVED`. Final approval belongs only to Planner and requires Planner's own final sanity check; Reviewer `PASS` is necessary when the team contract requires it, but is not sufficient. Missing review basis yields `NOT APPROVED` with the missing evidence identified.

When this runs from a normal correlated Herdr Reviewer handoff, preserve the
active role contract exactly: after the line-1 status, echo the received
`TASK_ID`, `ROUND`, and `HANDOFF_ID` as consecutive lines 2 through 4 before
the review body. Missing, invalid, or mismatched correlation fields require the
role contract's fail-closed `CHANGES_REQUIRED` response; never invent an ID.
The Planner's direct user-facing final result does not add correlation fields
unless its active contract explicitly requires them.

After the first line, report:

1. requested scope and evidence boundary;
2. the claim-by-claim evidence table;
3. blocking findings first, then non-blocking gaps;
4. the exact scope of the verdict and the next evidence needed, without starting that work.
