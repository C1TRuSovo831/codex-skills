# Skill mechanics

The skill-specific branch of [writing-for-agents](SKILL.md): frontmatter, invocation policy, and routers. Use the target host's installed skill-creator guidance as the authority for supported fields.

## Codex packaging and invocation

Every skill has `SKILL.md` with YAML `name` and `description`. The description is a concise capability and activation boundary; retain it for both automatic and explicit-only skills. Supporting references, scripts, and assets are optional and should serve a concrete workflow.

Codex invocation policy belongs in `agents/openai.yaml`:

```yaml
policy:
  allow_implicit_invocation: false
```

`false` keeps the skill out of model context by default while allowing explicit `$skill-name` invocation. Automatic selection is allowed by default. Preserve an existing policy; set explicit-only for a new skill only when the user requests that behavior. Sensitivity or required approval for one operation does not by itself justify hiding the entire skill.

`interface` in that file contains optional UI metadata such as `display_name`, `short_description`, and `default_prompt`. A default prompt should mention `$skill-name`. Preserve existing policy, dependencies, and unrelated interface fields during an update: a metadata generator may replace the whole file.

For exact current fields and validation, use the installed `skill-creator` skill and its `references/openai_yaml.md`; resolve paths from its catalog location rather than assuming a fixed installation root.

## Cross-agent compatibility

Some other hosts, including [Claude Code](https://code.claude.com/docs/en/skills#frontmatter-reference), use frontmatter such as `disable-model-invocation: true` and `argument-hint`. Those are host-specific conventions, not Codex's `agents/openai.yaml` invocation policy. Preserve intentional compatibility metadata in an existing cross-agent skill; verify the target host before adding or changing it. A Codex validator may reject those additional frontmatter keys without implying that the compatibility metadata should be deleted.

Distinguish automatic discovery, explicit invocation, and reading a linked file. Invocation policy does not make Markdown inaccessible or prevent a skill from linking to shared reference material. Conversely, a router does not grant permission to bypass explicit-only invocation by automatically executing the hidden skill's workflow.

## Splitting and routers

Create a separate skill when it has a useful independent activation boundary. Otherwise, prefer a supporting reference loaded by the branch that needs it; references do not need their own skill metadata.

A router names available workflows and explains when each applies. An explicit-only router can help the user choose among explicit-only skills, while an automatically discoverable router can guide ordinary selection. Preserve each target's invocation policy and the user's scope. Share common reference material by links and load only the selected branch.
