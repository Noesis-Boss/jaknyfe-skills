# Ten motion recipes

These are original, adaptable recipes based on the visible labels and previews in the supplied Motion Studio GIF. The image does not expose source code or exact parameters. Treat each recipe as creative direction, then fit it to the brief and renderer.

## 1. Beat-Synced Pop

**Feel:** bright, quick, rhythmic. **Best for:** short hooks, product moments, celebratory announcements.

- Build each beat around one readable word, icon, or object. Use bold rounded display type, a simple high-contrast palette, and a clean central safe area.
- Use a short scale-and-settle entrance on musical accents, with small shape pops as secondary motion. Hold the key message between accents; do not animate every element continuously.
- End on a stable, readable hero frame. Use a percussive sound only when it supports the supplied track.
- **Avoid:** random bounce, unreadable word flashes, and pretending the animation is beat-synced when no timing data was inspected.

## 2. Exploded Anatomy

**Feel:** precise, dimensional, curious. **Best for:** explaining a mechanism, interface, product, or system.

- Start with the intact object or diagram. Separate a few meaningful layers along clear axes, label each layer, then reassemble to show the relationship.
- Use restrained perspective, depth, and parallax; keep labels attached to their parts. Establish a consistent lighting direction and one accent color for the active component.
- Pace moves as reveal → inspect → reassemble. Use callouts only for facts supported by the source material.
- **Avoid:** implying real internal construction from a decorative illustration, excessive rotation, or separating so many parts that the whole becomes unclear.

## 3. Kinetic Showreel

**Feel:** confident, editorial, energetic. **Best for:** portfolios, product capabilities, event openers.

- Treat the video as a sequence of distinct visual ideas linked by one transition grammar. Use large type, cropped imagery, graphic shapes, and deliberate changes in scale.
- Let each shot make one claim or impression. Alternate fast passages with brief holds; use match cuts, directional wipes, or shape handoffs to preserve continuity.
- Close with the strongest image or a concise title card. Sync cuts to verified beats when music is supplied.
- **Avoid:** a pile of unrelated effects, unsupported “viral” or performance claims, and transitions that obscure the message.

## 4. Mascot Cartoon

**Feel:** friendly, expressive, playful. **Best for:** approachable brands, onboarding, simple stories.

- Give the character a small, repeatable set of readable poses and reactions. Use clean silhouettes, limited colors, soft staging, and clear eye-line or gesture cues.
- Animate anticipation → action → settle. Keep secondary motion (ears, tail, props) subtle and delayed so it reinforces the main action.
- Let the mascot demonstrate the point instead of decorating every scene. Keep text short and high contrast.
- **Avoid:** copying a known character, uncontrolled squash/stretch, or expressions that conflict with the message.

## 5. Hand-Drawn Story

**Feel:** personal, tactile, intimate. **Best for:** anecdotes, explainers, founder stories, reflective content.

- Use a paper-like field, limited ink palette, simple line illustrations, and handwritten accents only where readability allows.
- Reveal lines as if drawn, use gentle page or panel transitions, and let objects enter as story beats. Preserve slight organic irregularity without making text wobble.
- Keep narration and drawing aligned; leave enough hold time to read each panel.
- **Avoid:** fake handwriting for long copy, noisy paper textures, or presenting illustrative scenes as documentary evidence.

## 6. Pixel Art Scene

**Feel:** nostalgic, game-like, structured. **Best for:** playful tech, progress journeys, retro-themed launches.

- Set a deliberate pixel grid and small palette. Use tile-based environments, sprite-like objects, and crisp nearest-neighbor scaling.
- Move characters or objects in clear steps; use limited-frame loops and scene changes that feel like level progression. Keep UI text on a separate, highly legible layer.
- Use pixelated transitions only at scene boundaries, with a clean hold on key information.
- **Avoid:** mixing inconsistent pixel sizes, blurry scaling, and decorative game HUDs that imply real product functionality.

## 7. Data Explainer

**Feel:** clear, evidence-led, informative. **Best for:** research findings, comparisons, metrics, how-it-works content.

- One chart or relationship per beat. State the takeaway, show the data source/context, then animate the relevant marks. Keep labels, units, and baselines visible.
- Use calm transitions, progressive emphasis, and restrained color. Animate values only when the underlying values are supplied and verified.
- Provide a source note in-frame or end card when the data needs attribution. Avoid implying causation from correlation.
- **Avoid:** invented data, misleading axes, decorative chart motion, and tiny labels.

## 8. Launch Film

**Feel:** cinematic, composed, anticipatory. **Best for:** introducing a product, feature, event, or major reveal.

- Structure as atmosphere → hint → reveal → concrete benefit → end card. Use a small number of deliberate shots, controlled light, and purposeful camera movement.
- Hold back the hero object until the reveal. Let sound and negative space create anticipation; keep claims specific and supplied by the user.
- Use a consistent grade and a clean final frame with the product or call to action.
- **Avoid:** vague hype, fake product capabilities, relentless lens effects, or dramatic pacing that leaves no time to understand the offer.

## 9. Living Mosaic

**Feel:** layered, organic, evolving. **Best for:** community, many stories, creative collections, abstract transitions.

- Compose a field from a small set of tiles, images, or particles that can grow, merge, or rearrange. Keep an identifiable focal area and coherent palette.
- Let motion travel through the field in waves or clusters. Use depth sparingly and preserve a quiet interval for the main message.
- If using portraits or customer work, use only supplied/authorized media and avoid suggesting people endorse a product without permission.
- **Avoid:** indiscriminate collage, excessive detail, and motion that makes the focal subject hard to find.

## 10. Blender 3D

**Feel:** tactile, sculptural, spatial. **Best for:** hero objects, abstract product metaphors, dimensional logo or title work.

- Use a simple stage, deliberate camera path, consistent key/fill/rim lighting, and one material idea. Make depth and silhouette readable at the delivery size.
- Choose the renderer already available in the project: rendered 3D passes can be composited in HyperFrames; existing React scenes can use the project's Remotion/Three.js path. If neither is present, first propose a 2D depth illusion or a separate Blender render workflow rather than installing software without need.
- Keep camera motion smooth and reserve a stable hold for the message.
- **Avoid:** fake 3D that distorts a real product, uncontrolled orbiting, and costly geometry when a simple form works.

## Fill-in direction prompt

> Create an original [duration] motion video in the [recipe] visual grammar for [audience]. Its single takeaway is [message]. Use [assets/data] and [brand constraints]. Deliver [aspect ratio/platform]. Build a [number]-beat sequence: [beat purpose per segment]. Keep [must-remain-readable element] legible, use [motion quality] with [hold/pacing], and avoid [style-specific exclusions]. Do not invent product features, statistics, testimonials, or source attributions.
