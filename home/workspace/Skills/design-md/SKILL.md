---
name: design-md
description: Create, validate, and manage DESIGN.md design system files for AI agents. Use when building any UI (websites, apps, components) to ensure visual consistency across sessions — prevents Bootstrap Default, Color Roulette, and Style Drift. Also use when the user asks to "create a design system", "set up a DESIGN.md", "get a brand's design tokens", or when starting a new frontend project that needs consistent styling.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# DESIGN.md — AI-Native Design System Files

DESIGN.md is a markdown-based format for describing visual identity to AI coding agents. Created by Google and open-sourced under Apache 2.0, it gives agents a persistent, structured understanding of a design system — preventing the three failure modes that plague AI-generated UI:

1. **Bootstrap Default** — every page looks like unthemed Tailwind
2. **Color Roulette** — inconsistent color choices across pages
3. **Style Drift** — different sessions produce different designs for the same app

## When to Use

Activate this skill when:
- Starting a new frontend project (website, app, dashboard, landing page)
- The user asks to "create a design system" or "set up a DESIGN.md"
- The user wants to replicate a known brand's look (Stripe, Notion, Linear, etc.)
- You're about to build UI and want consistency across sessions
- The user complains about visual inconsistency in AI-generated pages

**Relationship with `frontend-design`:** The `frontend-design` skill handles creative execution and aesthetic choices. DESIGN.md provides the *persistent token layer* — exact colors, typography scales, spacing, and component specs that survive across conversations. Use both together: DESIGN.md for the system, `frontend-design` for the implementation.

## How It Works

A DESIGN.md file has two layers:
1. **YAML front matter** — Machine-readable design tokens (colors, typography, spacing, rounded corners, components)
2. **Markdown body** — Human-readable rationale organized into 8 canonical sections

The 8 sections (in order):
1. **Overview** — brand personality, emotional intent
2. **Colors** — palette with semantic roles (primary, secondary, accent, error, neutral, surface)
3. **Typography** — font families, size scale, weights, line heights, letter spacing
4. **Layout** — grid system, max-width, spacing scale, whitespace philosophy
5. **Elevation & Depth** — shadow system, layering, z-index rules
6. **Shapes** — border-radius scale, corner treatments
7. **Components** — button variants, cards, inputs, chips with exact token references
8. **Do's and Don'ts** — explicit negative constraints ("never use pill buttons", "never border-radius above 8px")

## Key Principle

> "The models aren't bad at design. They're bad at design *memory*."

The same constraints that make human design teams consistent (color roles, spacing scales, typography hierarchies, do's and don'ts) make AI agents consistent too. DESIGN.md encodes these in the one format LLMs already understand: structured markdown.

## Workflow

### Path A: Use an Existing Brand

```bash
# List available brands
bun run /home/workspace/Skills/design-md/scripts/fetch-brand.ts --list

# Fetch a specific brand's DESIGN.md
bun run /home/workspace/Skills/design-md/scripts/fetch-brand.ts stripe > DESIGN.md
```

### Path B: Scaffold from Scratch

```bash
# Interactive scaffold (asks questions about the design direction)
bun run /home/workspace/Skills/design-md/scripts/scaffold.ts --name "My Project" > DESIGN.md

# Minimal scaffold (4 essential sections only)
bun run /home/workspace/Skills/design-md/scripts/scaffold.ts --name "My Project" --minimal > DESIGN.md
```

### Path C: Validate an Existing File

```bash
npx @google/design.md lint DESIGN.md
```

### What to Put in the Project

Place DESIGN.md in the project root, next to CLAUDE.md or AGENTS.md. The agent picks it up automatically. For Zo-specific projects, reference it from AGENTS.md:

```markdown
# AGENTS.md
Design system: See DESIGN.md for colors, typography, spacing, and component specs.
Always consult DESIGN.md before generating any UI.
```

## Starting Minimal

If full 8-section file is too much context, start with these 4 (they cover the highest-impact failure modes):
1. **Overview** — 2 sentences describing the feel
2. **Colors** — primary, accent, error, neutral with roles
3. **Components** — button variants and card specs at minimum
4. **Do's and Don'ts** — 5 rules the agent should never break

## Limitations (Honest)

- **Token cost**: Full file ≈ 30K tokens per query. Trim to 4 sections for tight budgets.
- **No runtime enforcement**: DESIGN.md is guidance, not a linter. The agent can still violate rules.
- **Design drift**: Manual updates needed when live CSS changes. No auto-sync from Figma/CSS.
- **Spec is alpha**: Missing animation tokens, icon standards, accessibility checking.
- **Not a replacement for `frontend-design`**: DESIGN.md provides the *system*, not the creative execution.

## Reference

- Spec: https://github.com/google-labs-code/design.md
- Brand collection (423+): https://github.com/VoltAgent/awesome-design-md
- Google Stitch (extract from URL): https://stitch.withgoogle.com/
- CLI: `npx @google/design.md lint|diff|export|spec`
