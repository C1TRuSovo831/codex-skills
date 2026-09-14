---
name: diagnosing-bugs
description: Diagnose persistent bugs or performance regressions with a symptom-specific reproduction and evidence-driven probes. Use when the cause needs investigation.
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

Use relevant `CONTEXT.md` entries when module or domain terminology matters, and consult ADRs when the diagnosis touches an architectural decision.

## Active workflow boundary

This skill never expands the authority granted by the active role or the
user's request. Under a Herdr role contract:

- **Planner:** inspect and reason read-only, define the diagnostic signal and
  relay an authorized self-contained handoff to the same-team Coder. Do not
  create harnesses, instrument files, start services, apply fixes, or use
  native sub-agents as a substitute for Herdr.
- **Coder:** build loops, instrument, test, and fix only within the current
  Planner handoff. Do not contact another role, delegate, or expand scope.
- **Reviewer:** remain read-only. Assess the supplied reproduction, diff, and
  evidence; do not create artifacts, instrument, start services, or fix code.

If a phase below would violate the active sandbox, no-write rule, no-delegation
rule, or task scope, describe the needed Coder action or missing evidence
instead of performing it.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first** — write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1 — Build a feedback loop

Build a **tight** pass/fail signal that goes red on the reported symptom. Reproduction, hypothesis testing, bisection, and instrumentation must use that signal rather than a nearby failure.

Choose the smallest loop that reaches the symptom. For construction options, flaky bugs, or blocked reproduction, read [references/feedback-loops.md](references/feedback-loops.md). Read code as needed to build the loop; a causal claim still requires the reproduction and probes below.

### Completion criterion — a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring" — it must be able to _catch this specific bug_.
- [ ] **Repeatable** — same verdict under controlled conditions, or a measured reproduction rate sufficient to distinguish probes for a flaky bug.
- [ ] **Fast enough to iterate** — remove unrelated setup while preserving the conditions that produce the symptom; some representative workloads legitimately take minutes.
- [ ] **Agent-runnable** — you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

Use code inspection to construct the reproduction. No red-capable command, no Phase 2; if access or artifacts prevent a loop, report what is missing without claiming a confirmed cause or fix.

## Phase 2 — Reproduce + minimise

Run the loop. Watch it go red — the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut — keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing** — removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3 — Hypothesise

Rank **multiple plausible hypotheses** before testing, with enough alternatives to challenge the first explanation. Use the evidence to choose how many are useful; do not invent candidates to meet a fixed quota.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (use the final Phase 1 loop result from Phase 5; rerun if subsequent changes invalidate it)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (search the prefix with `rg`)
- [ ] Throwaway prototypes are in a clearly marked removable debug location; follow the user's cleanup policy before deleting them
- [ ] State the confirmed cause and evidence in the final report and any requested commit or PR message; this does not authorize creating or sending either

After the fix, state any supported prevention opportunity. For architectural limitations such as a missing test seam or hidden coupling, give a scoped recommendation; use an architecture skill only if it is available and that follow-up is authorized.
