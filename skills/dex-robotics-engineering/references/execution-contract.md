# Final output, freshness and failure response

Read this when a change affects postprocessing, asynchronous solving, timing, admission, fault handling or the command/feedback boundary. Use the active device and application contracts for actual states, limits and thresholds.

## Follow one admitted sample

Record source/session identity, sequence and clock domain through observation, solver proposal, accepted output, transmitted command and feedback. Record the model/calibration revision when interpretation depends on it. A display transform is not a command transform; a model joint vector is not necessarily the drive's joint vector. Verify dimensions, order, sign, zero reference and units at the adapter boundary.

Separate model limits, task constraints, command envelopes and drive limits. Check the final accepted/transmitted result, including transformations after the optimizer. A finite solver result or an interface-compatible command does not establish physical tracking.

## Preserve task meaning through the output window

- Determine which objectives are soft, which constraints are hard, and which task has priority. A weighted sum alone does not prove strict priority.
- Derive the current feasible window from the actual accepted or measured state required by the controller and its timing contract. Do not replace that state with an unaccepted proposal.
- If filtering or limiting can invalidate a geometric task, evaluate it on the final output. Where task preservation is required, solve within the relevant window or explicitly account for the downstream transformation. Componentwise clipping can change relative pose, aperture and branch even while every joint remains within bounds.
- For a hierarchy, preserve the primary task's achievable result before improving a secondary objective. An unreachable exact target should not silently turn the secondary problem into an unusable equality constraint; report the primary residual and the allowed degradation under the project's policy.
- Inspect gate entry/exit, partner selection, release, reset and interrupted recovery. Smooth scalar weights do not by themselves guarantee continuous optimizer solutions. Check both slow transitions and fast motions under the real timing/window constraints.
- Carry required branch/posture constraints through later solvers. Equal endpoints may have different intermediate geometry or future reachable motion. Recover toward an allowed branch within the existing limits rather than jumping to a seed.

Keep final validation even when constraints are included in optimization. Do not introduce collision models, motion modes or stricter physical requirements merely because this checklist mentions constraints.

## Time and asynchronous ownership

Name source timestamp, host receipt, solve completion, publication and feedback time, including their clock domains. Compute ages only within a known domain or with a justified clock mapping. Identify which clock advances filters, mode dwell times and rate limits.

Define the accepted sequence/session policy. Late results from an older session or superseded request must not overwrite newer accepted state. Republishing a cached target must preserve its original source age; transport activity does not make stale input fresh. Treat latest-only preview, control admission and loss-sensitive recording according to their different contracts.

On gaps, duplicate/out-of-order samples or clock resets, follow explicit reset/recovery rules. Do not let a long pause accumulate an unbounded motion step or run a burst of catch-up commands. Keep visualization and logging from changing the intended control timing when evaluating performance.

## Failure actions are contract-specific

Build a small mapping for the failure paths being changed: cause, detected state, allowed output, latched status, recovery condition and responsible owner. Distinguish at least the applicable cases below; do not assign all of them the same action.

| Failure class | Determine from the active contract |
| --- | --- |
| Recoverable source gap or rejected IK proposal | Whether the driver can retain a last admitted target/HOLD, freshness expiry and how tracking resumes |
| Missing or stale measured state | Whether continued position/torque output is admissible; required stop, disable or recovery procedure |
| Non-finite data, wrong identity/order/dimension or invalid calibration | Admission rejection, fault propagation and whether the active session must stop |
| Device/controller fault, authority loss or explicit STOP | Required motion prohibition, stop/disable path, latching and confirmation before reuse |

HOLD can retain actuator effort; issuing a HOLD command is itself a device operation. A stopped or faulted device may prohibit it. Conversely, disabling can release a load, so do not invent a universal disable policy either. Use the documented controller behavior and bounded project fallback; if the required behavior is unknown, identify that gap before changing a live path.

Preserve the original typed fault and its cause across layers. Do not infer disconnection from absent telemetry or clear a latched fault because a later packet looks healthy. Recovery, re-enable and cleanup ownership must follow the actual contract.
