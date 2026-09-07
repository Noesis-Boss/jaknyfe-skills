# Launch Plan: MCP Catalog & Trust Gateway
**Date:** 2026-09-07 · **Stage:** S3 · **Paper only — nothing published, sent, or purchased. All external actions await Don's approval.**

## Positioning
**The local trust layer for MCP: mirror every registry, show trust data with sources, execute only what you allowlisted.**

- **For:** developers and solo operators running AI agents against MCP servers who need discovery + trust + gated execution in one local surface.
- **Against the official MCP Registry** (registry.modelcontextprotocol.io, public REST API, launched in preview 2025-09-08 — [blog.modelcontextprotocol.io](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview), accessed 2026-09-07): it is discovery + namespace verification. It does not mirror multiple registries, attach per-finding sourced security data, or gate execution. We are the aggregator/gating layer above it, not a competitor to it.
- **Against scanners** (MCP-Scan, mcp-audit, etc.): we consume their signal instead of producing findings. Every trust entry cites its source and date; nothing auto-blocks without a human allowlist decision. This sidesteps the scanner-quality trap (~78% false-positive rate found in one audit of YARA-based MCP scanners, April 2026 — [practical-devsecops.com](https://www.practical-devsecops.com/mcp-security-statistics-2026-report), accessed 2026-09-06).
- **Model:** open source, free, distribution-first. Monetization deferred until usage data exists (personal-tier willingness-to-pay is unproven — `heist/final/choice.md`, 2026-09-06).

## Verified starting ground (reconfirmed 2026-09-07)
Scaffold at `Projects/mcp-catalog-gateway/` (~20–30% complete):
- **Tests:** 6/6 pass (`bun test`) — search/ranking, empty query, persistence, paginated registry sync, allowlist management, allowlisted-only execution.
- **Auth:** bearer auth on `POST /catalog/refresh` and `POST /tools/execute` (`src/auth.ts`; `CATALOG_API_TOKEN`); search/health read-only.
- **Surfaces:** MCP stdio server (`catalog_search`, `catalog_stats`), HTTP API, CLI (`catalog`, `allowlist add/remove/list`).
- **Principles in README:** no paid catalog dependency; official registry as public discovery source; execution requires explicit allowlist.

## Timeline (30/60/90, sized for ~60 min/day; each phase gated on the prior one)

### Phase 1 — Mirror (Days 0–30)
1. Sync the official registry via its public REST API (`registry.modelcontextprotocol.io/docs`, accessed 2026-09-07) + one secondary implementing the same Generic Registry API spec (PulseMCP Sub-Registry API — [pulsemcp.com/api](https://www.pulsemcp.com/api), accessed 2026-09-07). Dedupe by server name.
2. Surface `catalog stats` counts per source; ship v0.1.0 to GitHub with README demo.
- **Success criteria:** refresh from ≥2 registries behind bearer auth; deduped catalog ≥500 entries; tests green; CLI output screenshot-verified live.
- **Kill check:** if official API limits block a usable mirror, escalate to Don before workaround.

### Phase 2 — Trust (Days 31–60)
1. Trust-metadata layer: per-entry badges aggregating published scan results / audit data where available; every finding carries source link + date; zero auto-blocking.
2. Ship v0.2.0 with a docs page explaining the sourcing policy.
- **Success criteria:** trust field populated with source-linked data on ≥100 mirrored entries; docs page live; no entry modified without a recorded source.

### Phase 3 — Gate + Distribution (Days 61–90)
1. End-to-end demo: search → trust badge → allowlisted execute (stdin JSON, no shell) → append-only audit log.
2. Distribution: publish the 5-post series (`final/posts/`), open outreach conversations (`final/outreach-list.md`), Show-HN-style post — **only after Don approves each item**.
- **Success criteria:** full demo screenshot-verified; ≥1 substantive reply from a registry maintainer or scanner author; all 5 posts approved in draft before any publish decision.

### Overall kill criteria (honest)
If by day 90 there is no external engagement (zero maintainer/scanner replies, no organic installs) and the demo hasn't landed, park the project and report — do not keep building on a dead channel. Consistent with "ship small, verify, iterate."

## Channels
1. **GitHub** — primary home; README + demo GIF + tagged releases.
2. **X build-in-public** — @jak_nyfe; the 5-post series maps to phases (post files note their phase).
3. **Hacker News / Lobsters** — day-90 show-off post, only with Don's sign-off.
4. **Direct outreach** — registry maintainers and scanner authors per `final/outreach-list.md`.

## Risks carried from selection (mitigations)
- **Platform risk:** official roadmap may absorb aggregation (security ratings) — mitigate: multi-registry mirror + execution gating is not in the official registry's shipped feature set (`heist/final/choice.md`, 2026-09-06).
- **Trust-data quality:** scanner false positives — mitigate: sources per finding, human-in-loop allowlist.
- **Monetization unproven:** free/open during the 90 days; pricing decisions deferred to a future stage with usage evidence.
