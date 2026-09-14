---
name: find-skills
description: "Discover, compare, and install agent skills when the user asks to find a skill or extend agent capabilities. Ordinary requests to perform a task do not require skill discovery."
---

# Find Skills

Identify the capability the user wants to add, then find a skill whose actual instructions and resources fit that workflow. Search or installation is separate from carrying out the underlying task.

## Search and evaluate

Check already available skills first. Search with the domain plus the specific workflow; use the [skills.sh leaderboard](https://skills.sh/) for broad discovery when useful.

```bash
npx skills find <query>
npx skills find <query> --owner <owner>
```

Before recommending, inspect the skill's source and instructions for task fit, maintenance, dependencies, invocation boundaries, and side effects. Check author provenance, install counts, and repository activity/stars as supporting signals, with counts verified before reporting. Search results and popularity alone do not establish quality. For query examples and the prior adoption heuristics, read [search-examples.md](references/search-examples.md).

Present a short list with each skill's capability, source, relevant tradeoffs, verified adoption information when available, exact install command, and a link to its source or skills.sh page.

## Installation

When the user requests installation or has already authorized it, install the selected skill at the requested scope. A global, noninteractive install uses:

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` selects the user-level scope; `-y` skips CLI prompts. `npx skills add <package>` supports other package sources, and `npx skills update` updates installed skills when that is the task. A discovery request alone is not authorization to install or update everything.

If no match is found, report that result and use general capabilities for any underlying work already requested. For a recurring missing workflow, skill creation remains an option via `npx skills init <name>`; do not make it a prerequisite for completing an ordinary task.
