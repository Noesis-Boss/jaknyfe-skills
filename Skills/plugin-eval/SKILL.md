---
name: plugin-eval
description: Evaluate a local skill or plugin bundle and explain why it scored that way, what to fix first, and what the findings mean. Use when the user says "evaluate this skill", "eval this repo", "review this plugin", "why did this score low", or wants a rewrite brief for a skill that failed. Installed as a TRIAL of the OpenAI-curated Codex plugin bundle.
compatibility: Created for Zo Computer. Node.js >=20 required for the CLI.
metadata:
  author: jaknyfe.zo.computer
  upstream: https://github.com/openai/plugins/tree/main/plugins/plugin-eval
  install_type: trial
---

# Plugin Eval (Zo adapter)

Zo router for the OpenAI-curated `plugin-eval` bundle: a Node CLI that scores local skills and
plugins against a rubric and emits schema-conformant findings. This is a **TRIAL install** — see
`Skills/TRIAL-openai-plugins.md` for scan results and removal instructions.

## What lives here

Vendored at `plugin/`. Read the upstream skill file before running a workflow:

| Skill | Upstream file | Use for |
| --- | --- | --- |
| `plugin-eval` | `plugin/skills/plugin-eval/SKILL.md` | Entry point; routes to the right evaluation workflow |
| `evaluate-skill` | `plugin/skills/evaluate-skill/SKILL.md` | Evaluate one local skill |
| `evaluate-plugin` | `plugin/skills/evaluate-plugin/SKILL.md` | Evaluate a whole local plugin bundle |
| `improve-skill` | `plugin/skills/improve-skill/SKILL.md` | Turn findings into a concrete rewrite brief, then re-evaluate |
| `metric-pack-designer` | `plugin/skills/metric-pack-designer/SKILL.md` | Design custom local metric packs / rubrics |

Full path pattern: `/home/workspace/Skills/plugin-eval/plugin/skills/<skill>/SKILL.md`

## Running the CLI

```bash
cd /home/workspace/Skills/plugin-eval/plugin
node scripts/plugin-eval.js --help

# Chat-first entry point — start here for almost anything
node scripts/plugin-eval.js start <path> --request "evaluate this skill" --format markdown

# Direct evaluation
node scripts/plugin-eval.js analyze <skill-or-plugin-path> --brief-out /tmp/brief.json
```

Other verbs: `report`, `compare`, `explain-budget`, `measurement-plan`, `init-benchmark`,
`benchmark`. `guide` is a legacy alias for `start`; `recommend-measures` is a legacy alias for
`measurement-plan`.
No install step is required — the CLI is dependency-free; run it with `node`, not a package runner.

## How to work in Zo

1. **Evaluate with the CLI, report with judgment.** The score is a rubric output, not a verdict.
   Always state the actual findings and the specific files/lines involved, and say plainly when a
   high score is volume-driven (a large test-heavy Python bundle accumulates dozens of MEDIUM
   `subprocess` findings) rather than a real risk.
2. **Cross-check against the local security gate.** `Skills/skillspector/scripts/skillspector-run.sh`
   is already installed here and is the standing pre-install gate. Running both and reconciling is
   the expected workflow, not a duplicate.
3. **`improve-skill` is broken on this machine.** Its step 3 hardcodes
   `/Users/benlesh/.codex/skills/skill-creator/SKILL.md` (a macOS path from the original author).
   That file does not exist here. Skip that step, or substitute a locally available
   `skill-creator` if one exists under `/home/workspace/Skills/`.
4. **Do not push plugin-eval findings straight to GitHub.** Any change to a skill under
   `/home/workspace/Skills` must pass gitleaks and be committed to
   `Noesis-Boss/jaknyfe-skills` per the user's standing rule.

## Codex → Zo deltas

- No Codex `AGENTS.md`-level plugin loader exists here. The CLI takes a filesystem path, so pass
  paths directly (e.g. `/home/workspace/Skills/skillspector`).
- The upstream repo root has **no LICENSE file**, and `plugin/package.json` is `private: true`
  with no license field. Treat it as reference code; do not fork or redistribute it.

## Prerequisites

- Node >= 20 (this machine: v26.9.0 — satisfied). No Python needed.

## Removal (TRIAL)

```bash
rm -rf /home/workspace/Skills/plugin-eval
```
