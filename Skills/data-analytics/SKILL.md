---
name: data-analytics
description: Metric-backed product and business analysis - KPI design and readouts, metric-movement diagnostics, market sizing, data quality assessment, dashboards, analytical reports, charts, and reproducible SQL or Python notebooks. Use when a decision depends on numbers and the user asks why a metric moved, what KPIs to track, how big a market is, whether a dataset is trustworthy, or for a dashboard, report, chart, or notebook. Installed as a TRIAL of the OpenAI-curated Codex plugin bundle.
compatibility: Created for Zo Computer. Node.js >=20 and Python 3.12. Some workflows need MCP/warehouse integrations that are not connected here.
metadata:
  author: jaknyfe.zo.computer
  upstream: https://github.com/openai/plugins/tree/main/plugins/data-analytics
  install_type: trial
---

# Data Analytics (Zo adapter)

Zo router for the OpenAI-curated `data-analytics` bundle: 15 skills that take a product or business
question from raw data to a shareable dashboard, report, chart, or notebook. This is a **TRIAL
install** — see `Skills/TRIAL-openai-plugins.md` for scan results and removal instructions.

## What lives here

Vendored at `plugin/` (4.8 MB, includes `mcp/`, `src/`, and `tests/`). Read the upstream skill
file before running a workflow.

Full path pattern: `/home/workspace/Skills/data-analytics/plugin/skills/<skill>/SKILL.md`

### Entry and context

| Skill | Use for |
| --- | --- |
| `index` | Entry point; routes broad analytics requests to the right workflow |
| `gather-business-context` | Pull business context from connected or provided sources first |
| `create-data-context` | Create / update / repair the Data Analytics semantic layer |

### Analysis

| Skill | Use for |
| --- | --- |
| `product-business-analysis` | Analyze product or business data to support a decision |
| `metric-diagnostics` | Diagnose why a metric changed or differs from expectation |
| `market-sizing` | TAM / SAM / SOM with transparent assumptions and uncertainty |
| `design-kpis` | KPI frameworks, metric definitions, targets, guardrails |
| `kpi-reporting` | Readouts, scorecards, WBR/MBR/QBR, executive summaries |
| `analyze-data-quality` | Is this data trustworthy enough? grain, freshness, nulls, joins |

### Production

| Skill | Use for |
| --- | --- |
| `build-dashboard` | Source-backed dashboards with filters and QA |
| `build-report` | Answer-first analytical report with charts, tables, caveats |
| `visualize-data` | Design, build, revise, or QA quantitative charts |
| `jupyter-notebooks` | Reproducible SQL or Python notebooks |
| `validate-data` | Pre-share QA on an analysis: sources, calculations, conclusion strength |
| `publish-artifact-to-sites` | Publish a validated report or dashboard through Sites |

## How to work in Zo

1. **Read the upstream skill first.** Each skill declares its own output contract. The bundle is
   opinionated about evidence — it wants a labeled, calibrated answer that separates verified
   drivers from likely contributors from open questions. Do not downgrade that to a confident
   guess.
2. **No connected warehouse is wired up here.** The bundle expects Databricks, BigQuery,
   Snowflake, Amplitude, PostHog, etc. None are connected to this Zo. The realistic inputs are
   local files — CSV, XLSX, Parquet, SQLite/DuckDB under `/home/workspace` — or pasted results.
   Say which source you used and do not imply a live warehouse query you did not run.
3. **Artifacts belong in the user's workspace.** Dashboards, notebooks, and reports go under
   `/home/workspace/`, never in this skill directory.
4. **Verify charts render.** The local security gate flagged a base64 gzipped chart-widget asset
   (`assets/*.html.gz.b64.part*`). If a chart does not render, check the asset was reassembled
   before assuming a code bug.
5. **The repo is proprietary.** `plugin.json` declares `"license": "Proprietary"` and
   `package.json` is `private: true` with no license field. Do not publish or redistribute it.

## Codex → Zo deltas

- `mcp/server.cjs` is the bundle's own MCP server. It is **not** auto-registered as a Zo
  integration. Treat MCP-backed workflows as unavailable unless the user connects the source.
- `publish-artifact-to-sites` targets the Codex Sites tool. In Zo the equivalent is a Zo Site or a
  Space route — use the user's normal publishing path, and follow the screenshot-before-declaring-
  done rule.

## Prerequisites

Node.js >=20 and Python 3.12 on the Zo host. No install step required for the skills themselves.
