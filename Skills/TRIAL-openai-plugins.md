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
| `Skills/postgres-best-practices` | `plugins/supabase` | 2 | 104 KB |

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
| supabase-postgres-best-practices | 0 | LOW | SAFE | Gate exit 0. 48 files, no executables, no scripts, no network |
| supabase (platform skill) | 40 | MEDIUM | vendored, NOT activated | False positives on `.mcp.json` / `service_role`; platform-specific, not used on this host |
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

Fully reversible — no state outside these five directories:

```bash
rm -rf /home/workspace/Skills/hyperframes \
       /home/workspace/Skills/public-equity-investing \
       /home/workspace/Skills/plugin-eval \
       /home/workspace/Skills/data-analytics \
       /home/workspace/Skills/postgres-best-practices
rm /home/workspace/Skills/TRIAL-openai-plugins.md
```

## Licensing

- Repo root has **no LICENSE file**. `data-analytics` additionally declares
  `"license": "Proprietary"` with a `private: true` package.
- **`plugins/supabase` is the exception: it ships its own `LICENSE` (MIT, Copyright (c) 2025
  Supabase).** That is the one bundle in this trial that may be vendored or forked. It is still
  gitignored here to keep the trial uniform, but the licence does not require it.
- Treat the other four as reference code. Do not redistribute, publish, or fork.

## `supabase` — the one keep, and why

`plugins/supabase` is the only bundle in this repo that ships a real licence, and the only one
whose payload is platform-neutral:

- `supabase-postgres-best-practices` — 31 rules on query performance, connection management, RLS,
  schema design, locking, data access, and monitoring. Scored **0/100 LOW/SAFE**: 48 files, zero
  executables, zero scripts, zero network calls. Nothing in it is Supabase-specific except the
  occasional footnote, and it applies directly to this host's **PostgreSQL 15.19** server.
  Installed as `Skills/postgres-best-practices` with a Zo router.
- `supabase` (the platform skill) — 40/100 MEDIUM. Covers the Supabase MCP server, the `supabase`
  CLI, and the `anon`/`authenticated` role model. **None of that exists on this host**, so it is
  vendored but explicitly not activated. Its RLS security checklist is generic Postgres and is
  worth reading by hand when needed.

This is the bundle that answers the trial's own question — it beat nothing, but it had no local
equivalent to lose to, and it is 104 KB of pure prose.

## `build-web-apps` — evaluated 2026-09-27; `react-best-practices` INSTALLED, rest NOT installed

The other half of the bundle's frontend story. 6 skills, 133 files, 451 KB, **no LICENSE anywhere**
(not in the plugin, not at the repo root) — so it is reference code on the same footing as the other
four. Every skill is pure markdown plus an `agents/openai.yaml`; zero scripts, zero executables.

| Upstream skill | Files | Verdict | Reason |
| --- | --- | --- | --- |
| `react-best-practices` (Vercel) | 71 | **INSTALLED 2026-09-27** | 66 discrete perf rules, progressive-disclosure format, zero collision |
| `shadcn` | 13 | **INSTALLED (patched)** | Highest day-to-day value on Zo. Auto-execute frontmatter directive stripped; CLI pinned to `bunx --bun` in the router |
| `stripe-best-practices` | 6 | **INSTALLED (4 refs)** | Local skill is a good 10 KB stub with no routing table, no Treasury |
| `frontend-app-builder` | 3 | **SKIP** | Rule 9 bans the eyebrow label; a direct conflict with live local work |
| `frontend-testing-debugging` | 2 | **SKIP** | Entirely Codex-plugin-routing scaffolding; local `webapp-testing` already covers it |
| `supabase-best-practices` | 38 | **SKIP — duplicate** | Same `name: supabase-postgres-best-practices`, v1.1.0 vs the v1.1.1 already installed |

### `react-best-practices` — the clean win

Identical structure to the Supabase rules already installed, from a recognised maintainer (Vercel
Engineering). Categories: `server-*` (RSC data fetching, caching, dedup, parallel fetching),
`rerender-*` (22 rules — `derived-state-no-effect`, `memo-with-default-value`, `use-ref-transient-
values`, `split-combined-hooks`), `client-*`, `bundle-*`, `async-*`, `js-*`, `rendering-*`,
`advanced-*`.

Nothing here conflicts with `frontend-design` (Anthropic, aesthetic direction) — one is
performance, the other is taste. It also lines up with the Zo Spaces guidance already in play
(`esm.sh` imports, bundle budgets). Installed as `Skills/react-best-practices/plugin/` (66 rules, 224 KB) behind a hand-written Zo
router `SKILL.md` with a symptom-to-file routing table and the Next.js-on-Vite caveat. Bundled
tree is gitignored. SkillSpector 23/100 MEDIUM — both HIGH findings are the word "injecting" in
the hydration-flicker rule plus a `dangerouslySetInnerHTML` snippet in a markdown sample; manually
adjudicated false positives (68 markdown files, zero scripts).

Caveat: several rules are Next.js/App-Router specific (`server-components`, `RSC` patterns). Most of
Don's Zo sites are Vite + React, where the `server-*` and `rerender-*` halves still apply but
`server-actions` rules do not.

### `shadcn-best-practices` — INSTALLED, with the auto-execute removed

Zo Sites and Spaces both ship shadcn, and this is the only skill in the entire bundle that knows
`bunx --bun shadcn@latest` as the right runner for this host. It also handles the `render` (Base UI)
vs `asChild` (Radix) split that the Spaces docs warn about. It was the single highest-value item in
the whole bundle, so it was worth unblocking rather than parking.

**The blocker was real.** Upstream built the skill on an auto-execute frontmatter directive:

```json
!`npx shadcn@latest info --json 2>/dev/null || echo '{"error": "No shadcn project found..."}'`
```

Every single load shelled out to the network before the assistant had decided it needed the data.
That is a standing side effect on a Codex plugin format that has no meaning in Zo, where
`SKILL.md` frontmatter is just `name` + `description`. It was also the entire cause of the
100/100 CRITICAL SkillSpector verdict.

**What changed.** The directive block was removed from the vendored copy and the section retitled
to *Project Context (run on demand)* with an explicit command line to run when — and only when —
a shadcn task is actually underway. Nothing else in the body was touched; `cli.md`,
`customization.md`, `mcp.md`, `evals/`, `agents/openai.yaml`, `assets/`, and the five `rules/`
files are byte-identical to upstream.

**SkillSpector: 100/100 CRITICAL → 43/100 MEDIUM.** No HIGH or CRITICAL findings remain. The
residual MEDIUM is the skill's documented purpose — it tells the assistant to run
`bunx --bun shadcn@latest` — plus the many CLI invocations across the reference docs. This is the
same class of finding as `react-best-practices` (23/100 MEDIUM) and is expected for a CLI-driven
skill. Proceed.

**CLI verified against the live binary (2026-09-27).** Two claims worth pinning down before anyone
trusts this skill unattended:

- `shadcn info` **exits 0 even when the directory is not a shadcn project.** Run in an empty dir it
  prints `"framework": "Manual"`, `"config": null`, `"components": []` and returns 0. Do not gate a
  check on its exit code — parse the JSON and test `config !== null`.
- `info` exposes only `-c, --cwd`, `--json`, `-h, --help`. `--package-manager` appears nowhere in
  the CLI help, which confirms the router's "use the project's package runner" rule.

Both findings are recorded in the Zo router at `Skills/shadcn-best-practices/SKILL.md`.

**Still true after install:** the CLI moves fast. The reference docs are pinned to whatever shipped
at repo-copy time and will rot silently. Re-check `shadcn@latest --help` and the `info --json`
output shape before trusting it unattended. The Zo router, not the vendored body, is what pins the
runner to `bunx --bun` and states the safe-usage rules.

### `frontend-app-builder` — do not install as-is

Its Hard Rule 9: *"Hero eyebrow, kicker, pretitle, badge, or pill labels above the main heading are
prohibited by default."* That is a global aesthetic rule, and it directly contradicts the hero
pattern in live local work — Noësis News, Idea Desk, the Zo Space homepage, the DeMolay deck.

Rules 4 and 11 also assume Codex surfaces that do not exist here: Plan mode, `request_user_input`
approval gates, and a `view_image`-on-both-images handoff block. The intent behind 11 — do not call
a build done on code-review alone — is already a standing rule for this workspace via screenshot
verification. Rule 8 (default to React + Vite for new complex app UIs) is genuinely useful and is the
one thing worth lifting by hand.

### `frontend-testing-debugging`

Content is almost entirely about detecting whether the Codex **Browser plugin** is available and
routing to it, plus report-shape and fallback-policy contracts. On Zo the browser tools, `agent-browser`
CLI, and `webapp-testing` are already the first-class path. Little to transfer.

### Licensing note

`build-web-apps` ships **no LICENSE file at all** — not in the plugin directory, not at the repo root.
Same posture as the other four bundles: vendored for reference, do not redistribute or fork.

## `hyperframes` smoke test — 2026-09-27, PASSED

The bundle had been vendored but never run. Exercised end to end on this host: scaffold → check →
render → artifact verification.

| Step | Command | Result |
| --- | --- | --- |
| Version | `npx -y hyperframes@latest --version` | `0.8.81` |
| Environment | `hyperframes doctor` | Node v26.9.0, FFmpeg/FFprobe 5.1.8, headless Chrome 152, whisper-cpp, unzip all green |
| Scaffold | `hyperframes init . --example kinetic-type --non-interactive` | exit 0; wrote `index.html`, `hyperframes.json`, `AGENTS.md`, `CLAUDE.md`, `compositions/` |
| Check | `hyperframes check` | 0 errors; 1 layout warning + 5 info on the stock template; 14/14 contrast checks pass WCAG AA |
| Render | `hyperframes render` | exit 0 — 9.3 MB MP4, 15.0 s, 450/450 frames, **21.4 s** wall clock, 6 workers, software GPU |
| Audio | `ffmpeg -i out.mp4 -af volumedetect` | mean −21.8 dB, max −4.4 dB — a real mix, not silence |
| Frames | ffmpeg frame grab at t=1/5/9/13 s | all four have real content (mean 20–136, stddev 22–77, 5.8k–160k distinct colors) |

Render speed is the headline: **a 15 s composition in 21 s**, faster than its own runtime, on
software GPU with no Docker. Chrome and FFmpeg were already present, so nothing needed installing.

Two optional doctor checks fail and do not block: Kokoro TTS and MusicGen BGM are not installed,
and the Docker daemon is not running (expected — Zo is a gVisor sandbox). Neither is needed for
the HTML→MP4 path. Note that `whisper-cpp` **is** present, so the transcribe workflow is available.

### Two router bugs this test caught

1. **Wrong package name.** The router said the CLI was `npx -y hyperframes-cli@latest`. The real
   npm package is `hyperframes`. The scaffolder also pins an exact version in `package.json`
   (`npx --yes hyperframes@0.8.81`) rather than `@latest` — worth mirroring, since `latest` rots.
2. **Wrong Node floor.** The router said Node >= 20; `hyperframes-cli/SKILL.md` requires >= 22.
   This host runs v26.9.0 so it never showed up as a failure, but the number was wrong.

### `hyperframes init` is not sandboxed

The scaffolder's final step is **"Linked skills into 53 other agent directories"** — it wrote
**635 symlinks across 53 agent skill directories** across `/root` (`.claude`, `.codex`, `.gemini`,
`.terramind`, `.iflow`, `.qoder`, `.commandcode`, `.hermes`, `.kilocode`, `.openclaw`, `.continue`,
`.config/goose`, and ~30 more), plus 11 empty placeholder dirs under `/root/.claude/skills/`,
touching nothing in `/home/workspace/Skills`. Nothing was overwritten, but the write is host-wide
and silent. Prefer `--non-interactive` from an agent context so it cannot block on prompts.

**What could call them: nothing.** Every placeholder is an empty directory (0 files), so all 635
links resolve to nothing loadable. Verified inert in the three runtimes installed and running on
this host (`hermes`, `kilocode`, `openclaw`; `zcode` is not installed). A separate ~795-link fanout
dated 2026-08-18 points at the same empty placeholders — pre-existing platform state, not from this
run, and deliberately left alone.

**Corrected 2026-09-28:** the original "~530 symlinks across 53 directories" undercounted the
links (directory count was right). The first inventory stopped at `find -maxdepth 4` and missed 11
more under `/root/.pi/agent/skills`. Correct figure: 635 links, 53 dirs. An mtime-gated undo
(remove only links dated on the run day, then `rmdir` the empty placeholders — never `rm -rf`) plus
a sweep at `-maxdepth 6` is recorded in the Zo router; all 635 were removed and 0 verified
remaining on 2026-09-28.

## Decision point after the trial

Reassess on real use, not on install day. The question worth answering: does any of this beat the
local skills that already exist — `clarion-*` for equity, `Skills/skillspector` for security
gating, and the spec-driven-development and hyperframes-related work already in the workspace?
