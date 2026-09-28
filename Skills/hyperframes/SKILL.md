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

- Node >= 22 (this machine: v26.9.0 — satisfied) and FFmpeg on PATH.
- The npm package is `hyperframes`, **not** `hyperframes-cli` (the `hyperframes-cli` name is only the
  skill directory inside the bundle). Invoke it as `npx -y hyperframes@latest <cmd>`, or pin the
  version the scaffold wrote into `package.json` (`npx --yes hyperframes@0.8.81 render`).
- `hyperframes doctor` must be green before a long render. Verified 2026-09-27 at v0.8.81: Node,
  FFmpeg/FFprobe, Chrome headless shell, whisper-cpp, and unzip all pass. The two optional
  local-voice fallbacks (Kokoro TTS, MusicGen BGM) are not installed, and the Docker daemon is
  not running — none of those block a render.
- Browser mode (`hyperframes browser`) requires a local Chrome/Chromium install.

## `hyperframes init` is not sandboxed

`init` scaffolds the project, then links its workflow skills into **every agent skills directory it
can find on the host**, and creates an empty placeholder dir for each linked name under
`/root/.claude/skills/`.

Measured exactly 2026-09-28: **635 symlinks across 53 directories** (624 across 52 dirs found at
depth 4, plus 11 more under `/root/.pi/agent/skills` at depth 5 — an inventory that stops at
`find -maxdepth 4` undercounts, so sweep at depth 6). Directories hit include `.codex`, `.gemini`,
`.claude`, `.config/goose`, `.continue`, `.hermes`, `.kilocode`, `.openclaw`, `.terramind`,
`.qoder`, `.iflow`, `.commandcode`, `.roo`, `.trae`, `.codeium/windsurf`, `.augment` and ~30 more.

Every target under `/root/.claude/skills/` is an **empty directory** (0 files), so the links resolve
but there is nothing behind them — no agent runtime can actually load these skills. Confirmed inert
in all three runtimes installed and running on this host (`hermes`, `kilocode`, `openclaw`; `zcode`
is not installed at all). A separate, older 2026-08-18 platform fanout of ~795 links points at the
same empty placeholders; that one is **pre-existing, not ours** — leave it alone.

Nothing lands in `/home/workspace/Skills` — the workspace is not on its search path — but it does
write outside the workspace on every run, so run it once per project and then clean up.

To undo a run (recipe used 2026-09-28, removed all 635 and confirmed 0 remaining):

```bash
# 1. snapshot links before deleting
find /root -maxdepth 6 -type l 2>/dev/null | while read -r l; do
  t=$(readlink "$l" 2>/dev/null); case "$t" in *"/.claude/skills/"*) printf '%s\t%s\n' "$t" "$l";; esac
done > /tmp/hf-links.tsv

# 2. remove ONLY links created by the run (mtime-gated, so the 2026-08-18 fanout survives)
cut -f2 /tmp/hf-links.tsv | while read -r l; do
  [ "$(date -u -r "$l" +%F)" = "<run-date>" ] && rm -- "$l"
done

# 3. drop the empty placeholder dirs the run created
for d in /root/.claude/skills/*/; do
  [ -L "${d%/}" ] && continue
  [ -z "$(ls -A "$d")" ] && [ "$(date -u -r "$d" +%F)" = "<run-date>" ] && rmdir "$d"
done
```

`rmdir` (never `rm -rf`) is the safety: it refuses any directory that still has content, so real
skill files cannot be lost.

`init` also writes `AGENTS.md` and `CLAUDE.md` (identical, 8 KB) into the new project. Both are
agent instruction files, not build config — review them before they reach a repo you care about.

## Smoke test — passed 2026-09-27

Full end-to-end run at `noesis_content/videos/hyperframes-smoke-test/` on this host, CLI v0.8.81:

| Step | Result |
| --- | --- |
| `doctor` | green on Node, FFmpeg, FFprobe, Chrome headless shell, whisper-cpp |
| `init . --example kinetic-type --non-interactive` | exit 0 |
| `check` | 0 errors; 1 layout warning + 5 info on the stock template; 14/14 contrast pass |
| `render` | 9.3 MB, 15.0s, 450 frames, **21.4s wall clock** (6 workers, software GPU) |

Audio was muxed and is real: `hasAudio: true` in the render trace, `volumedetect` mean -21.8 dB,
max -4.4 dB. Four frames pulled at t=1/5/9/13s all carry live motion and per-frame change, so the
MP4 is genuine output and not a black or frozen render.

Use this as the baseline: **a 15s composition renders in about 20 seconds on CPU.** Anything much
slower means something is wrong, not that the machine is slow.

The smoke-test folder is a throwaway. Delete it when it stops being useful.

## Removal (TRIAL)

## Removal (TRIAL)

```bash
rm -rf /home/workspace/Skills/hyperframes
```
