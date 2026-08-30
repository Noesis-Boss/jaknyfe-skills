# Design DNA — Bound Book Card-Stack

## Core Metaphor
Bound book with deckle edge and exposed stitching. Individual cards rest on warm parchment pages. One corner of each card is folded — lifts on hover to reveal status and label.

## Color Palette

### Base
| Token | Hex | HSL | Usage |
|-------|-----|-----|-------|
| Parchment | `#F5E6C8` | `38 30% 85%` | Page background |
| Ink | `#1A1A1A` | `20 10% 10%` | Blackletter text |
| Fiber Brown | `#8B7355` | `30 25% 42%` | Organic fiber strands |
| Fiber Ink | `#2C2C2C` | `20 10% 18%` | Dark fiber strands |
| Stitch | `#D4C5A0` | `40 30% 75%` | Exposed binding thread |

### Status Ribbons
| State | Hex | HSL | Icon |
|-------|-----|-----|------|
| Active | `#2E7D32` | `142 76% 36%` | ✓ check |
| Waiting | `#F57C00` | `30 100% 50%` | ◷ clock |
| Done | `#1565C0` | `217 91% 40%` | ✓ check (filled) |

## Typography
- **Primary face:** Victorian ledger blackletter
- **Fallbacks:** `"IM Fell English"`, `"UnifrakturMaguntia"`, `Georgia`, serif
- **Weights:** 400 (body), 700 (emphasis, ribbon labels)
- **Tracking:** +0.02em (ledger feel)
- **Line height:** 1.5

## Spacing & Elevation

### Cards
| State | Shadow | Transform |
|-------|--------|-----------|
| Rest | `0 2px 4px rgba(0,0,0,0.08)` | none |
| Hover | `0 8px 24px rgba(0,0,0,0.15)` | translateY(-2px) |

### Page
- Padding: `24px` (mobile: `16px`)
- Card gap: `16px`
- Max content width: `1200px`
- Paper texture: irregular organic fibers, mixed brown-and-ink

## Motion

### Fold Lift (Hover)
- Duration: `≤120ms`
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` (ease-out)
- Property: `transform` (rotate fold) + `box-shadow`
- Sound metaphor: paper crease

### Parallax (Page-wide)
- Trigger: on-scroll
- Intensity: moderate
- Targets: paper layers AND cards
- Direction: vertical offset, layers move at different speeds

## Components

### Card
- **Rest:** flat surface, folded corner (top-right), soft elevation
- **Hover:** fold lifts with paper crease, reveals text/label + status underneath
- **Depth:** medium stack (panel-on-panel)
- **Content:** title, body, status ribbon

### Ribbon Bookmark
- **Position:** extends from top edge of card
- **Width:** `6–8px`
- **Icon:** micro-version of card content (initials, symbol, or tiny glyph)
- **Color:** maps to status (active/waiting/done)
- **States:** 3 (active, waiting, done)

### Page Surface
- **Background:** warm parchment with visible irregular organic fibers
- **Fiber pattern:** mixed brown-and-ink strands
- **Edge:** deckle (rough torn)
- **Binding:** exposed stitching along spine
- **Ribbon:** single bookmark per page, color-matched to section status

## Do's
- Use exact hex values — no substitutions
- Keep fold animation snappy (≤120ms)
- Apply parallax to both paper and cards
- Use blackletter for headings, clean sans for body if needed
- Maintain deckle edge on all paper surfaces

## Don'ts
- Don't use smooth/rounded corners on paper elements
- Don't add motion to the fold beyond the lift (no bounce, no elastic)
- Don't use more than 3 status colors
- Don't let parallax exceed moderate intensity
- Don't use modern sans-serif for headings
