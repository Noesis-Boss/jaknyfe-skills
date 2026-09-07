# Post 05 — Build in public (all phases)
**Surface:** X · **Status:** DRAFT — not published; requires Don's approval · **Hook provenance:** hook-generator run 2026-09-07, curiosity variant "Three people told me the same thing about MCP this week. None of them knew each other." used as-is (batch 2).

---

Three people told me the same thing about MCP this week. None of them knew each other.

Not people, exactly — three independent datasets:

1. Enkrypt AI's scan of 1,000 servers: 33% with critical vulnerabilities (Oct 2025) ([practical-devsecops.com](https://www.practical-devsecops.com/mcp-security-statistics-2026-report), accessed 2026-09-06)
2. BlueRock's scan of 7,000+: SSRF exposure in 36.7% (2026) (same source)
3. An April 2026 audit of MCP scanners: ~78% false-positive rate (same source)

Translation: the ecosystem is dangerous, and the tools measuring it are unreliable.

So I'm spending 90 days building the boring layer between them — a local catalog that mirrors registries, shows trust data with sources, and executes only what I explicitly allowlist. Day 1 status: scaffold exists, 6/6 tests passing, bearer auth on write endpoints.

Milestones every 30 days, receipts every step. Paper rule applies: nothing ships without my review.

**Sources (attach as reply when approved):** link above with access date.
