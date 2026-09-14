# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Read when relevant

- **Domain terminology:** use relevant entries in the root `CONTEXT.md`. If `CONTEXT-MAP.md` exists, follow it to the contexts involved in the task.
- **Architectural decisions:** consult applicable files in `docs/adr/`; in multi-context repos also check `src/<context>/docs/adr/` when that context is affected.

A narrow change that does not depend on domain language or architectural decisions does not require these reads.

If any of these files don't exist, **proceed silently**. Don't flag their absence or suggest creating them upfront. When domain modeling is in scope, the `domain-modeling` skill creates them lazily as terms or decisions are resolved.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
