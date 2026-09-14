---
name: writing-for-agents
description: Write or revise agent instructions, including skills, AGENTS.md, CLAUDE.md, and their supporting references.
---

# Writing for Agents

Write instructions that make the intended outcome, decision boundaries, and completion criteria clear. Preserve the user's scope and existing operational guarantees; give capable agents room to choose routine implementation details.

For skill frontmatter, invocation policy, and routers, read [SKILL-MECHANICS.md](SKILL-MECHANICS.md). For a narrow instruction edit, inspect only the affected guidance and its callers.

## Active workflow boundary

This reference never grants file-write or delegation authority. Under a Herdr role contract, Planner may inspect and specify the required agent document but must relay edits through the same-team Coder; Coder may edit only within the current Planner handoff; Reviewer remains read-only and reports corrections without applying them. Never use native sub-agents or this document's hand-off concepts to bypass active Herdr routing, no-write, or no-delegation rules.

## Context pointers

A **context pointer** names material outside the current context and states when to read it. Skill descriptions and conditional links in `AGENTS.md` are both pointers. Keep each short and discriminating: what the material does, and which distinct task branches need it. Collapse synonyms that describe the same branch; avoid keyword lists that attract unrelated work.

If essential guidance is repeatedly missed, first clarify its pointer. Inline it only when that still fails. Route to architecture docs for service-boundary decisions, for example, rather than requiring them before every edit.

Every pointer spends **context load**: tokens and attention whenever it is visible. Separate documents also spend **cognitive load**: the human must understand which documents exist and when to reach them. Split when the selective reading saves more than this routing costs; a short self-contained skill needs no extra router.

## Information hierarchy

Place information according to when it is needed:

1. **In-file steps:** actions whose order matters for correctness or a fragile workflow.
2. **In-file reference:** shared definitions, constraints, and decision criteria.
3. **Disclosed reference:** substantial guidance needed only by a specific branch, linked with a clear reading condition.

Use **progressive disclosure** to keep shared purpose and constraints in the entrypoint and conditional detail in references. Load only the applicable branch. Use **co-location** within each file: keep a concept's definition, rules, and exceptions together. Avoid both duplication and scattering one rule across several headings.

**Sprawl** can persist even when each line is unique. Split by real task branches rather than arbitrary length, or shorten the explanation when the agent already knows the mechanics.

## Completion criteria and sequences

Define completion as an observable result: the requested behavior works, the artifact is reviewable, and relevant checks support the claim. Name known stopping boundaries, unresolved dependencies, and evidence limits. A change list alone does not establish that the task is complete.

Balance **clarity** (can the agent tell done from not-done?) and **demand** (what work must be accounted for?). Scope exhaustiveness to the actual task; do not require every possible check or a new full run after each message.

Prefer outcomes and decision criteria to fixed recipes. Preserve ordered steps where their order is load-bearing, such as a failing test before a fix. If later steps demonstrably cause premature completion of an ambiguous stage, sharpen that stage's criterion first. Split by sequence only when needed; hiding later steps requires a real context boundary, not another heading. Any handoff or subagent dispatch still requires the active workflow's authority.

## Vocabulary and phrasing

A **leading word** is a compact, shared concept such as "seam" or "red" that can connect prompts, docs, and code. Reuse established vocabulary when it preserves meaning; define unfamiliar terms and avoid replacing a clear instruction with an ambiguous slogan. Repeating a useful term is different from repeating its full definition.

State the desired behavior directly. Keep explicit prohibitions when they express real scope, safety, or compatibility boundaries, and pair them with the allowed action where helpful. Treat claims about phrasing effects as heuristics to validate in use, not universal facts about every model.

## Pruning and validation

- Keep each meaning in one authoritative place. Preserve links and callers when moving guidance.
- Treat configuration, directory structure, and tool help as sources of truth. Cache only costly lookups or non-obvious conventions and reasons; avoid duplicating easily checked facts that can drift.
- Remove stale material and **no-ops**: generic advice that does not improve decisions for the intended agents. Model capabilities vary, so preserve useful cross-model constraints rather than assuming all readers share one model's defaults.
- Remove repeated explanations before removing operational guarantees. Narrow a rule derived from one failure to the conditions that caused it.
- Validate relevant links, metadata, and behavioral invariants. Use realistic bounded examples when a change affects routing or authority; a wording edit does not justify multiplying test runs.
