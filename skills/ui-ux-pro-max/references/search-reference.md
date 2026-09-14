# Search domains, stacks, and examples

Command paths such as `scripts/search.py` are relative to this skill's actual installed directory. Resolve that directory from the loaded `SKILL.md` location and use the corresponding absolute script path when running from a project; installation may be under `~/.codex/skills` or a custom `--dest`.

### Step 3: Supplement with Detailed Searches (as needed)

Use a domain search directly for a focused concern. After generating a design system, add one only for a distinct detail the result does not address:

```bash
python3 scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**When to use detailed searches:**

| Need | Domain | Example |
|------|--------|---------|
| Product type patterns | `product` | `"entertainment social" --domain product` |
| More style options | `style` | `"glassmorphism dark" --domain style` |
| Color palettes | `color` | `"entertainment vibrant" --domain color` |
| Font pairings | `typography` | `"playful modern" --domain typography` |
| Chart recommendations | `chart` | `"real-time dashboard" --domain chart` |
| UX best practices | `ux` | `"error summary validation" --domain ux` |
| Landing structure | `landing` | `"hero social-proof" --domain landing` |
| React/Next.js performance | `react` | `"rerender memo list" --domain react` |
| Native/app interface guidance | `web` | `"accessibilityLabel touch safe-areas" --domain web` |
| Icon suggestions | `icons` | `"decorative icon aria hidden" --domain icons` |
| Individual Google Fonts | `google-fonts` | `"variable sans serif" --domain google-fonts` |
| GSAP animation snippets | `gsap` | `"scroll reveal stagger" --domain gsap` |

### Step 4: Stack Guidelines

Get implementation-specific best practices for the user's stack:

```bash
python3 scripts/search.py "<keyword>" --stack <stack>
```

Example for a known React Native implementation concern:

```bash
python3 scripts/search.py "virtualized list" --stack react-native
```

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `gsap` | GSAP animation skeletons by intensity tier | scroll reveal, stagger, magnetic cursor, page transition |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | App interface guidelines (iOS/Android/React Native) | accessibilityLabel, touch targets, safe areas, Dynamic Type |
| `icons` | Icon recommendations with import code | arrow, navigation, lucide, phosphor |
| `google-fonts` | Individual Google Fonts lookup | sans serif, monospace, japanese, variable font, popular |

### Available Stacks

`react`, `nextjs`, `vue`, `svelte`, `astro`, `swiftui`, `react-native`, `flutter`, `nuxtjs`, `nuxt-ui`, `html-tailwind`, `shadcn`, `jetpack-compose`, `threejs`, `angular`, `laravel`, `javafx`, `wpf`, `winui`, `avalonia`, `uno`, `uwp`

**JavaFX enterprise examples:**

```bash
python3 scripts/search.py "atlantafx primer enterprise theme" --stack javafx
python3 scripts/search.py "enterprise tableview density permission" --stack javafx
```

---

## Example Workflow

**User request:** "Make an AI search homepage。"

### Step 1: Analyze Requirements
- Product type: Tool (AI search engine)
- Target audience: C-end users looking for fast, intelligent search
- Style keywords: modern, minimal, content-first, dark mode
- Stack: Next.js, detected from the project

### Step 2: Generate Design System

```bash
python3 scripts/search.py "AI search tool modern minimal" --design-system -p "AI Search"
```

**Output:** Complete design system with pattern, style, colors, typography, effects, and anti-patterns.

### Step 3: Supplement with Detailed Searches (as needed)

```bash
# Get style options for a modern tool product
python3 scripts/search.py "minimalism dark mode" --domain style

# Get UX best practices for search interaction and loading
python3 scripts/search.py "search loading animation" --domain ux
```

### Step 4: Stack Guidelines

```bash
python3 scripts/search.py "streaming suspense" --stack nextjs
```

**Then:** Synthesize design system + detailed searches and implement the design.

---

## Output Formats

The `--design-system` flag supports two output formats:

```bash
# ASCII box (default) - best for terminal display
python3 scripts/search.py "fintech crypto" --design-system

# Markdown - best for documentation
python3 scripts/search.py "fintech crypto" --design-system -f markdown
```

---
