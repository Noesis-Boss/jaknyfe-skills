---
name: public-equity-investing
description: Public-equity research lifecycle for listed companies - tearsheets, DCF and comps valuation, three-statement and operating models, earnings previews and deep dives, catalysts, scenario sensitivity, thesis tracking, memos, decks, and meeting prep, with XLSX and DOCX artifacts. Use when the user asks to research a ticker, value a company, analyze earnings, build or audit a financial model, write an investment memo or pitch, or prep for an earnings call or investor meeting. Installed as a TRIAL of the OpenAI-curated Codex plugin bundle.
compatibility: Created for Zo Computer. Python 3.12 with openpyxl/python-docx available. 23 bundled skills.
metadata:
  author: jaknyfe.zo.computer
  upstream: https://github.com/openai/plugins/tree/main/plugins/public-equity-investing
  install_type: trial
---

# Public Equity Investing (Zo adapter)

Zo router for the OpenAI-curated `public-equity-investing` bundle: 23 skills covering the
listed-company research lifecycle from idea triage through valuation, modeling, and the written
deliverable. This is a **TRIAL install** — see `Skills/TRIAL-openai-plugins.md` for scan results
and removal instructions.

## What lives here

Vendored at `plugin/` (4.0 MB, includes `shared/` and `tests/`). Read the upstream skill file
before running a workflow — each carries its own section structure, model conventions, and output
format.

Full path pattern: `/home/workspace/Skills/public-equity-investing/plugin/skills/<skill>/SKILL.md`

### Entry and routing

| Skill | Use for |
| --- | --- |
| `public-equity-investing` | Entry point; routes a request to the right workflow |
| `user-context` | Initialize / inspect / save / reset user preferences and context |

### Research and idea generation

| Skill | Use for |
| --- | --- |
| `idea-generation` | Triage idea candidates. Not final trade recommendations |
| `company-tearsheet` | Source-backed issuer tearsheets |
| `initiating-coverage` | Full initiating-coverage reports |
| `thesis-tracker` | Build or update a thesis tracker |
| `meeting-prep` | Meeting / call prep briefs |
| `economic-impact-report` | Translate an event, policy change, or macro shock into equity impact |

### Valuation and modeling

| Skill | Use for |
| --- | --- |
| `financials-normalizer` | Normalize financials from source materials |
| `three-statement-model-builder` | Banker-formula three-statement operating model workbook |
| `dcf-model-builder` | DCF valuation workbooks |
| `comps-valuation` | Comparable-company valuation, report or workbook mode |
| `equity-model-update` | Safely update an existing model copy from a source-to-model map |
| `model-audit-tieout` | Audit existing models / spreadsheets (not build new ones) |
| `scenario-sensitivity-generator` | Turn a base case into scenario skew and sensitivity tables |
| `portfolio-risk-management` | Position sizing, equity hedges, integrated risk |

### Events and earnings

| Skill | Use for |
| --- | --- |
| `earnings-preview` | Full pre-earnings preview with expectation bar and guidance |
| `earnings-deep-dive` | Post-results analysis from results, guidance, transcript, call |
| `catalyst-calendar` | Catalyst calendars (not full event underwriting) |
| `event-driven-analyzer` | Dated event paths, probabilities, payoffs, expected returns |

### Written deliverables

| Skill | Use for |
| --- | --- |
| `memo-builder` | Formal investment memos |
| `long-short-pitch` | PM-facing trade pitches |
| `deck-report-qc` | First-pass QC on decks or reports before circulation |

## How to work in Zo

1. **Read the upstream skill first.** Each of the 23 declares its own scope and its own
   "do not use for" boundary. Respect those — the upstream author is explicit that e.g.
   `model-audit-tieout` audits but does not build, and `deck-report-qc` is a first pass, not
   external-circulation clearance.
2. **Artifacts belong in the user's workspace**, not in this skill directory. Write models,
   tearsheets, and memos under `/home/workspace/` — for equity work, prefer a project folder such
   as `/home/workspace/equity/<TICKER>/`. The user needs to open and download these.
3. **Sources must be real.** Every tearsheet, model, and deep dive is source-backed by design.
   Do not fabricate figures, cite SEC filings that were not actually retrieved, or fill in a
   financial model with invented numbers. The user runs a live trading bot; wrong inputs here
   propagate into real decisions.
4. **Related local work already exists.** The `clarion-*` skills cover regime, SEC research,
   single-stock eval, expected return, screener, and thesis monitoring. Prefer those for the
   *systematic/portfolio* layer and this bundle for the *single-name deliverable* layer
   (tearsheet, model, memo, deck). Say which one you are using.
5. **Excel output.** Models are XLSX built with openpyxl. Verify the file opens and the formulas
   compute before declaring it done; a workbook with `#REF!` is worse than no workbook.

## Codex → Zo deltas

- No Codex plugin loader here. The bundle is read from the filesystem; pass absolute paths.
- The plugin manifest declares no license field; the upstream repo root has **no LICENSE file**.
  Treat it as reference code — do not redistribute it or publish derived bundles.
- `plugin/tests/` contains ~50 MEDIUM `subprocess` findings under the local security gate. These
  are openpyxl/python-docx test harnesses, not a real risk. Do not re-report them as a finding
  every run.

## Prerequisites

Python 3.12 with `openpyxl` and `python-docx` available on the Zo host. No install step required.
