---
name: verification-before-completion
description: Check completion, fix, test, or build claims against evidence from the final changed state.
---

# Verification Before Completion

Match each success claim to evidence for the state being reported. Confidence, changed code, and another agent's success message are not verification.

## Evidence gate

Identify the check that establishes the claim, run it within the authorized scope, and inspect its output and exit status. Required checks must complete; a truncated or partial run supports only the part actually observed. If a check fails or cannot run, report the actual state and the limitation.

Evidence must be fresh enough to cover the final relevant files, configuration, and environment. A successful affected check in this task remains usable while that state is unchanged; a new message alone does not require rerunning it. Rerun after changes that could invalidate the result, and broaden testing when failures, task requirements, or unresolved risks justify it.

| Claim | Evidence needed |
|---|---|
| Tests pass | Completed output for the named suite or selected tests, with no failures |
| Linter is clean | Completed linter result for the stated scope |
| Build succeeds | Successful build exit status; lint alone is insufficient |
| Bug is fixed | Original symptom checked against the changed implementation |
| Regression test detects the bug | Observed failure without the fix and pass with it |
| Delegated work is complete | Inspect the resulting diff or artifact and relevant checks |
| Requirements are met | Account for the requested outcomes; test results alone may not cover them |

## Report and finish

State what was checked and what that evidence proves. Keep uncertainty explicit: source inspection, an offline test, a build, a running service, and hardware behavior establish different things. A targeted check can support a targeted claim; it cannot establish that every test or environment passes.

For regression evidence, prefer the recorded failing test before the fix. If a controlled before/after comparison is still needed, isolate it and preserve user changes; do not revert an active workspace casually just to produce evidence.

Complete the remaining authorized work and checks before declaring success or preparing a commit or PR. Verification does not itself authorize commits, pushes, external messages, deployment, or other out-of-scope actions.
