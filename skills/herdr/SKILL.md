---
name: herdr
description: "Control Herdr panes, terminals, and agents only when the user explicitly requests Herdr and HERDR_ENV=1; not a generic delegation skill."
---

> Modified by C1TRuSovo831 on 2026-09-14: condensed and reorganized guidance into task-specific references; original license and operational constraints retained.

# Herdr

Herdr organizes terminals into workspaces, tabs, and panes, recognizes coding agents running inside panes, and exposes the current session through the `herdr` CLI.

Before issuing any control command, verify that this agent is running inside a Herdr-managed pane:

```bash
test "${HERDR_ENV:-}" = 1
```

If the check fails, say that you are not running inside Herdr and stop. Do not inspect or control the focused Herdr session from outside Herdr.

When the check passes, the `herdr` binary in `PATH` talks to the current session. Use it to inspect neighboring work, create terminal layout, start agents and commands, read output, and wait for state changes.

## Learn the current CLI

The installed binary is the authority for command syntax. Start with:

```bash
herdr --help
```

Then print the relevant command group by running the group without a subcommand:

```bash
herdr agent
herdr pane
herdr workspace
herdr tab
herdr worktree
herdr terminal
herdr notification
herdr integration
herdr session
```

Do not run bare `herdr` for discovery; it launches or attaches the TUI. Do not probe a mutating nested command by omitting arguments. Commands such as `herdr workspace create` are valid with defaults and will execute.

Most control commands return JSON. Read identifiers and state from those responses instead of predicting them.

## Choose the operation

Read the relevant section of [references/operations.md](references/operations.md) before that operation:

- **Layout, identities, or state interpretation:** “Understand layout, panes, and agents” and “Use IDs and caller context”. These define opaque IDs, move semantics, lifecycle states, and caller-safe targeting.
- **Start or coordinate an agent:** “Start and coordinate an agent”, plus the identity sections when needed. This covers layout defaults, readiness, prompts, waits, and blocked UI handling.
- **Run a shell command or inspect output:** “Run an ordinary command in another pane”, plus the identity sections when needed. This covers pane commands, read sources, scrollback limits, and the file-output fallback.

## Safety and coordination rules

- Use `--no-focus` for background work unless the user asked to switch context.
- Use `--current`, an explicit pane ID, or a unique agent name. Do not rely on another client's focused pane.
- Parse IDs from JSON responses. Do not derive them from sidebar order or examples.
- Do not close workspaces, tabs, panes, or sessions you did not create unless the user explicitly asked.
- Never run `herdr server stop` from an active session unless the user explicitly intends to stop the server and its pane processes.
- Never kill the main Herdr process. Use named test sessions for experiments that need an isolated server.
- CLI server errors are JSON on stderr with exit status 1. CLI syntax errors exit with status 2.
