# Replay and performance validation

Read this for changes to temporal state, mapping objectives, solver behavior or runtime performance. Select cases and metrics that exercise the change; a narrow fix does not require every metric below.

## Comparison basis

Freeze input identity/hash, model/calibration, relevant configuration and code revision or dirty diff. Identify the intended difference between baseline and candidate. Each stateful variant needs its own solver/filter history, the same initial/reset conditions and matching source timing. Reuse cached stages only when their independence from the change is established.

Distinguish original recordings, selected prefixes, reconstructed streams, mirrored examples and synthetic holds. Missing accepted predecessors or state snapshots may prevent exact reproduction of an observed run. A comparison on the same visible inputs remains useful, but name that narrower claim. Do not label incomplete logs a full replay.

Keep the denominator: input, admitted, emitted, failed, missing and excluded samples; for stateful tasks also count complete activation/release episodes. Explain exclusions. Report both whether a task activated and whether it completed, including interruptions and available time. Success-only latency or residual summaries hide failure behavior.

## Acceptance beyond static poses

Use representative continuous segments containing the affected transitions: entry/release, competing targets, fast motion, bound activation, source gaps or resets. Static and synthetic cases isolate mechanisms; they do not establish continuous task success. Include unaffected behaviors needed for a non-regression claim.

Evaluate the final accepted output in the correct frame. Relevant measurements may include FK task error, shape/relative-pose error, limit violations, discontinuities, derivative peaks, completion rate and additional lag. State which are measured truth, model-derived quantities or proxies. Human pinch labels, robot FK proximity and physical contact are different variables; false-contact or force claims require an appropriate independent reference.

For a suspected geometry or adapter error, recompute the relevant invariant independently where practical, rather than checking only a status flag produced by the same path. Track source completion, transmitted-command completion, feedback-based completion and physical task success separately.

## Timing vocabulary

| Quantity | Evidence required |
| --- | --- |
| Solver computation | Measured start/end duration for the named stage; state warm-up, hardware and concurrent load |
| Simulated/source action duration | Source timestamps or an explicitly simulated clock; includes dwell/ramp time |
| Queue or end-to-end age | Corresponding timestamps with known clock mapping and exact start/end boundaries |
| Physical response | Time-correlated command and actual measured response, with sampling and alignment limits |

For performance changes report throughput and relevant latency distributions, tail values/maxima, deadline misses and dropped work. Average compute time does not prove a real-time bound. A faster accepted-output rate can result from dropping work; expose that tradeoff. Do not subtract unrelated clocks or present a frame-count-derived duration as a compute benchmark.

## Decision and retained evidence

Use the requested acceptance criteria, including protected behaviors. Separate root-cause fixes from task compensation and diagnostic candidates; state any residual tradeoff. A passing test subset does not close an unfulfilled task criterion. Preserve failed cases and prior conclusions when revising a candidate; consult the project's history before retrying a rejected mechanism.

Report what the evidence supports for each claim: source implementation, software checks, replay/simulation, observed runtime, identified hardware, correlated physical response or scoped safeguard validation. These are independent dimensions, not an automatic promotion ladder. A recorded user report and an inspected synchronized measurement have different provenance. Missing physical evidence limits a physical claim, without invalidating an otherwise satisfied software-only acceptance criterion.
