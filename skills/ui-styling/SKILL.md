---
name: ui-styling
description: "Implement accessible UI with shadcn/ui and Tailwind, including components, responsive layouts, themes, and dark mode. Also supports canvas-based posters and visual compositions."
argument-hint: "[component or layout]"
license: MIT
metadata:
  author: claudekit
  version: "1.0.0"
---

> Modified by C1TRuSovo831 on 2026-09-14: condensed and reorganized guidance into task-specific references; original license and operational constraints retained.

# UI Styling

Use the existing framework, components, and design tokens. Choose the relevant component/styling reference or canvas workflow; a small edit does not require reinitializing the stack.

## Reference routing

| Task | Read |
|------|------|
| Add or compose forms, navigation, overlays, tables, or feedback components | [shadcn-components.md](references/shadcn-components.md) |
| CSS variables, component variants, theme toggle, or dark mode | [shadcn-theming.md](references/shadcn-theming.md) |
| Keyboard, focus, screen reader announcements, or form accessibility | [shadcn-accessibility.md](references/shadcn-accessibility.md) |
| Layout, spacing, type, color, borders, or utility syntax | [tailwind-utilities.md](references/tailwind-utilities.md) |
| Breakpoints, adaptive layout, or container queries | [tailwind-responsive.md](references/tailwind-responsive.md) |
| Theme tokens, plugins, custom utilities, or variants | [tailwind-customization.md](references/tailwind-customization.md) |
| Canvas poster, brand composition, or visual design system | [canvas-design-system.md](references/canvas-design-system.md) |
| Initial setup or concrete form/layout example | [setup-and-examples.md](references/setup-and-examples.md) |

## Implementation guidance

- Compose accessible primitives; preserve semantic HTML, keyboard behavior, and visible focus. Radix defaults still require correct application labels and focus management.
- Use Tailwind utilities and extract components where repetition warrants it. Preserve TypeScript types in typed projects.
- Apply consistent spacing, typography, and semantic colors. Keep all themed elements consistent across supported light/dark modes.
- Build responsive layouts from the mobile baseline and preserve visual hierarchy through spacing and composition.
- Keep Tailwind class names statically detectable so CSS generation retains the classes used at runtime.

## Utility scripts

Resolve these paths from this skill's directory. Inspect the existing setup before generating configuration.

```bash
python scripts/shadcn_add.py button card dialog
python scripts/tailwind_config_gen.py --colors brand:blue --fonts display:Inter
```

`shadcn_add.py` installs selected components with dependencies; `tailwind_config_gen.py` generates `tailwind.config.js`. Use only the helper needed for the task, with the project's version and configuration format.

## Upstream references

- shadcn/ui: https://ui.shadcn.com/llms.txt
- Tailwind CSS: https://tailwindcss.com/docs
- Radix UI: https://radix-ui.com
- Tailwind UI: https://tailwindui.com
- Headless UI: https://headlessui.com
- v0: https://v0.dev
