---
name: hatch-pet
description: Create, repair, validate, preview, and package Zo-compatible animated pet spritesheets from character art, screenshots, generated images, or visual references. Use when a user wants to hatch a Zo pet or create a custom animated pet asset with an 8x9 atlas, transparent unused cells, row-by-row animation prompts, QA contact sheets, preview videos, and pet.json packaging. This skill uses Zo image generation tools for visual generation and bundled scripts for deterministic spritesheet assembly.
---
# Hatch Pet

## Overview

Create a Zo-compatible animated pet from a concept, one or more reference images, or both. This skill owns pet-specific prompt planning, animation rows, frame extraction, atlas geometry, QA, previews, and packaging. It delegates visual generation to Zo image tools.

User-facing inputs are optional. If the user omits a pet name, infer one from the concept or reference filenames; if that is not possible, choose a short appropriate name. If the user omits a description, infer one from the concept or references. If the user omits reference images, generate the base pet from text first, then use that base as the canonical reference for every animation row.

## Generation Delegation

Use Zo's image generation tools for all normal visual generation:

- Use `generate_image` for a text-only base pet when no reference image exists.
- Use `edit_image` when the job has reference images, a canonical base image, a layout guide, or any other grounding input.
- Save Zo-generated candidates outside the run directory, preferably under `/home/workspace/Images/hatch-pet/generated/` or the current conversation workspace, then record the selected original output with `file record_zo_image_result.py`.
- Never save Zo-generated row candidates under the run's `references/`, `references/layout-guides/`, `prompts/`, `qa/`, or other input/derived-output folders. `references/layout-guides/` is input-only. A visual candidate copied there does not count as a completed job until the original Zo output has been recorded through `file record_zo_image_result.py` and `file zo-image-jobs.json` shows that job as `complete`.

Do not call provider-specific image helpers or direct image APIs for the normal path. Zo's media tools are the visual generation layer; this skill's scripts are for deterministic work only: preparing prompts and manifests, ingesting selected Zo image outputs, extracting frames, validating rows, composing the final atlas, creating QA media, and packaging.

Hard boundary: do not create, draw, tile, warp, mirror, or synthesize pet visuals with local Python/Pillow scripts, SVG, canvas, HTML/CSS, or other code-native art as a substitute for Zo-generated images. For a normal pet run, expect up to 10 visual generation jobs: 1 base pet plus 9 row-strip jobs. The only exception is `running-left`, which may be derived by mirroring `running-right` only after `running-right` has been generated, visually inspected, and explicitly approved as safe to mirror. If mirroring is not appropriate, generate `running-left` as a normal grounded Zo image job. If the required image generation is too expensive, blocked, or unavailable, stop and explain the blocker instead of fabricating row strips locally.

Do not mark visual jobs complete by editing `file zo-image-jobs.json`, copying files into `decoded/`, or writing helper scripts that populate row outputs. Use `file record_zo_image_result.py` for selected Zo-generated outputs. The deterministic scripts may only process already-generated visual outputs.

Only the base job may be prompt-only. Every row-strip job generated through Zo image tools must use the input images listed in `file zo-image-jobs.json`, including the canonical base reference created after the base job is recorded.

## Zo Digital Pet Style

Default pet art should match Zo's digital-pet style: small pixel-art-adjacent mascots with compact chibi proportions, chunky readable silhouettes, thick dark 1-2 px outlines, visible stepped/pixel edges, limited palettes, flat cel shading, simple expressive faces, and tiny limbs. Even if the reference art is more detailed, complex or realistic, the generated pet should be simplified into this style.

Do NOT generate polished illustration, painterly rendering, anime key art, 3D rendering, glossy app-icon treatment, realistic fur or material texture, soft gradients, high-detail antialiasing, and complex tiny accessories. References that are more detailed than this should be simplified into the house style before row generation.

## Transparency And Effects

Pet rows are processed into transparent 192x208 cells, so every generated pixel must either belong to the pet sprite or be cleanly removable chroma-key background. Prefer pose, expression, and silhouette changes over decorative effects.

Allowed effects must satisfy all of these conditions:

- The effect is state-relevant and helps explain the animation.
- The effect is physically attached to, touching, or overlapping the pet silhouette, not floating nearby.
- The effect is inside the same frame slot as the pet and does not create a separate sprite component.
- The effect is opaque, hard-edged, pixel-style, and uses non-chroma-key colors.
- The effect is small enough to remain readable at 192x208 without clutter.

Examples of allowed effects: a tear touching the face, a small smoke puff touching the box or head, or tiny stars overlapping the pet during a failed/dizzy reaction.

Avoid these by default because they usually break transparent-background cleanup or component extraction:

- wave marks, motion arcs, speed lines, action streaks, afterimages, blur, or smears
- detached stars, loose sparkles, floating punctuation, floating icons, falling tear drops, separated smoke clouds, or loose dust
- cast shadows, contact shadows, drop shadows, oval floor shadows, floor patches, landing marks, impact bursts, glow, halo, aura, or soft transparent effects
- text, labels, frame numbers, visible grids, guide marks, speech bubbles, thought bubbles, UI panels, code snippets, checkerboard transparency, white backgrounds, black backgrounds, or scenery
- chroma-key-adjacent colors in the pet, prop, effects, highlights, or shadows
- stray pixels, disconnected outline bits, speckle/noise, cropped body parts, overlapping poses, or any pose that crosses into a neighboring frame slot

State-specific guidance:

- `waving`: show the wave through paw pose only. Do not draw wave marks, motion arcs, lines, sparkles, or symbols around the paw.
- `jumping`: show vertical motion through body position only. Do not draw shadows, dust, landing marks, impact bursts, bounce pads, or floor cues.
- `failed`: tears, attached smoke puffs, or attached stars are allowed if they obey the allowed-effects rules; do not use red X marks, floating symbols, detached smoke, detached stars, or separate tear droplets.
- `review`: show focus through lean, blink, eyes, head tilt, or paw position. Do not add magnifying glasses, papers, code, UI, punctuation, or symbols unless that prop already exists in the base pet identity.
- `running-right`, `running-left`, and `running`: show locomotion through body, limb, and prop movement only. Do not draw speed lines, dust clouds, floor shadows, or motion trails.

## Pet Naming

Ask the user for a pet name when they have not provided one and only if the conversation naturally allows it. If asking would slow down a direct execution request, choose a short appropriate name from the pet concept, reference image, or personality, then use that name consistently as the display name and as the source for the package folder slug.

Good built-in style examples:

- Zo - The original Zo companion.
- Dewey - A tidy duck for calm workspace days.
- Fireball - Hot path energy for fast iteration.
- Rocky - A steady rock when the diff gets large.
- Seedy - Small green shoots for new ideas.
- Stacky - A balanced stack for deep work.
- BSOD - A tiny blue-screen gremlin.
- Null Signal - Quiet signal from the void.

## Visible Progress Plan

For every pet run, keep a visible checklist so the user can see where the work is up to. Create the checklist before starting, keep one step active at a time, and update it as each step finishes.

Before creating the checklist, establish the pet name when possible. Use the user-provided name when available; otherwise infer a short appropriate name from the concept or references. If the name is too long, not settled, or not appropriate for a friendly checklist, use `your pet` instead.

Use this checklist for a normal pet run, replacing `<Pet>` with the pet's name or `your pet`:

1. Getting `<Pet>` ready.
2. Imagining `<Pet>`'s main look.
3. Picturing `<Pet>`'s poses.
4. Hatching `<Pet>`.

What each step means:

- `Getting <Pet> ready.` Choose or confirm the pet name, description, source images, and working folder.
- `Imagining <Pet>'s main look.` Generate the pet's main reference image. This is required for new pets, even when the user does not provide an image, because it becomes the visual source of truth.
- `Picturing <Pet>'s poses.` Create the pose rows, starting with `idle` and `running-right` to confirm the pet still looks consistent. Only mirror `running-left` if `running-right` clearly works when flipped.
- `Hatching <Pet>.` Turn the approved poses into the final pet files, review the contact sheet, previews, and validation results, fix any broken parts, save `file pet.json` and `file spritesheet.webp` into the pet folder, then tell the user where the pet and QA files were saved.

Only mark a step complete when the real file, image, or decision exists. If this is just a repair run, start from the first relevant step instead of restarting the whole checklist.

## Default Workflow

1. Prepare a pet run folder and Zo image job manifest:

```bash
SKILL_DIR="/home/workspace/Skills/hatch-pet"
python "$SKILL_DIR/scripts/prepare_pet_run.py" 
  --pet-name "<Name>" 
  --description "<one sentence>" 
  --reference /absolute/path/to/reference.png 
  --output-dir /absolute/path/to/run 
  --pet-notes "<stable pet description>" 
  --style-notes "<style notes>" 
  --force
```

All arguments above are optional except any flags needed to express user constraints. For text-only requests, pass the concept through `--pet-notes` and omit `--reference`; `file prepare_pet_run.py` will infer a name, description, chroma key, and output directory as needed. If `--output-dir` is omitted, runs are created under `/home/workspace/Images/hatch-pet/runs/`.

2. Inspect the next ready Zo image jobs:

```bash
python "$SKILL_DIR/scripts/pet_job_status.py" --run-dir /absolute/path/to/run
```

If `complete` is less than `total`, the pet is not done. Continue generating and recording every ready/pending row job before finalization. Do not package, accept, or present the run as complete while `file pet_job_status.py` still reports pending or ready row jobs.

3. For each ready job, generate the visual with Zo media tools:

- read the prompt file listed in `file zo-image-jobs.json`
- attach every input image listed for the job, with its role label
- use `generate_image` only for prompt-only jobs
- use `edit_image` for grounded jobs with references, canonical base images, layout guides, or repair context

The base job must complete first. If user references exist, the base job uses them. If no references exist, the base job may be prompt-only. After recording the base, `file record_zo_image_result.py` writes `file decoded/base.png` and `file references/canonical-base.png`; all row jobs use the original references if present plus those canonical base images.

`file prepare_pet_run.py` also creates 9 row-specific layout guide images under `references/layout-guides/`, one per animation state. Row jobs attach the matching guide as a layout-only input so the model can follow the correct frame count, spacing, centering, and safe padding. Treat these guides as invisible construction references: the generated row strip must not include visible boxes, borders, center marks, labels, guide colors, or the guide background.

When generating row strips, keep the identity lock in the row prompt authoritative: do not redesign the pet, and preserve the same head shape, face, markings, palette, prop, outline weight, body proportions, and silhouette. A row that looks like a related but different pet is failed even if the deterministic geometry QA passes.

Generate and record `running-right` before deciding how to complete `running-left`. Inspect `running-right` against the base and references. If the pet is visually symmetric enough that a horizontal mirror preserves identity, prop placement, handedness, markings, lighting, text-free details, and direction semantics, derive `running-left` with:

```bash
python "$SKILL_DIR/scripts/derive_running_left_from_running_right.py" 
  --run-dir /absolute/path/to/run 
  --confirm-appropriate-mirror 
  --decision-note "<why mirroring preserves this pet's identity>"
```

If there is any asymmetric side-specific marking, readable text, non-mirrored logo, handed prop, one-sided accessory, lighting cue, or direction-specific pose that would become wrong when flipped, do not mirror. Generate `running-left` with Zo image tools using its row prompt and all listed grounding images, including `file decoded/running-right.png` as a gait reference.

After selecting a Zo-generated output for a job, ingest it:

```bash
python "$SKILL_DIR/scripts/record_zo_image_result.py" 
  --run-dir /absolute/path/to/run 
  --job-id <job-id> 
  --source /absolute/path/to/zo-generated-output.png
```

This copies the image to the exact decoded path expected by the deterministic pipeline and records source metadata in `file zo-image-jobs.json`.

### Finalization And Packaging Contract

A normal hatch-pet run is not complete when row images exist in `decoded/`. It is complete only after the deterministic finalization pipeline has succeeded and the package directory exists.

Before finalizing, run `file pet_job_status.py` and require `complete == total`, `ready == 0`, and `blocked == 0`. If any job is still pending, ready, blocked, failed, or missing from `decoded/`, continue generation/repair instead of finalizing.

Run finalization with:

```bash
python "$SKILL_DIR/scripts/finalize_pet_run.py" 
  --run-dir /absolute/path/to/run
```

`file finalize_pet_run.py` is the canonical final-package command. It must be used instead of manually assembling the package. It runs the deterministic pipeline in this order:

1. `file extract_strip_frames.py` — extracts the completed decoded row strips into per-state `192x208` frames.
2. `file inspect_frames.py` — writes `file qa/review.json` and blocks on geometry/component errors.
3. `file compose_atlas.py` — builds `file final/spritesheet.png` and `file final/spritesheet.webp` as the full `1536x1872` 8x9 Zo pet atlas.
4. `file validate_atlas.py` — writes `file final/validation.json` and verifies used/unused cells, transparency, dimensions, and row/frame counts.
5. `file make_contact_sheet.py` — writes `file qa/contact-sheet.png` for visual row-by-row review.
6. `file render_animation_videos.py` — writes one preview MP4 per state under `file qa/videos/`.
7. `file package_custom_pet.py` — writes the installable package under `${ZO_PETS_HOME:-/home/workspace/Images/hatch-pet/pets}/<pet-name>/`.

Do not call the pet finished until all of these artifacts exist:

- `file final/spritesheet.webp`
- `file final/validation.json`
- `file qa/contact-sheet.png`
- `file qa/review.json`
- `file qa/videos/` with per-state previews
- `file ${ZO_PETS_HOME:-/home/workspace/Images/hatch-pet/pets}/<pet-name>/pet.json`
- `file ${ZO_PETS_HOME:-/home/workspace/Images/hatch-pet/pets}/<pet-name>/spritesheet.webp`

After finalization, read `file final/validation.json` and `file qa/review.json`; errors are blockers and warnings require visual inspection. Also inspect `file qa/contact-sheet.png` and enough preview videos to confirm every state reads as the same pet. If anything fails, repair the affected row, re-record it with `file record_zo_image_result.py --force`, and rerun `file finalize_pet_run.py`.

4. When all jobs are complete, finalize:

```bash
python "$SKILL_DIR/scripts/finalize_pet_run.py" 
  --run-dir /absolute/path/to/run
```

Expected output:

```text
run/
  pet_request.json
  zo-image-jobs.json
  prompts/
  decoded/
  frames/frames-manifest.json
  final/spritesheet.png
  final/spritesheet.webp
  final/validation.json
  qa/contact-sheet.png
  qa/review.json
  qa/run-summary.json
  qa/videos/*.mp4
```

Package output is written outside the run directory by default:

```text
${ZO_PETS_HOME:-/home/workspace/Images/hatch-pet/pets}/<pet-name>/
  pet.json
  spritesheet.webp
```

Review `file qa/contact-sheet.png`, `file qa/review.json`, `file final/validation.json`, and `qa/videos/` before accepting the pet.

Deterministic validation is necessary but not sufficient. Before calling the pet done, visually inspect the contact sheet for identity consistency. Block acceptance if any row changes species/body type, face, markings, palette, prop design, prop side unexpectedly, or overall silhouette.

## Optional: Add The Pet To A Zo Space Page

Use this optional workflow when the user asks to put the finished pet on their Zo Space page, homepage, dashboard, or another `zo.space` route.

1. Prepare web-friendly sprite strips from the completed frames or final atlas:

A Zo Space/homepage widget may intentionally use only a subset of states, usually `idle`, `running-right`, and `running-left`. Treat that as a partial interaction preview, not as a completed pet package. Unless the user explicitly asked only for a page widget prototype, do not let a partial homepage GIF or subset strip replace the full 9-row pet workflow, final atlas, QA contact sheet, validation, and package output.

- Extract frames from the finalized atlas or decoded row strips with `file extract_strip_frames.py`.
- Build one horizontal transparent PNG strip per needed state, usually:
  - `idle`: default loop
  - `running-right`: while dragging right
  - `running-left`: while dragging left
- Keep every frame the same cell size, normally `192x208`. Do not crop individual frames to content bounds; content-bounds cropping causes visible popping/scaling in CSS animation.
- For idle loops, inspect the per-frame alpha bounding boxes. Remove or regenerate frames with large size/position outliers. If the transition from the last frame back to the first pops, use a loop order that returns smoothly to the start.
- Build strips by pasting full cells at exact multiples of `cell_w`. The final strip width must equal `frames * cell_w`; otherwise CSS animation will show partial neighboring frames.
- If a generated left/right direction looks reversed in the browser, swap the route's state-to-asset mapping instead of regenerating first.

Example strip-builder and validation pattern:

```python
from pathlib import Path
from PIL import Image

frames_dir = Path("/absolute/path/to/frames/idle")
order = ["00.png", "01.png", "02.png", "01.png"]
frames = [Image.open(frames_dir / name).convert("RGBA") for name in order]
cell_w, cell_h = frames[0].size
assert all(frame.size == (cell_w, cell_h) for frame in frames)

strip = Image.new("RGBA", (cell_w * len(frames), cell_h), (0, 0, 0, 0))
for index, frame in enumerate(frames):
    strip.paste(frame, (index * cell_w, 0), frame)

out = Path("/absolute/path/to/pet-idle-v1.png")
strip.save(out)

with Image.open(out) as check:
    assert check.size == (cell_w * len(frames), cell_h)
    assert check.width % cell_w == 0
    print({"path": str(out), "frames": len(frames), "cell": [cell_w, cell_h], "size": check.size})
```

2. Upload the strips as Zo Space assets with `update_space_asset`.

Use versioned asset names whenever the strip content, width, or frame count changes. Do not overwrite `/pets/<pet-id>-idle.png` with a different frame count and then point existing code at the same URL. Browsers may keep the old image cached while the route code expects the new frame count, which creates a carousel/partial-frame artifact.

Good asset naming:

```text
/pets/<pet-id>-idle-v1.png
/pets/<pet-id>-idle-stable-5.png
/pets/<pet-id>-running-right-v1.png
/pets/<pet-id>-running-left-v1.png
```

After upload, the route's `frames` value must exactly match the uploaded strip's actual frame count:

```text
actual_frames = uploaded_strip_width / cell_width
PET_STATES.idle.frames === actual_frames
```

3. Inspect the existing route before editing it:

- Use `list_space_routes()` and `get_space_route("/")` or the target route path.
- Do not overwrite an existing homepage or public route wholesale unless the user explicitly wants that. Prefer `edit_space_route()` with a small surgical component addition.

4. Add a draggable pet component to the route. The important implementation details are:

- Use a fixed display box with the same aspect ratio as one source frame, e.g. `width = 96`, `height = 104` for half-size display of `192x208` cells.
- Animate by changing CSS `backgroundPosition`, not by swapping `<img>` dimensions.
- Set `backgroundSize` to `${frames * width}px ${height}px` so each frame is exactly one displayed cell.
- Set `imageRendering: "pixelated"`.
- Track pointer movement while pointer is down:
  - movement right -&gt; `running-right`
  - movement left -&gt; `running-left`
  - pointer up/cancel -&gt; `idle`, leaving the final position unchanged
- Use pointer events plus `setPointerCapture` and `touch-none` so it works with mouse and touch.
- If the apparent direction is wrong after testing, swap the `left` and `right` asset entries.
- If the idle animation scrolls horizontally or shows two partial frames at once, do not tweak CSS first. Check for a stale asset URL or a frame-count mismatch between the uploaded strip and `PET_STATES`; upload a new versioned asset path and update `PET_STATES` to match.

Minimal React component pattern:

```tsx
const PET_STATES = {
  idle: { src: "/pets/<pet-id>-idle-v1.png", frames: 4 },
  left: { src: "/pets/<pet-id>-running-left-v1.png", frames: 8 },
  right: { src: "/pets/<pet-id>-running-right-v1.png", frames: 8 },
} as const;

function DraggablePet() {
  const [position, setPosition] = useState({ x: 96, y: 96 });
  const [mode, setMode] = useState<keyof typeof PET_STATES>("idle");
  const [frame, setFrame] = useState(0);
  const dragRef = useRef({ active: false, pointerId: -1, offsetX: 0, offsetY: 0, lastX: 0 });
  const width = 96;
  const height = 104;
  const pet = PET_STATES[mode];

  useEffect(() => {
    setFrame(0);
    const id = window.setInterval(() => {
      setFrame((current) => (current + 1) % PET_STATES[mode].frames);
    }, mode === "idle" ? 180 : 95);
    return () => window.clearInterval(id);
  }, [mode]);

  const clamp = (x: number, y: number) => ({
    x: Math.max(0, Math.min(window.innerWidth - width, x)),
    y: Math.max(0, Math.min(window.innerHeight - height, y)),
  });

  const onPointerDown = (event: React.PointerEvent<HTMLDivElement>) => {
    event.currentTarget.setPointerCapture(event.pointerId);
    dragRef.current = {
      active: true,
      pointerId: event.pointerId,
      offsetX: event.clientX - position.x,
      offsetY: event.clientY - position.y,
      lastX: event.clientX,
    };
  };

  const onPointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    const drag = dragRef.current;
    if (!drag.active || drag.pointerId !== event.pointerId) return;
    const dx = event.clientX - drag.lastX;
    if (dx > 1) setMode("right");
    if (dx < -1) setMode("left");
    drag.lastX = event.clientX;
    setPosition(clamp(event.clientX - drag.offsetX, event.clientY - drag.offsetY));
  };

  const stopDragging = (event: React.PointerEvent<HTMLDivElement>) => {
    if (!dragRef.current.active || dragRef.current.pointerId !== event.pointerId) return;
    dragRef.current.active = false;
    setMode("idle");
  };

  return (
    <div
      role="button"
      aria-label="Drag the pet"
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={stopDragging}
      onPointerCancel={stopDragging}
      className="absolute z-20 cursor-grab active:cursor-grabbing select-none touch-none"
      style={{
        left: position.x,
        top: position.y,
        width,
        height,
        imageRendering: "pixelated",
        backgroundImage: `url(${pet.src})`,
        backgroundRepeat: "no-repeat",
        backgroundSize: `${pet.frames * width}px ${height}px`,
        backgroundPosition: `-${frame * width}px 0px`,
      }}
    />
  );
}
```

5. Verify locally before reporting completion:

- Open `http://localhost:3099/<route>` with `agent-browser` for agent-side previewing.
- Check that the pet appears, drags, switches direction while held, returns to idle on release, and has no obvious idle pop.
- While testing, specifically watch for two failure modes:
  - **pop/shrink:** an individual source frame has a visibly different content bounding box; fix by removing/regenerating that frame or choosing a smoother loop order.
  - **carousel/partial-frame scroll:** CSS is slicing the strip at the wrong boundaries, usually because the route's `frames` count does not match the actual uploaded strip or the browser has cached an overwritten asset path; fix by uploading a new versioned asset URL and matching `frames` exactly.
- If the issue appears only after deployment but not in local/generated GIFs, suspect the Zo Space embedding layer first: asset cache, stale URL, `frames` mismatch, `backgroundSize`, or state-to-asset mapping.
- Report the public `https://<handle>.zo.space/<route>` URL and whether the page is public/private.

## Zo Row Generation Delegation

After the base job has been recorded and `file references/canonical-base.png` exists, row-strip visual generation should be delegated to parallel Zo child sessions when available, unless the user explicitly says not to use delegated sessions for this run. Before row generation, state which row jobs are being delegated. If child sessions cannot be used because the current environment or tool policy blocks them, stop before row-strip generation, explain the blocker, and ask for explicit user direction before continuing sequentially.

The parent agent owns the manifest and package writes.

Default flow:

1. Parent runs `file prepare_pet_run.py`.
2. Parent generates and records `base`.
3. Parent runs `file pet_job_status.py`.
4. Parent delegates `idle` and `running-right` first as identity and gait checks.
5. Parent records the selected `idle` and `running-right` results returned by child sessions.
6. Parent decides whether `running-left` is safe to derive by mirror; if not, parent treats it as a normal grounded row job delegated to a child session.
7. Parent delegates every remaining non-derived row image-generation job.
8. Each child session receives the row prompt and every listed input image path, invokes Zo image tools, and returns only the selected generated image path.
9. Parent alone runs `file record_zo_image_result.py`, `file derive_running_left_from_running_right.py`, repair queueing, finalization, QA, and packaging.

Delegated-session write boundary: do not let child sessions edit `file zo-image-jobs.json`, copy files into `decoded/`, run `file record_zo_image_result.py`, run `file derive_running_left_from_running_right.py`, run `file finalize_pet_run.py`, or package the pet. This avoids manifest races and keeps provenance checks centralized.

Delegation handoff contract:

- Give each child session exactly one row job unless intentionally batching adjacent simple rows.
- Include the row id, the absolute prompt file path, the full prompt text or an instruction to read that exact prompt file, and every input image path with its role label from `file zo-image-jobs.json`.
- Explicitly remind the child session that the prompt's transparency and effects rules are mandatory: no detached effects, no wave marks for `waving`, no speed lines or dust for running rows, and only attached opaque sprite-like tears/smoke/stars when allowed by the state prompt.
- Tell the child session to inspect the generated candidate for frame count, identity consistency, clean flat chroma-key background, safe spacing, and forbidden detached effects before returning it.
- Tell the child session to return only the selected original Zo-generated source path plus a one-sentence QA note. The parent decides whether to record or repair it.

Use this template for each child session:

```text
Generate the `<row-id>` row for this hatch-pet run.

Run dir: <absolute run dir>
Prompt file: <absolute prompt file>
Input images:
- <absolute path> — <role>
- <absolute path> — <role>

Read and follow the row prompt exactly, including the transparency and artifact rules. Use Zo image tools only; do not use local scripts to draw, tile, edit, or synthesize sprites.

Before returning, visually check:
- exact requested frame count
- same pet identity as the canonical base
- clean flat chroma-key background
- complete, separated, unclipped poses
- no forbidden detached effects or slot-crossing artifacts

Do not edit manifests, copy into decoded, record results, mirror rows, finalize, repair, or package. Return only:
selected_source=/absolute/path/to/zo-generated-output.png
qa_note=<one sentence>
```

No silent sequential fallback: if delegated child sessions cannot be used for row-strip visual generation, stop and ask for explicit user direction before continuing without them. Only an explicit user instruction such as "do not use child sessions" or "run this sequentially" authorizes a normal sequential row-generation path. The final answer must report which row jobs were delegated and which, if any, were mirrored or repaired by the parent.

## Repair Workflow

If finalization stops because row QA failed, queue targeted repair jobs:

```bash
python "$SKILL_DIR/scripts/queue_pet_repairs.py" 
  --run-dir /absolute/path/to/run
```

Then repeat the Zo image tools generation and `file record_zo_image_result.py` ingest loop for each reopened row job. Regenerate the smallest failing scope: the failed row, not the whole sheet.

For identity repairs, use the canonical base image, original references, contact sheet, and exact row failure note as grounding context. Repair only the failed row while preserving the canonical pet identity.

## Rules

- Keep Zo image tools as the primary generation layer.
- Keep reference images attached/visible for Zo image tools whenever the chosen path supports references.
- Attach the row's `file references/layout-guides/<state>.png` image to every row-strip job as a layout-only guide, and do not accept outputs that copy guide pixels.
- Use delegated Zo child sessions for row-strip visual generation after the parent records the base image unless the user explicitly says to run sequentially.
- Generate every normal visual job with Zo image tools: base plus all row strips that are not explicitly approved `running-left` mirror derivations.
- Treat only the base job as eligible for prompt-only generation; every row job must attach its listed grounding images.
- Delegate `running-right` first, then mirror `running-left` only when visual inspection confirms a mirror preserves identity and semantics; otherwise delegate `running-left` as a normal grounded Zo image-tools row.
- Never substitute locally drawn, tiled, transformed, or code-generated row strips for missing Zo image outputs.
- Never manually mutate `file zo-image-jobs.json` to claim a visual job completed.
- Do not rely on generated images for exact atlas geometry; use this skill's deterministic scripts.
- Use the chroma key stored in `file pet_request.json`; do not force a fixed green screen.
- Keep the pet's silhouette, face, materials, palette, and props consistent across all rows.
- Enforce the transparency and effects rules above in every base, row, and repair prompt.
- Treat visual identity drift as a blocker even when `file qa/review.json` and `file final/validation.json` have no errors.
- Treat a contact sheet that shows cropped references, repeated tiles, white cell backgrounds, or non-sprite fragments as failed.
- Treat forbidden detached effects, chroma-key-adjacent artifacts, shadows, glows, smears, dust, landing marks, wave marks, speed lines, or motion trails as failed rows.
- Treat `file qa/review.json` errors as blockers. Warnings require visual review.

## Acceptance Criteria

- Final atlas is PNG or WebP, `1536x1872`, transparent-capable, and based on `192x208` cells.
- Used cells are non-empty and unused cells are fully transparent.
- Atlas follows the row/frame counts in `file references/animation-rows.md`.
- Contact sheet and preview videos have been produced unless explicitly skipped.
- `file qa/review.json` has no errors.
- Row-by-row review confirms the animation cycles are complete enough for the Zo pet viewer.
- `file ${ZO_PETS_HOME:-/home/workspace/Images/hatch-pet/pets}/<pet-name>/pet.json` and `file ${ZO_PETS_HOME:-/home/workspace/Images/hatch-pet/pets}/<pet-name>/spritesheet.webp` are staged together for custom pets.