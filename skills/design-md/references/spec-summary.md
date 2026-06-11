# DESIGN.md Format Reference

## Quick Start

```bash
# Create a minimal DESIGN.md
bun run /home/workspace/Skills/design-md/scripts/scaffold.ts --name "My Project" --minimal > DESIGN.md

# Grab an existing brand's design system
bun run /home/workspace/Skills/design-md/scripts/fetch-brand.ts notion > DESIGN.md

# Validate against the spec
npx @google/design.md lint DESIGN.md
```

## Canonical Section Order

| # | Section | Aliases |
|---|---------|---------|
| 1 | Overview | Brand & Style |
| 2 | Colors | |
| 3 | Typography | |
| 4 | Layout | Layout & Spacing |
| 5 | Elevation & Depth | Elevation |
| 6 | Shapes | |
| 7 | Components | |
| 8 | Do's and Don'ts | |

## Token Schema

```yaml
version: alpha          # optional
name: <string>
description: <string>   # optional
colors:
  <name>: <hex>         # e.g., "#1A1C1E"
typography:
  <name>:
    fontFamily: <string>
    fontSize: <px|rem|em>
    fontWeight: <number>
    lineHeight: <number|px|rem|em>
    letterSpacing: <px|em>
rounded:
  <level>: <px|rem>     # e.g., sm: 4px
spacing:
  <level>: <px|rem|number>
components:
  <name>:
    backgroundColor: <hex|{ref}>
    textColor: <hex|{ref}>
    typography: "{typography.name}"
    rounded: "{rounded.level}"
    padding: <px|rem>
    border: <css>
```

## Token Types

| Type | Format | Example |
|------|--------|---------|
| Color | `#` + 6-char hex (SRGB) | `"#1A1C1E"` |
| Dimension | number + px/em/rem | `48px`, `-0.02em` |
| Reference | `{path.to.token}` | `{colors.primary}` |
| Typography | object with font props | See schema above |

## Component Properties

Valid sub-properties: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`, `border`.

Variants (hover, active, pressed) are separate component entries with related keys.

## The 3 Failure Modes DESIGN.md Prevents

1. **Bootstrap Default** — Without design context, agents converge on white backgrounds, blue buttons, gray text, 4px radius, system fonts.
2. **Color Roulette** — Reasonable colors per element that don't form a system. Blue shifts between pages, red means error on one page and decoration on another.
3. **Style Drift** — Same agent produces different designs in different conversations. Rounded corners Monday, square Tuesday.

## Token Budget Strategy

| Sections | ~Tokens | Best for |
|----------|---------|----------|
| 4 (Overview, Colors, Components, Do's/Don'ts) | ~8K | Tight context budgets, rapid prototyping |
| 6 (+ Typography, Shapes) | ~15K | Most projects — covers high-impact failures |
| 8 (all sections) | ~22K-30K | Production apps needing full consistency |

## CLI Reference

```bash
npx @google/design.md lint DESIGN.md     # Validate
npx @google/design.md diff v1 v2          # Compare versions
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css
npx @google/design.md export --format json-tailwind DESIGN.md > tailwind.config.json
npx @google/design.md spec                # Output the full format spec
```

## Sources

- Spec repo: https://github.com/google-labs-code/design.md
- Brand collection: https://github.com/VoltAgent/awesome-design-md
- Google Stitch: https://stitch.withgoogle.com/
