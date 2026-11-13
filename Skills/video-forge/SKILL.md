---
name: video-forge
description: Plan and coordinate end-to-end video creation and editing by routing work to the right specialized skill or tool, from brief and script through assets, assembly, sound, rendering, and quality review. Use for animated shorts, explainers, promotional videos, and mixed-media edits.
metadata:
  author: jaknyfe.zo.computer
---

# Video Forge

Video Forge is the project-level workflow and dispatcher for video work. It coordinates specialist skills; it does not replace their implementation instructions. Keep work in the user's named project folder, or ask for a destination when none is clear. Preserve source media and write derived outputs separately. Never publish or schedule a video without explicit approval for that specific video.

## Production stages

1. **Brief** — Establish audience, purpose, runtime, aspect ratio, delivery platform, source material, visual direction, narration, music, captions, and approval boundaries. Separate confirmed facts from creative proposals.
2. **Plan** — Create a beat sheet or shot list with target duration, visual, audio, text, and asset needs for each beat. Identify licensing, likeness, factual, and continuity constraints before production.
3. **Build assets** — Generate or source only the assets needed. Keep names, claims, logos, statistics, and quotations faithful to supplied or verified sources. Track provenance and usage rights.
4. **Assemble** — Choose one primary composition/editing path, then use other tools only for bounded tasks such as audio cleanup, transcoding, captions, or finishing.
5. **Review** — Check the rendered file with probe data and representative frames; listen to the audio; inspect captions, transitions, safe areas, timing, and encoding. Fix defects and repeat review.
6. **Handoff** — Report output path, format, duration, dimensions, audio/caption status, verification performed, and anything requiring human approval. Rendering is not publication.

## Skill and tool routing

| Need | Route |
| --- | --- |
| HTML/CSS/GSAP animated composition, title cards, overlays, kinetic text, voiceover-led graphics, website-to-video | `Skills/hyperframes/SKILL.md`; read the relevant vendored skill under `Skills/hyperframes/plugin/skills/` before execution. |
| React/TSX programmatic video, reusable data-driven scenes, Remotion rendering | `Skills/remotion-best-practices/SKILL.md`; read its relevant `rules/*.md` before changing a composition. |
| Editing supplied footage by transcript, cuts, overlays, grading, subtitles, or narration | `Skills/video-use/SKILL.md`; follow its confirm-before-cut and production-correctness rules. |
| Generative edits to an existing clip using Gemini | `Skills/gemini-video-editing/SKILL.md`. |
| Frame extraction, contact sheets, or visual inspection inputs | `Skills/video-frames/SKILL.md` for its frame extraction CLI; otherwise use FFmpeg frame extraction. |
| Mathematical/explainer animation | `Skills/video-use/skills/manim-video/SKILL.md`. |
| Local media inspection, conversion, trimming, muxing, loudness/audio finishing, or frame extraction | Use the FFmpeg adapter below. |
| Speech synthesis, transcription, or external video generation | Use the appropriate available skill/tool and confirm its constraints before use. |

Choose the simplest primary path that matches the asset and desired edit. Avoid rendering the same full composition in multiple engines. For a graphics-first short, prefer HyperFrames or Remotion; for source-footage edits, prefer Video Use; for a targeted generative transformation, use Gemini Video Editing. FFmpeg is the media utility layer and can serve any path.

## FFmpeg adapter

Use installed `ffmpeg` and `ffprobe` directly for deterministic local media operations. Inspect inputs first; preserve originals; write to a new output path. Prefer explicit codecs, pixel format, frame rate, dimensions, audio behavior, and output container when delivery requirements are known. Do not re-encode when stream-copy is valid, but verify compatibility and timestamps. Use argument arrays or safely quoted paths; never build shell commands from untrusted filenames or text.

Typical tasks:

- Probe streams, duration, frame rate, dimensions, and audio tracks with `ffprobe`.
- Extract representative frames/contact sheets for review.
- Trim, scale/crop/pad, concatenate, convert, or remux media.
- Normalize or mix audio; preserve sync and avoid clipping.
- Add or repair subtitles only when the requested workflow calls for FFmpeg subtitle rendering.

After every operation, probe the output and check a frame or short playback. Validate duration, dimensions, frame rate, audio presence/sync, subtitle timing, and nonzero file size against the brief. For a full visual grade, use a contact sheet or inspect several points across the timeline; one opening frame is not enough. Do not claim visual correctness from successful encoding alone.

FFmpeg adapter commands are recipes, not a substitute for reading a specialist skill's hard rules. In particular, Video Use's segment/caption/audio ordering rules take precedence when that workflow is selected.

## Decision and approval gates

- For supplied footage, follow the selected editing skill's confirmation requirements before making cuts or destructive changes.
- Keep generated drafts local. Do not upload, publish, or schedule without explicit per-video approval.
- Do not invent facts, spoken words, product claims, or source attribution.
- If a required source, license, voice authorization, or factual basis is missing, identify the gap before production.
- Do not call a render complete until the resulting video and representative frames have been inspected and audio has been checked when present.

## Final delivery checklist

- Output is saved in the agreed project directory; source files remain intact.
- Container, codec, dimensions, frame rate, and duration match the brief.
- Audio and captions are present, synchronized, intelligible, and at suitable levels when requested.
- Representative frames and the full timeline have been visually checked for black/frozen frames, clipping, layout issues, and unintended artifacts.
- Rights/provenance and outstanding approvals are stated; no publication occurred without explicit approval.
