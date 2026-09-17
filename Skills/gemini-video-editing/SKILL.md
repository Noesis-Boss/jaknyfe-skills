---
name: gemini-video-editing
description: Create precise Google Gemini video-editing prompts for cinematic restyling, background and object replacement, cleanup, wardrobe changes, visual effects, product ads, face preservation, and camera-angle changes. Use when the user wants to edit an existing video through Gemini with natural-language instructions.
metadata:
  author: jaknyfe.zo.computer
---
# Gemini Video Editing

Create a short, executable prompt for Google Gemini's video editor. Treat the source video as authoritative and explicitly preserve anything the user does not want changed.

## Workflow

1. Identify the edit type, subject, desired result, and delivery context.
2. Ask only for missing details that materially affect the prompt: source clip, target element, style or replacement, timing, aspect ratio, and audio behavior.
3. Write one primary Gemini prompt using plain language. Keep it focused on the requested change.
4. Add preservation constraints: “Keep everything else the same,” plus the specific face, clothing, movement, camera, lighting, logo, or background details that must remain stable.
5. Provide a short fallback prompt if the first edit is too broad or changes unwanted details.
6. Recommend a visual check for identity, temporal consistency, edges, shadows, reflections, text, and audio before use.

## Prompt construction

Use this shape:

```text
[Action] [target] [desired result]. Keep [subject and important details] unchanged. Match [lighting, shadows, perspective, movement, and timing] so the edit looks natural. Keep everything else the same.
```

Prefer one clear transformation over a long cinematic brief. For a single continuous shot, say “in one continuous shot” and state “no scene cuts.” For a timed effect, specify the trigger and timing. For audio, state whether to preserve the original audio or regenerate it.

## Edit patterns

### Cinematic look

```text
Edit this video into a cinematic clip. Keep [main subject] unchanged. Improve the lighting to [lighting style], add [camera movement], [color treatment], and [mood]. Do not change [protected details]. Keep everything else the same.
```

### Background replacement

```text
Replace the background with [new location]. Keep [main subject] exactly the same. Match the lighting, shadows, camera angle, and perspective so it looks real. Do not change [face, clothing, voice, lip movement, or body movement].
```

### Object removal or replacement

```text
Remove [object] from this video and fill the space naturally from the surrounding background. Keep [subject], lighting, camera movement, and timing unchanged. Make the edit clean and realistic.
```

```text
Replace [old object] with [new object]. Keep the same camera angle, lighting, reflections, shadows, movement, and scale. Do not change [subject] or [background].
```

### Wardrobe change

```text
Change [person's outfit] into [new outfit]. Keep the face, body shape, pose, and movement unchanged. Make the clothing move naturally with the body and match the original lighting and shadows.
```

### Style treatment

```text
Apply a [style] look to this video with [style details], [color tone], and [texture]. Keep [main subject] unchanged. Do not change [important details]. Keep everything else the same.
```

### Product advertisement

```text
Edit this product video into a premium advertisement for [product]. Keep the product's shape, color, logo, screen, and key features unchanged. Add [background], [lighting], and [camera movement]. Keep the result realistic.
```

### Timed visual effect

```text
Add [effect] when [specific action] happens. Start it exactly at [timing]. Keep [subject], background, camera movement, and original timing unchanged. Blend the effect naturally into the scene.
```

### Face preservation

```text
Keep the original subject's face exactly the same throughout the edit. Do not change the eyes, nose, mouth, skin tone, hair, or facial expression. Only edit [specific element].
```

### Camera-angle change

```text
Recreate this scene from a [new camera angle]. Keep [subject], action, outfit, and important details consistent. Adjust lighting, shadows, and background perspective to match the new angle.
```

## 20-second reel templates

Use these when preparing a short vertical reel. Keep the edit focused on one transformation and preserve the source performance.

### Talking-head hook

```text
Turn this clip into a 20-second vertical social reel. Keep the speaker's face, voice, words, lip movement, expression, clothing, and body movement unchanged. Reframe to 9:16, keep the speaker centered, add readable captions that match the spoken words, and use subtle punch-ins only at natural emphasis points. Preserve the original audio. Do not invent or rewrite any words. Keep everything else the same.
```

### Product demonstration

```text
Turn this product demonstration into a 20-second vertical social reel. Keep the product shape, color, logo, text, proportions, and demonstrated action unchanged. Reframe to 9:16 without cropping important details, tighten pauses while preserving the original sequence, and add captions using only words spoken or visibly shown in the source. Preserve the original audio. Do not invent claims or features. Keep everything else the same.
```

### B-roll montage

```text
Create a 20-second vertical reel from this footage using the strongest moments in their original order. Keep the subject, locations, colors, movement, and visual meaning unchanged. Use clean cuts, preserve natural motion, and add minimal captions only when supplied with the edit request. Preserve the original audio unless instructed otherwise. Do not create new scenes or alter the subject's identity. Keep everything else the same.
```

For every reel, state the target aspect ratio, whether captions are allowed, and whether original audio must remain. Avoid asking Gemini to “make it viral” without concrete visual instructions.

## Gemini API execution

For an actual local edit, use `file scripts/edit_video.py`. Set `GEMINI_API_KEY` in the environment, keep the source unchanged, and pass the focused prompt as one argument:

```bash
python3 Skills/gemini-video-editing/scripts/edit_video.py input.mp4 "Apply the edit. Keep everything else the same." output.mp4
```

The script uploads the source through Gemini Files, waits for processing, calls `gemini-omni-1.1-flash`, retrieves the returned video, and writes a separate output file. It does not claim success until the output file is written. Review the rendered file for identity, timing, artifacts, audio, and captions.

Do not place `GEMINI_API_KEY` in the skill, shell history, or committed files. Store it in Zo Settings → Advanced or inject it for the current process.

## VoiceStudio narration workflow

Use VoiceStudio after the visual edit when the narration should use the user's supplied or consent-verified voice. VoiceStudio runs locally at `http://localhost:3900` and accepts OpenAI-compatible requests at `/v1`.

1. Prepare narration text from the approved script. Do not invent claims or rewrite quoted material.
2. List available profiles with `GET http://localhost:3900/v1/audio/voices` and select the verified profile ID.
3. Generate WAV narration with `POST http://localhost:3900/v1/audio/speech`, using `model: "omnivoice"`, the profile ID in `voice`, `response_format: "wav"`, and a deliberate `speed`.
4. Inspect the WAV, then align it to the video with the local video workflow. Preserve the original track until the replacement has been checked.

Example request:

```bash
curl -sS http://localhost:3900/v1/audio/speech \
  -H 'Content-Type: application/json' \
  -d '{"model":"omnivoice","voice":"<verified-profile-id>","input":"<approved narration>","response_format":"wav","speed":1.0}' \
  --output narration.wav
```

For a 20-second reel, keep narration short enough to fit the measured duration, normalize levels, and check lip-sync only when the source is a talking head. Never clone or use another person's voice without permission.

## Quality rules

- Never invent names, claims, logos, statistics, or product features.
- For talking heads, protect face, voice, lip movement, expression, clothing, and body movement unless the user requests otherwise.
- For products, protect shape, branding, color, text, proportions, and functional details.
- For replacements, require realistic lighting, shadows, reflections, occlusion, scale, and motion.
- For removals, require natural background reconstruction and temporal consistency across frames.
- If the request would alter identity or meaning, call that out and ask what must be preserved.
- Do not claim Gemini completed an edit. This skill writes the prompt; the user or an available Gemini tool must run it.

## Output format

Return:

1. `Gemini prompt:` followed by the ready-to-paste prompt.
2. `Preserve:` one sentence listing the critical invariants.
3. `Check:` one sentence listing the visible and audio checks after rendering.

If the user supplied a video and asks for execution, use the available Gemini or video workflow after presenting the prompt. Preserve the original source and save derived output separately.