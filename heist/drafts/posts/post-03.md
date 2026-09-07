# Post 03 — Scanner skepticism (Phase 2: Trust)
**Surface:** X · **Status:** DRAFT — not published; requires Don's approval · **Hook provenance:** hook-generator run 2026-09-07, contrarian variant "Hot take: the obvious play on MCP is the trap." used as-is (batch 2).

---

Hot take: the obvious play on MCP is the trap.

The obvious play is "run a scanner, trust the verdict." One independent audit of YARA-based MCP scanners found a ~78% false-positive rate ([practical-devsecops.com](https://www.practical-devsecops.com/mcp-security-statistics-2026-report), accessed 2026-09-06).

A verdict without sources is noise. At 78% error, red flags and green lights are both coin flips.

The fix isn't a better scanner. It's a different contract:

1. Every finding links to its source and date.
2. Nothing blocks automatically — a human allowlists.
3. Scan results are inputs to a decision, not the decision.

That's the design I'm building toward. Verdicts are cheap; receipts are the product.

**Sources (attach as reply when approved):** link above with access date.
