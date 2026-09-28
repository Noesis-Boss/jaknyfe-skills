---
name: postgres-best-practices
description: Postgres performance, schema, locking, and RLS guidance maintained by Supabase (MIT). Use when writing or reviewing SQL, designing a schema, adding indexes, debugging slow queries, sizing connection pools, working with row-level security, or tuning a Postgres database. Applies to any Postgres 12+ server, not just Supabase. Installed as a TRIAL of the OpenAI-curated Codex plugin bundle.
compatibility: Created for Zo Computer. No scripts — the vendored plugin is pure markdown. Guidance is version-aware; this host runs PostgreSQL 15.19.
metadata:
  author: jaknyfe.zo.computer
  upstream: https://github.com/openai/plugins/tree/main/plugins/supabase
  license: MIT
  install_type: trial
---

# Postgres Best Practices (Zo adapter)

Zo router for the official Supabase `supabase-postgres-best-practices` skill, vendored from the
OpenAI-curated Codex plugin bundle. This is a **TRIAL install** — see
`Skills/TRIAL-openai-plugins.md` for scan results and removal instructions.

SkillSpector: **0/100, LOW / SAFE** (exit 0). No executable files, no scripts, no network calls.

## What lives here

| Path | What |
| --- | --- |
| `plugin/skills/supabase-postgres-best-practices/SKILL.md` | Upstream router — read first |
| `plugin/skills/supabase-postgres-best-practices/references/*.md` | 31 rules across 8 categories |
| `plugin/skills/supabase/` | Companion Supabase-platform skill (**not** activated by this router — see below) |

**The rule files are the payload.** The upstream `SKILL.md` is a thin index; it deliberately does
not restate the rules. Read the specific rule file before making a change.

## The rules

Read by prefix from
`/home/workspace/Skills/postgres-best-practices/plugin/skills/supabase-postgres-best-practices/references/`

| Priority | Prefix | Rules |
| --- | --- | --- |
| 1 — CRITICAL | `query-` | `composite-indexes` `covering-indexes` `index-types` `missing-indexes` `partial-indexes` |
| 1 — CRITICAL | `conn-` | `idle-timeout` `limits` `pooling` `prepared-statements` |
| 1 — CRITICAL | `security-` | `privileges` `rls-basics` `rls-performance` |
| 2 — HIGH | `schema-` | `constraints` `data-types` `foreign-key-indexes` `lowercase-identifiers` `partitioning` `primary-keys` |
| 3 — MEDIUM-HIGH | `lock-` | `advisory` `deadlock-prevention` `short-transactions` `skip-locked` |
| 4 — MEDIUM | `data-` | `batch-inserts` `n-plus-one` `pagination` `upsert` |
| 5 — LOW-MEDIUM | `monitor-` | `explain-analyze` `pg-stat-statements` `vacuum-analyze` |
| 6 — LOW | `advanced-` | `full-text-search` `jsonb-indexing` |

Upstream reference: <https://www.postgresql.org/docs/current/>

## This host (Zo)

Verified 2026-09-27. Re-check before relying on it.

- **Server: PostgreSQL 15.19.** `psql` client is 18.3 — a version skew; the *server* version
  governs feature availability.
- PG15 means `CREATE VIEW ... WITH (security_invoker = true)` is available, and the `security-`
  rules apply as written.
- Local socket: `/var/run/postgresql:5432`. Superuser access: `sudo -u postgres psql`.
- `bin/postgresql-watchdog.sh` recovers this server every 10 seconds. **Do not stop, kill, or
  restart Postgres** to "fix" a connection error — fix the query or the pool instead.
- Multiple Zo services share this one server (SaaS-Mailer, Twenty, MyPCHousecall, ScholarSearch).
  A load test or `pg_terminate_backend` sweep takes them all down.

## Safe-usage rules for Zo

1. **Back up before DDL.** `pg_dump` first, or work inside a transaction you can roll back:
   `BEGIN; <ddl>; ROLLBACK;`. DDL on this server is not isolated to one service.
2. **Wrap noisy output.** `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements` dumps, and
   `\d+` recursion produce far more than a screen. Route them through
   `bun run /home/workspace/Skills/token-saver/scripts/run.ts <command>`.
3. **Explain before you index.** Run `monitor-explain-analyze.md` first. Most "needs an index"
   problems are a missing predicate sargability fix, not a missing index.
4. **Adding `pg_stat_statements` needs a restart.** Confirm with the user before touching
   `shared_preload_libraries` — the watchdog will fight the restart.
5. **Vacuum/autovacuum changes** are server-wide and affect every service. Read
   `monitor-vacuum-analyze.md` and name the blast radius before changing anything.

## Not activated: `plugin/skills/supabase/`

The bundle also vendors Supabase's platform skill (40/100 MEDIUM, `CAUTION` — the HIGH findings
are the scanner reacting to `.mcp.json` and `service_role` key references, both false positives in
context, but it is genuinely platform-specific). It covers the Supabase MCP server, the
`supabase` CLI, and the `anon`/`authenticated` role model. **None of that exists on this host.**
Its RLS security checklist is generic Postgres and is worth reading manually if you need it:

    /home/workspace/Skills/postgres-best-practices/plugin/skills/supabase/SKILL.md

Do not follow its Supabase CLI or MCP instructions on this box.
