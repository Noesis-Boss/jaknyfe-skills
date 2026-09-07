# Budget — MCP Catalog & Trust Gateway
**Date:** 2026-09-07 · **Stage:** S3 · **Paper only — nothing purchased.** Per mission constraint: ASSUMPTIONS are shown strictly separately from CONFIRMED costs. Every cost figure carries a source + date; unverified prices are stated as unverified rather than guessed.

---

## CONFIRMED costs (incurred or verified-$0)

| Item | Cost | Basis |
|---|---|---|
| Spend to date (S1–S3, all stages) | **$0** | Paper-only constraint held across all stages; nothing sent, published, or purchased. Verified by this session's logs. |
| Source control + releases | $0 | GitHub Free tier covers public repo, issues, actions for an OSS project — [github.com/pricing](https://github.com/pricing) (accessed 2026-09-07). |
| Runtime / language / DB | $0 | Bun, TypeScript, SQLite-class local persistence — open source, no licenses. Existing local machine. (Verified in `Projects/mcp-catalog-gateway/package.json`, 2026-09-07.) |
| Registry data — official MCP Registry | $0 | Public read API, no auth for reads — [registry.modelcontextprotocol.io/docs](https://registry.modelcontextprotocol.io/docs) and [registry-authorization.md](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/registry-authorization.md) ("remains public for reading") (accessed 2026-09-07). |
| Registry data — PulseMCP Sub-Registry | $0 for documented read API | API docs publicly documented; **partner/enriched tier pricing is NOT published** — see assumptions. [pulsemcp.com/api](https://www.pulsemcp.com/api) (accessed 2026-09-07). |
| Hosting — 90-day build window | $0 incremental | Local-first architecture (README principle: "No paid catalog dependency"); runs on already-owned infrastructure. (Project README, accessed 2026-09-07.) |

**Total confirmed spend: $0.**

---

## ASSUMPTIONS (not incurred; require Don's approval + price verification before any purchase)

| Item | Assumption | Status of figure |
|---|---|---|
| Custom domain (optional; only if a hosted docs page ships post-day-90) | Registrar list price — **NOT verified this session** | No figure asserted. Per constraint, price will be sourced from a registrar page and dated **before** any approval request. |
| PulseMCP enriched/partner API tier (only if the documented public API proves insufficient) | May require partner terms; their API page says partners should "reach out" — pricing unpublished | **Price unknown** — [pulsemcp.com/api](https://www.pulsemcp.com/api) (accessed 2026-09-07). Treated as potentially paid; not budgeted. |
| Paid scanner feeds / commercial security data | None budgeted in 90-day plan — design consumes only free/published scan output (MCP-Scan OSS, mcp-audit OSS) | $0 by design; any paid feed would be a future stage decision. (Sources: [invariantlabs.ai/blog/introducing-mcp-scan](https://invariantlabs.ai/blog/introducing-mcp-scan); [github.com/adudley78/mcp-audit](https://github.com/adudley78/mcp-audit), both accessed 2026-09-07.) |
| Paid ads / promotion | None | $0 by design — distribution via OSS, X, HN, and direct outreach only. |

**Assumption ceiling for the 90-day plan: $0 required.** Optional items above are deliberately unbudgeted until priced with a dated source.

## Cost-risk note
The plan is structured so that no milestone depends on an unpaid-for external resource: Phase 1 uses only the officially public read API; Phase 2 consumes only free/open-source scan output; Phase 3 distribution channels (GitHub, X, HN) are free. If a registry API changes terms mid-plan, the kill-check in `final/launch-plan.md` Phase 1 applies (escalate to Don before workarounds).
