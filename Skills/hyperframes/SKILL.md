---
name: hyperframes
description: Create HTML/CSS/GSAP video compositions and render them to MP4 — title cards, overlays, captions, voiceovers, audio-reactive visuals, and website-to-video conversions. Use when the user wants to produce video from code rather than a timeline editor, or wants to turn an existing web page into a video. Installed as a TRIAL of the OpenAI-curated Codex plugin bundle.
compatibility: Created for Zo Computer. Node >=20 and the `hyperframes` CLI (npx) required for render/preview; browser mode needs a local Chrome.
metadata:
  author: jaknyfe.zo.computer
  upstream: https://github.com/openai/plugins/tree/main/plugins/hyperframes
  license: GPL-3.0-only
  install_type: trial
---

# HyperFrames (Zo adapter)

Zo router for the OpenAI-curated `hyperframes` plugin bundle. This is a **TRIAL install** —
see `Skills/TRIAL-openai-plugins.md` for scan results and removal instructions.

## What lives here

The vendored plugin is at `plugin/`. Read the upstream skill file before running any workflow —
this router does not restate them:

| Skill | Upstream file | Use for |
| --- | --- | --- |
| `hyperframes` | `plugin/skills/hyperframes/SKILL.md` | The core workflow: compositions, title cards, overlays, captions, voiceovers |
| `hyperframes-cli` | `plugin/skills/hyperframes-cli/SKILL.md` | `init`, `lint`, `inspect`, `preview`, `render`, `transcribe`, `tts`, `doctor`, `browser` |
| `gsap` | `plugin/skills/gsap/SKILL.md` | Animation reference: `gsap.to()`, `from()`, `fromTo()`, easing, stagger, defaults |
| `website-to-hyperframes` | `plugin/skills/website-to-hyperframes/SKILL.md` | Convert a web page into a video composition |
| `hyperframes-registry` | `plugin/skills/hyperframes-registry/SKILL.md` | Install and wire registry blocks/components into compositions |

Full path pattern: `/home/workspace/Skills/hyperframes/plugin/skills/<skill>/SKILL.md`

## How to work in Zo

1. **Read the upstream `SKILL.md` first.** It carries the actual composition schema, HTML structure,
   and render flags. Do not reconstruct them from memory.
2. **Reuse, don't reinvent.** No local hyperframes skill or project exists on this machine
   (verified 2026-09-27: no `Skills/hyperframes-local/`, no `/home/workspace/hyperframes`). The
   OpenAI bundle is the only implementation present, so it is the reference — but check for
   newer local work before extending it.
3. **Composations live in the user's workspace**, not in this skill directory. Write output under
   `/home/workspace/noesis_content/videos/` (or the project the user names), so the files are
   visible and downloadable.
4. **Render is slow and can fail silently.** Always confirm with `hyperframes doctor` before a
   long render, and after rendering verify the MP4 exists with a non-trivial size
   (`ls -lh`, `ffprobe`) and that it has audio tracks when a voiceover was expected.
5. **Never auto-publish.** Rendering produces a local MP4. Uploading is a separate, explicit user
   instruction — see the standing YouTube approval rule in the user's rules.

## Codex → Zo deltas

- Codex's `@hyperframes` mention syntax does not exist in Zo. Reference the skill by name and read
  the file from the path above.
- `plugin/.codex-plugin/plugin.json` is kept for provenance only; Zo does not read it.
- No Codex app connectors ship with this plugin, so nothing depends on OAuth linking.

## Prerequisites

- Node >= 20 (this machine: v26.9.0 — satisfied)
- CLI is invoked via `npx -y hyperframes-cli@latest <cmd>`; the bundle does not vendor a binary.
- Browser mode (`hyperframes browser`) requires a local Chrome/Chromium install.

## Removal (TRIAL)

```bash
rm -rf /home/workspace/Skills/hyperframes
```
