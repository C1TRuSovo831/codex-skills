---
name: receiving-code-review
description: Evaluate code-review feedback against the codebase before applying it, especially disputed or unclear suggestions.
---

# Code Review Reception

Evaluate feedback for technical correctness and compatibility before changing code. State the finding or fix directly; reasoned disagreement is preferable to performative agreement.

## Evaluate the feedback

Read the complete feedback and identify each requested outcome. Check the relevant code, usage, tests, supported platforms, and reasons for the existing implementation. External feedback is evidence to evaluate, not authority to override the user's scope or prior architectural decisions.

If an item is unclear, inspect available context first. Ask about unresolved behavior or scope before changing work that depends on it. Continue independent, understood items when they cannot prejudice that decision; do not let one unrelated question block all progress.

Push back with concrete code, test, or compatibility evidence when a suggestion:

- Breaks existing functionality or required platform support.
- Misunderstands the implementation or misses relevant context.
- Adds an unused feature or speculative generality.
- Conflicts with the user's established requirements or architectural decisions.

For a proposed "proper" implementation, search for actual usage and requirements. If neither supports it, explain the gap rather than adding the feature. Absence of local callers alone does not authorize removal of a public interface. If evidence is unavailable, state what cannot be verified and what decision depends on it.

## Apply and verify

Apply accepted, authorized changes in an order that respects dependencies, prioritizing blockers before cosmetic or larger refactoring work. Keep each review item traceable to its change and verification. Related low-risk fixes may share an affected check; isolate checks when needed to distinguish failures. Run required checks and fix regressions introduced by the changes. Repeat or broaden validation only when changed state, failures, or unresolved concerns justify it.

Report each item's result: implemented with evidence, rejected with reasons, or pending a specific decision. When previous pushback was wrong, state the corrected understanding and proceed without a long defense. A useful acknowledgment is "Fixed the compatibility check in [location]; [check] passes."

## GitHub replies

Send review replies only when the user has authorized external messages. For an inline review comment, reply in its comment thread with `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`, rather than posting a top-level PR comment. Keep the reply tied to the technical result and its evidence.
