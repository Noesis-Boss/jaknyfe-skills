---
name: cutout-cartoon-shorts
description: Turn a short script (and optionally a reference picture) into a vertical 2D cut-out cartoon Short on Zo - character poses and props generated as flat cartoon images, keyed to transparent sprites, voiced with ElevenLabs, and animated in code (Remotion) with a 2.5D camera, physics-based throws, drawn effects, and sound. Use when the user asks for a cut-out, cartoon, or Oddsoneout-style animated Short from a script or picture.
metadata:
  author: jaknyfe.zo.computer
---
# Cut-out Cartoon Shorts

Output: a 1080x1920 Remotion composition at 60 fps, rendered to MP4 under `Media/cartoon-shorts/<short>/`. A flat cartoon character acts out a voice-over. Every pose and expression is its own generated picture with a transparent background. Motion, camera, physics, effects, and timing are code.

Method adapted from a public Claude Code + Higgsfield tutorial. Techniques are restated in Zo terms; no tutorial text is reproduced.

## Stage order

Run stages in order. Each stage ends with a "done" check. Do not start a stage until the previous one's check passes.

1. **Script** (`Done` = final lines shown to the user with word count and sources)
2. **Beat sheet** (`Done` = table of time / words / on-screen / picture / sound)
3. **Voice** (`Done` = voice file + word timestamps + timing constants)
4. **Pictures** (`Done` = every sprite keyed and checked on a colour sheet)
5. **Prep** (`Done` = trimmed sprites + `sprites.json` with head, feet, and offsets)
6. **Animation code** (`Done` = contact sheet of every beat reviewed)
7. **Sound** (`Done` = mixed audio, peak near -4 dBFS)
8. **Render and verify** (`Done` = ffprobe confirms size, fps, duration, audio)

## Stage 1: Script

- Ask for the script only if none was given. Otherwise use it, and fix it to the rules below.
- Length: 10–20 s, about 25–35 words per line, 4–6 lines.
- Write plain speech. Avoid narrator phrases ("here's the thing"), hype words (incredible, shocking, amazing, insane), and exclamation marks.
- The first line names what is visible in frame 0.
- Every fact must be true. For a researched script, verify the central fact against a primary source (university, museum, government agency, or established scientific body) and cite the links.
- Avoid repeating a topic already logged in `Skills/cutout-cartoon-shorts/topics-used.md`. Append each new topic there.
- Do not ask the user to pick between ideas. Pick the strongest and say why in one sentence.

## Stage 2: Beat sheet

- One visual beat per line, landing on the exact spoken word.
- Frame 0 states the premise, centred and readable like a thumbnail.
- One gag per beat (an object that opens its eyes, an anticipation squash before a blast, a sweat drop, a thrown object that returns).
- Last frame loops back to frame 0.
- List every pose, expression, moving prop, and set piece needed. This list drives Stage 4.

## Stage 3: Voice

- Use ElevenLabs through the connected integration:
  1. `use_integration(app_slug="elevenlabs", tool_name="elevenlabs-get-voices-with-descriptions", configured_props={})` — pick a natural, conversational male or female voice. Not deep, not a narrator.
  2. `use_integration(app_slug="elevenlabs", tool_name="elevenlabs-text-to-speech", configured_props={"voiceId": "...", "modelId": "...", "text": "...", "stability": 0.5, "similarityBoost": 0.75})` — plain text, no tags. Check `elevenlabs-list-models` for the current expressive model ID and use it if available.
  3. `elevenlabs-get-audio-from-history-item` (or the download action from `list_app_tools`) to save the file to `Media/cartoon-shorts/<short>/vo/take1.mp3`. Confirm the path exists before continuing.
- Fallback if ElevenLabs is unavailable: Zo's `generate_speech` (presets: ara, eve, leo, rex, sal). Tell the user the fallback was used.
- Word timestamps with the installed faster-whisper:
  ```python
  from faster_whisper import WhisperModel
  m = WhisperModel("small", compute_type="int8")
  segs, _ = m.transcribe("take1.mp3", word_timestamps=True)
  words = [{"w": w.word.strip(), "s": w.start, "e": w.end} for s in segs for w in s.words]
  ```
- Whisper word edges can be off by about 0.2 s. Find real pauses by loudness (RMS per 20 ms; silence = below -42 dB for at least 0.18 s) and trust those for big sounds.
- Define each beat as a constant (`T = {turn: 2.05, release: 3.7, land: 4.8}`). Composition length = voice end + 0.5 s.

## Stage 4: Pictures

Zo's `generate_image` does not expose a transparent background, so generate on a flat solid colour and key it out (Stage 4b).

**Style blocks.** Reuse these exact strings for every picture in a project:

- Character: `Flat 2D cartoon in exactly the same drawing style as the reference images: the same simple character with a big round head, a small soft body, noodle arms with simple hands, short legs with rounded feet, thick smooth black outlines of even weight, flat fill with one soft pale shade, small solid black oval eyes, simple curved eyebrows, no nose, no hair, no clothes, a pink tongue only when the mouth is open. Clean vector-like linework, flat colours, no texture, no text, no border. Plain solid background colour #9BCFFD, nothing else in the background.`
- Object or set piece: `Flat 2D cartoon in exactly the same drawing style as the reference images: thick smooth black outlines of even weight, flat colours with one simple soft shade, clean vector-like linework, no texture, no text, no border, no characters. Plain solid background colour #9BCFFD, nothing else in the background.`

**Prompt pattern.** Framing ("Full body, three-quarter view facing right" / "Waist-up close-up, facing the viewer") + expression ("scared: eyebrows tilted up in the middle, wide eyes, mouth wide open") + exact hands ("the hand on the right side of the image holds a black garbage bag by its knot") + "whole body in frame with a margin". Say "on the left side of the image", not "his left".

**Consistency.** Pass one approved hero picture as `reference_filepaths` on every later call. If there is no reference, generate one hero picture first, check it, then use it.

**Generate in parallel.** Each call is one `generate_image` tool call. Use the file_stem as the picture name, e.g. `images/<short>/raw/pose_scared.png`. Use `aspect_ratio` 2:3 for full body, 4:5 for close-ups, 1:1 for props, 3:2 for set pieces.

**Two poses that must align** (same pose with and without the object): generate the second as an edit of the first with `edit_image` (source_filepath = first picture, prompt "the same picture with the bag removed, the hand now empty and open, everything else identical").

### Stage 4b: Key the background

```bash
python3 /home/workspace/Skills/cutout-cartoon-shorts/scripts/key_background.py raw/pose_scared.png sprites/pose_scared.png
```

Check every sprite on a coloured sheet before use. Known glitch: shaded areas can turn half-transparent. Regenerate that picture with a stronger instruction ("every shaded area fully opaque") and key again.

Done = every sprite passes the sheet check. Save prompts to `images/<short>/prompts.md`.

## Stage 5: Prep

```bash
python3 /home/workspace/Skills/cutout-cartoon-shorts/scripts/prep_sprite.py sprites/pose_scared.png public/<short>/pose_scared.png
```

The script prints JSON with `offset` (trim origin), `size`, `head` (centre and radius from the hole-filled silhouette), and `feet` (bottom-centre). Collect the JSON for every sprite into `src/<short>/sprites.json`.

- Scale each full-body pose so its head radius matches across poses. Swaps then never change head size.
- Full-body poses share one world feet point. Waist-up poses align their head to the full-body head.
- Keep the offset: edited pose pairs need it for alignment.

## Stage 6: Animation code (Remotion)

- Use the `remotion-best-practices` skill for Remotion conventions. Create the project with `bunx create-video@latest` if none exists. Register the composition in `src/Root.tsx`. Put final assets in `public/<short>/`.
- **Camera (2.5D multiplane).** Each sprite sits on a layer at depth Z. Camera has (x, y, z). Layer scale k = 1000 / (Z − z). Dollying changes perceived depth. Depths that worked: foreground 650, character 1000, mid ground 1800, set piece and horizon 3000. Ease moves: easeInOutCubic for glides, easeOutCubic for blast pull-backs. Interpolate scale in log space so zooms feel even. Holds are perfectly still. Blur far layers 2.5–3.6 px only while the camera is close on the character.
- **Pose swaps never cross-fade.** Swap during motion that hides it:
  - turn: squash scaleX ~0.8 about the feet; swap at the narrowest frame.
  - action: anticipation squash (scaleY 0.94, scaleX 1.04) → swap → stretch (1.03), then a damped spring settle.
  - throw: swap to follow-through at release.
  - catch: swap to the holding pose the frame the object reaches the hand.
- **Life on holds.** Breathing (scaleY ±0.9 % about the feet, ~0.6 Hz). Small tremble when scared. Contact shadow under full-body poses: soft ellipse, rgba(72, 54, 42, 0.26), 3 px blur.
- **Projectiles.** Thrown sprites follow a 3D arc. x and z at constant speed; y follows a gravity parabola with the apex at a chosen fraction of flight:
  ```ts
  const g = (2 * (y0 - y1)) / (ta * ta - (T - ta) * (T - ta));
  const ya = y0 - 0.5 * g * ta * ta;
  const y = (tau: number) => ya + 0.5 * g * (tau - ta) * (tau - ta);
  ```
  A return flight ends exactly on the object drawn in the next pose.
- **Effects in code, same flat look.** Lava: flat orange, no outline. Smoke and steam: draw every outline circle first, then every fill circle. Shrink puffs away rather than fading outlined puffs. Faces on objects: white eyes, black pupils, glint, eyelids clipped to the eye, thick brows.
- **Screen shake.** Sums of sines times an amplitude envelope. Never random per-frame jumps.
- **Rules.** No motion blur. No cross-fades between drawings. Every move eased and at least 1 s for camera glides. One focal action at a time. Same outline weight across pictures and drawn effects.

## Stage 7: Sound

- Layers: voice at 0 dB, effects from one cue list (file, start time, dB).
- Sources: user-supplied sound effects first. If none exist, say so and ship without them. Do not invent a library path.
- Levels under voice: whooshes −25 to −31 dB; impacts −14 to −19 dB; beds −26 to −33 dB; big blast −8 to −10 dB inside a pause.
- Sync each file by its measured onset or peak to the beat. Peak-normalise the mix to about −4 dBFS.

## Stage 8: Check and render

- **Contact sheet.** Still frames at every beat (Remotion `renderStill` at 0.5 scale) in one grid. Check frame 0, every swap, every gag, and the last frame.
- **Pop scan.** Render a 0.5x preview. Compute mean frame-to-frame difference (blurred). Flag frames above 2.2x the local median. Every flag must be an intended swap or cut.
- **Render.** `npx remotion render src/index.ts <CompId> out/<name>.mp4 --scale=2 --image-format=png --crf=16 --pixel-format=yuv420p`. Zo may have no GPU, so use the default renderer and report the time. Do not claim GPU rendering.
- **Verify.** `ffprobe` must show 2160x3840, 60 fps, frames = duration × 60, an audio stream as long as the picture, and motion in the final second. View two extracted frames before reporting done.

## Deliverables

- `Media/cartoon-shorts/<short>/<name>-4K.mp4`
- Remotion project path, `sprites.json`, `prompts.md`, and the voice file
- Final script, word count, and the source links
- One line per choice made without asking: voice, beat count, picture count, and any fallbacks used

## Publishing boundary

Do not upload to any platform. Final publication to the AI for the Rest of Us YouTube channel needs the user's explicit per-video approval in that moment.

## Scripts

- `scripts/key_background.py IN OUT [--tol 60]` — keys a flat background connected to the border; softens edges.
- `scripts/prep_sprite.py IN OUT` — trims to alpha box + 12 px; prints head and feet JSON.

## Known limits

- Zo image generation is not verified for consistent character identity across many poses. Use the hero-reference step and check every sprite.
- Higgsfield is not connected to Zo. If the user connects it through the Higgsfield integration, its image generator can replace Stage 4 and the transparent output removes the keying step.
- Earlier Zo renders are not benchmarked. Report measured times, not estimates.
