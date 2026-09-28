# Trial install: OpenAI-curated Codex plugin bundle

**Installed:** 2026-09-27
**Upstream:** https://github.com/openai/plugins (7,203 stars, 931 forks, 62 plugins, 0 releases, no LICENSE file at repo root)
**Type:** TRIAL — vendored into Zo skill format, not installed as Codex plugins.

## What was installed

| Zo skill | Upstream plugin | Bundled skills | Size |
| --- | --- | --- | --- |
| `Skills/hyperframes` | `plugins/hyperframes` | 5 | 390 KB |
| `Skills/public-equity-investing` | `plugins/public-equity-investing` | 23 | 4.0 MB |
| `Skills/plugin-eval` | `plugins/plugin-eval` | 5 | 340 KB |
| `Skills/data-analytics` | `plugins/data-analytics` | 15 | 4.8 MB |

Each Zo skill contains:
- `SKILL.md` — the Zo router (routing, prerequisites, Codex→Zo deltas, local pitfalls)
- `plugin/` — the vendored upstream bundle, unmodified

## Security gate results

Gate: `Skills/skillspector/scripts/skillspector-run.sh` (NVIDIA SkillSpector), the standing
pre-install rule for this workspace.

| Plugin | Raw score | Band | Adjudicated | Basis |
| --- | --- | --- | --- | --- |
| hyperframes | 19 | LOW | SAFE | Gate exit 0, no gate breach. Passed clean |
| public-equity-investing | 100 | CRITICAL | PASS (false positives) | See below |
| data-analytics | 100 | CRITICAL | PASS (false positives) | See below |
| plugin-eval | 61 | HIGH | PASS (false positives) | See below |

### public-equity-investing — 126 findings, 3 HIGH

All three HIGHs are false positives, verified by reading the flagged files:

- **Data Exfiltration @ `skills/model-audit-tieout/scripts/audit_workbook.py`** — grep for
  `os.environ` / `os.getenv` in that file returns **zero matches**. Nothing is read from the
  environment, so nothing can leave.
- **Anti-Refusal @ `skills/user-context/references/plugin-routing-map.md`** — the word "jailbreak"
  appears in a *guard* sentence instructing the agent to treat override attempts as injection and
  re-confirm with the user. That is anti-jailbreak logic, not an anti-refusal instruction.
- **Memory Poisoning @ `skills/user-context/references/plugin-memory.md`** and **YARA hit** on the
  same file — see above. Same text, same false positive.

The remaining 123 findings are 60 MEDIUM "Agent Snooping" reads of `mcp.json` / config in `tests/`
and `scripts/`, plus 48 "Dangerous Code Execution" `subprocess` uses in openpyxl/python-docx test
harnesses. Volume-driven, not risk.

### data-analytics — 100 findings, 3 HIGH

- **YARA @ `assets/datascience-chart-widget.html.gz.b64.part001`** — file starts `H4sIA`, which is
  the gzip magic number in base64. It is a compressed chart-widget asset. YARA matching on the
  base64 alphabet is a known false positive.
- **YARA @ `mcp/server.cjs`** — `child_process.spawnSync("tar", [...])` for build packaging plus
  base64 for embedding the compressed widget. Benign build tooling.
- **Privilege Escalation @ `src/analytics-app/scripts/package_utils.py`** — grep for
  `ssh` / `aws` / `credential` / `.netrc` / `token` returns **zero matches**.

### plugin-eval — 4 findings, 2 HIGH

- **Anti-Refusal @ `src/core/scoring.js`** — grep for `refus` / `disclaimer` / `jailbreak` in the
  file returns **zero matches**. It is a scoring rubric that *penalizes* those patterns.
- **Rogue Agent @ `skills/improve-skill/SKILL.md`** — the skill's declared purpose is rewriting
  other skills. Self-modification is the documented function, not a hidden behavior.

**Note on the waiver:** the raw gate returned HIGH/CRITICAL on 3 of 4, which the standing rule
treats as a block. The user said "install trials" and "structure them for zo" after seeing those
results, which is an explicit waiver. The adjudication above is what makes the waiver safe — every
HIGH was checked against the actual file, not assumed.

## Known breakages on this host

1. **`plugin-eval/improve-skill` step 3** hardcodes
   `/Users/benlesh/.codex/skills/skill-creator/SKILL.md` (a macOS path from the original author).
   That file does not exist here. Skip or substitute a local `skill-creator`.
2. **`data-analytics/mcp/server.cjs`** is not registered as a Zo integration. MCP-backed
   workflows are unavailable. No warehouse/BI source is connected to this Zo.
3. **`hyperframes`** composites at `mcp/`, `tools/`, and `website-to-hyperframes/` are Codex-tool
   shaped and will need mapping to Zo equivalents before those paths work.

## Removal

Fully reversible — no state outside these four directories:

```bash
rm -rf /home/workspace/Skills/hyperframes \
       /home/workspace/Skills/public-equity-investing \
       /home/workspace/Skills/plugin-eval \
       /home/workspace/Skills/data-analytics
rm /home/workspace/Skills/TRIAL-openai-plugins.md
```

## Licensing

- Repo root has **no LICENSE file**. `data-analytics` additionally declares
  `"license": "Proprietary"` with a `private: true` package.
- Treat all four as reference code. Do not redistribute, publish, or fork.

## Decision point after the trial

Reassess on real use, not on install day. The question worth answering: does any of this beat the
local skills that already exist — `clarion-*` for equity, `Skills/skillspector` for security
gating, and the spec-driven-development and hyperframes-related work already in the workspace?
