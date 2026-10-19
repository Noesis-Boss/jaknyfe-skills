---
name: motion-style-studio
description: "Create original short motion-design videos using ten reusable visual recipes: Beat-Synced Pop, Exploded Anatomy, Kinetic Showreel, Mascot Cartoon, Hand-Drawn Story, Pixel Art Scene, Data Explainer, Launch Film, Living Mosaic, and Blender 3D. Use when a user asks for one of these styles, wants a motion-video template, or needs a style brief translated into HyperFrames or Remotion."
metadata:
  author: jaknyfe.zo.computer
---

# Motion Style Studio

Use the ten recipes in `references/ten-styles.md` as original production patterns inferred from the user-supplied Motion Studio reference. They describe broad visual grammar; they do not reproduce that product's source implementation, proprietary assets, or exact animation.

## Workflow

1. Identify the requested style, subject, audience, purpose, platform, aspect ratio, approximate duration, and available assets. Ask only for missing choices that materially affect the result. If the user says “make one,” use a short 15–30 second draft, 9:16 for social unless context points elsewhere, and clearly mark those defaults.
2. Read the matching recipe. Adapt its color, type, imagery, pacing, and sound to the user's brand and content. Do not reuse the demo's cream/orange palette unless requested. Preserve factual claims and supplied brand assets.
3. Choose the renderer from the existing project: use HyperFrames for HTML/GSAP compositions, Remotion for an existing React video project, and `video-use` when editing supplied footage. Read and follow that skill's own rules before implementation. Do not scaffold a new renderer just to apply a recipe.
4. Write a compact style brief and beat map before rendering. Use `assets/motion-brief-template.md`. For footage edits, show the proposed cut/style plan and wait for approval before changing the edit.
5. Build the hero frame before animation. Keep each beat legible at the target aspect ratio, reserve platform safe areas, sync motion to actual audio/transcript timing when available, and use stillness as contrast.
6. Render a short preview, inspect representative frames and audio, correct visible issues, then render the requested deliverable. Never publish or upload as part of rendering.

## Recipe selection

Load only the matching recipe section from `references/ten-styles.md`. For combinations, choose one dominant recipe and borrow at most two supporting traits from another. Keep the result coherent rather than stacking effects.

The recipe names are descriptive labels from the reference image, not a claim that the image exposes the original tool's implementation. Translate them into original work with user-owned or licensed assets.
