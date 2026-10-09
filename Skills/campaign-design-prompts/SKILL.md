---
name: campaign-design-prompts
description: Create polished prompts and finished visual assets for social posts, event flyers, product advertisements, infographics, luxury campaigns, and YouTube thumbnails. Use when the user asks for professional advertising artwork, a design prompt, or one of these seven formats.
metadata:
  author: jaknyfe.zo.computer
---

# Campaign Design Prompts

Turn a brief into a restrained, production-ready visual design. Treat supplied copy, facts, brand colors, product identity, and dimensions as constraints. Do not invent claims, statistics, prices, event details, logos, QR codes, awards, or packaging text.

## Route the format

- **Social post** — 1080 × 1350 px, 4:5. Headline first, visual second, supporting copy and CTA last.
- **Event flyer** — 1080 × 1350 px, 4:5. Event name first, attraction second, details third.
- **Product advertisement** — 1080 × 1350 px, 4:5. Product is dominant; preserve realistic proportions, labels, materials, shadows, and identity.
- **Infographic** — 1080 × 1350 px, 4:5. Title, key idea, main information, then supporting details. Use visual aids only when they clarify supplied information.
- **Luxury campaign** — 1080 × 1350 px, 4:5. Let imagery, proportion, typography, materials, and restraint communicate luxury.
- **YouTube thumbnail** — 1280 × 720 px, 16:9. One focal element, 2–5 words, and at most one supporting visual.

If the user asks for a flyer without specifying the type, use the event-flyer route and request only the missing event fields.

## Build the prompt

Normalize every brief into this order:

1. Format and exact dimensions.
2. Audience and intended action.
3. Exact text to render, preserving spelling and punctuation.
4. Primary visual subject and realism requirements.
5. Layout hierarchy and focal point.
6. Palette, typography, materials, lighting, camera direction, and background.
7. Relevant negative constraints and quality checks.

Use an editorial grid, consistent margins, deliberate alignment, generous negative space, and no more than two font families. Prefer clean sans-serif type; for luxury work, pair one elegant serif with one neutral sans-serif. Make text readable at target size and keep it away from busy imagery.

Describe the output as a professional advertising campaign with meticulous art direction, realistic materials and anatomy, coherent lighting, precise spacing, and controlled hierarchy. State the exact canvas size. Keep the prompt concise enough that the model prioritizes composition.

## Universal exclusions

Append relevant exclusions, including: no Canva-style template look, random shapes, clutter, unnecessary ornaments, overdone gradients, glass effects, glow effects, fake logos, fake QR codes, dummy data, tiny text, generic stock-photo treatment, distorted anatomy, invented claims, or illegible copy.

## Format-specific checks

- **Social and event:** verify every supplied text field is present once; use three clear hierarchy levels and one focal point.
- **Product:** verify the product remains recognizable; prohibit distorted packaging, fake labels, ingredient explosions, cheap sale badges, fake awards, and exaggerated reflections.
- **Infographic:** use only supplied facts and numbers; remove any chart or icon that does not improve comprehension; never guess missing data.
- **Luxury:** avoid gold gradients, marble clichés, crowns, diamonds, shine, ornate frames, and decorative excess.
- **Thumbnail:** test legibility at small size; avoid shocked expressions, emoji, explosions, excessive arrows, circles, and saturation.

## Execution

For a finished image, use the image-generation workflow available in the current environment. If the user asks for philosophy-led artwork or a downloadable PNG/PDF, follow `canvas-design`. If the user asks to browse or fill a reusable template, use the connected design-template workflow instead of inventing a template search result.

Inspect every generated result. Revise if text is missing or garbled, hierarchy is unclear, the subject is distorted, dimensions are wrong, contrast is weak, or the composition violates the exclusions. Visual work is complete only after the rendered asset passes inspection.

When the brief is incomplete, ask for the smallest missing set of fields. Never fabricate brand identity, event information, product claims, or statistics.
