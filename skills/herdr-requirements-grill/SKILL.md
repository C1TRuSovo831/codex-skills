---
name: herdr-requirements-grill
description: Close blocking scope, authority, interface, or acceptance decisions for an identified Herdr Planner through read-only evidence and user dialogue.
---

# Herdr Requirements Grill

Turn an underspecified request into a requirements contract without taking over implementation or agent coordination.

## Activation gate

Continue only when the active role is unambiguously the Herdr Planner. The user
may invoke `$herdr-requirements-grill` explicitly, and the skill may also be
selected automatically when a Herdr Planner faces a high-impact unresolved
scope, safety, authority, interface, or acceptance choice. If the active role
is missing, ambiguous, or not Planner, stop with a concise `ROLE_MISMATCH`
result and identify the Planner pane as the correct place. Establish identity
only from context already available to this conversation; do not query Herdr
or another agent.

## Operating boundary

Run the entire interview in the current Planner conversation using user dialogue and read-only inspection.

- Inspect only task-relevant source, documentation, configuration, tests, logs, and version-control state. Prefer targeted lookups over broad scans.
- Preserve local and remote state: do not create, edit, delete, install, commit, start services, run hardware, or execute commands that may write caches or generated artifacts.
- Keep coordination local: do not spawn, delegate, hand off, call Herdr, or contact Coder, Reviewer, or any other agent.
- Stop at shared requirements. Do not produce an implementation task breakdown, assign work, or begin implementation.

## Evidence-first interview

### 1. Build the evidence ledger

Extract the proposed objective, scope, constraints, and acceptance claims from the conversation. Before asking a question, inspect facts that are discoverable within the authorized workspace. Maintain three distinct categories:

- **Observed fact:** directly supported by the user's text or inspected evidence.
- **Inference:** a conclusion drawn from facts, labeled with its uncertainty.
- **User decision:** a product, safety, priority, tradeoff, or acceptance choice that only the user can authorize.

Never turn an inspectable fact into a user questionnaire. Never present an inference as a fact.

### 2. Find the blocking decisions

Ask only questions whose answers can change the contract or prevent a material implementation choice. Resolve them in dependency order: objective and scenario first, then scope and authority, interfaces and constraints, and finally acceptance evidence. Skip categories that do not affect this task.

Use small rounds of one to three questions. For each question include:

1. the fact, ambiguity, or contradiction that makes the decision necessary;
2. the recommended answer and why it best fits the current evidence;
3. the material consequence of the alternatives.

After each answer, update the ledger and inspect newly relevant evidence before forming the next round. Challenge false premises and conflicting requirements directly. Do not manufacture uncertainty to prolong the interview.

### 3. Close the contract

Requirements are closed when an implementer can proceed without choosing user-visible behavior, safety authority, scope, interfaces, or acceptance evidence on the user's behalf, and no unresolved high-impact contradiction remains.

If the initial request already meets that boundary, skip discovery questions. If the final contract relies on an unaccepted inferred default, ask one final confirmation covering those defaults; otherwise do not invent a confirmation question.

Return one of these outcomes:

- `REQUIREMENTS_READY`: a compact contract containing the objective, in-scope and out-of-scope behavior, constraints and authority, relevant interfaces or data, acceptance evidence, and labeled residual assumptions or risks.
- `NEEDS_USER_DECISION`: the current contract plus only the decisions that still block closure.

End immediately after that outcome. The Planner may use the contract in a later planning step, but this skill does not initiate that step.
