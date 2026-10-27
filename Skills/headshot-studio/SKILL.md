---
name: headshot-studio
description: Retouch and prepare a professional headshot from an uploaded photo in four modes — studio-look retouch, office background swap, light and color fix, and a platform crop set (square profile, wide banner, vertical bio) with export settings. Use when the user uploads a portrait and asks for a headshot, LinkedIn or profile photo, background replacement, color or lighting correction, or sized crops for profiles and speaker bios. Preserves the person's identity; every edit is checked against the original.
metadata:
  author: jaknyfe.zo.computer
---

# Headshot Studio

## Route first

Ask one question only if the request is ambiguous: which mode(s), and whether the backdrop should be a neutral studio or an office. Otherwise run the pipeline below.

| Mode | Job | Tool |
|---|---|---|
| 3 — Light & Color | Fix white balance, exposure, shadows, cast | `edit_image` (generative) |
| 1 — Studio Look | Soft key light, neutral backdrop, true color | `edit_image` |
| 2 — Background Swap | Clean out-of-focus office backdrop | `edit_image` |
| 4 — Crop Set | Square, banner, vertical, export settings | `scripts/crop_set.sh` (deterministic) |

Recommended order: **3 → (1 or 2, never both) → 4**. Mode 3 first normalizes color so the backdrop step matches. Modes 1 and 2 both replace the backdrop; pick one.

## Identity gate (run after every edit)

1. Build a side-by-side: `convert original.jpg edited.jpg +append /home/.z/workspaces/<id>/compare.jpg`
2. View it with `read_file`. Check the face, hair, and clothing match the original in shape, expression, and detail.
3. If any feature changed (eyes, nose, jaw, hairline, teeth, clothing), re-run with stricter wording ("keep every facial feature unchanged") or stop and tell the user which feature drifted. Do not deliver an edit that changed the person.

Generative editors can smooth skin, slim faces, or redraw hair. Mode 3 explicitly forbids reshaping, and the gate is how that is enforced.

## Prompts (use verbatim unless the gate fails)

**Mode 1 — The Studio Headshot Look**

> Act as a professional portrait retoucher. Edit the photo I upload so it looks like a studio session shot it. Analyze the light direction, the skin tones, the background, the crop and the color cast. Apply soft key light from one side, a clean neutral backdrop, natural depth of field and true to life color. Keep the face, hair and clothes exactly as they are.

**Mode 2 — The Background Swap**

> Act as a photo editor who specializes in professional profiles. Replace the background of the photo I upload with a clean office setting softly out of focus. Analyze the edges around the hair and shoulders, the light on the subject, the shadow direction and the color temperature. Match the new background to that light, blend every edge cleanly and keep the person untouched.

**Mode 3 — The Light And Color Fix**

> Act as a color grader for portrait photography. Fix the light and color in the photo I upload. Analyze the white balance, the exposure, the harsh shadows, the shine on the skin and any yellow or green cast from indoor bulbs. Apply even exposure, balanced shadows, a gentle matte finish and neutral skin tones. Do not reshape, slim or smooth any feature of the person.

**Mode 4 — The Platform Crop Set** (judgment step, then script)

> Act as a photo editor preparing headshots for professional use. Take my edited photo and prepare it for every place I will use it. Analyze the framing, the head room, the eye line and how the photo reads at small sizes. Design a square crop for profiles, a wide banner version, a vertical version for speaker bios and the export settings for each one.

Mode 4's analysis is done by you: check headroom (top of head about 8–12% from the top edge), eye line near the upper third, and that the face is still readable in the 160 px preview. Set `OFFSET_Y` to move the crop, then run the script.

## Mode 4 — Crop set

```bash
OFFSET_Y=0 sh /home/workspace/Skills/headshot-studio/scripts/crop_set.sh <edited.jpg> <out_dir>
```

Outputs in `<out_dir>`:

| File | Size | Use |
|---|---|---|
| `<name>-square-800.jpg` | 800×800 (1:1) | Profile pictures, avatars |
| `<name>-banner-1500x500.jpg` | 1500×500 (3:1) | Wide banners, header images |
| `<name>-vertical-1000x1250.jpg` | 1000×1250 (4:5) | Speaker bios, event pages |
| `<name>-square-160-preview.jpg` | 160×160 | Small-size legibility check |

Export settings applied to all files: sRGB, JPEG quality 92, progressive, metadata stripped (`-strip`). The banner is a 3:1 crop taken from full source width, so a portrait source gives a band about one-third of its width in height. A source narrower than 1500 px is upscaled to 1500 px wide, which softens detail. Check the square and banner outputs at full size before delivering. For a sharper banner, use a wider source or accept a lower-resolution banner.

Sizes are defaults chosen for common profile surfaces. The user's platform may require different pixel counts; change the constants in `scripts/crop_set.sh` before running.

## Delivery

- Save finals to `/home/workspace/Media/headshots/<name>/` (create the folder; do not write into the root of the workspace).
- Report: which mode(s) ran, the file paths, and the identity-gate result per edit (pass, or which feature drifted).
- Do not upload, publish, or send any headshot unless the user asks for that action in this turn.
