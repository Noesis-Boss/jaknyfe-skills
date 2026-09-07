# S2 Decision: Chosen Opportunity
**Date:** 2026-09-06 · **Stage:** S2 (selection & justification) · **Paper only — no external action taken**

## The pick
**Opportunity 2: MCP Catalog & Trust Gateway** — a local-first catalog that mirrors MCP registries, layers trust/security metadata on every server entry, and executes only allowlisted tools behind local auth. Full case: `file 'heist/evidence/opportunities/opportunity-2.md'`.

## Why it beats the other two (named tradeoffs)
1. **vs Opportunity 1 (security scanner CLI):** Both attack the trust vacuum (33% of scanned servers critical-vulnerable, per `category-scan.md`), but scanners are crowded (MCP-Scan, ScanMCP, Akto, mcp-audit — all free) and solo devs don't pay. The catalog gateway *consumes* security signal instead of producing it — lower research burden, and its differentiator (trust metadata + allowlisted execution in one local surface) has no observed direct incumbent. Tradeoff accepted: it depends on registry APIs and scanner signal quality rather than owning the scan.
2. **vs Opportunity 3 (skills distribution):** Skills tooling has stronger brand competitors (Vercel's skills.sh, LobeHub) and zero observed willingness-to-pay; every layer is free. The catalog gateway's adjacent market already prices at €690+ (enterprise gateways), implying value in the trust/gateway layer even if our wedge is the personal tier. Tradeoff accepted: personal-tier pricing is unproven.
3. **Decisive factor — asset leverage:** `mcp-catalog-gateway` already exists in the workspace with registry sync + SQLite persistence, `catalog_search`/`catalog_stats` MCP tools, CLI allowlist management (add/remove/list), and bearer auth on refresh/execution, tests passing (workspace memory, 2026-09-07). Opportunity 2 starts at ~20–30% complete; the others start at zero. With ~60 min/day and $0 capital, this is the only option whose time-to-first-shippable fits the constraint.

## Key risks (with mitigations to address downstream)
- **Platform risk:** Anthropic's 2026 roadmap includes an official curated registry with security ratings (`digitalapplied.com` source in evidence). Mitigation: position as local/aggregator layer that mirrors *multiple* registries and adds execution gating — a feature the official registry doesn't ship.
- **Trust-data quality:** scanner false-positive rates run high (~78% in one audit, `practical-devsecops.com` source). Mitigation: show sources per finding; never auto-block without human allowlist decision.
- **Monetization unproven** at personal tier. Mitigation: launch open-source/free for distribution; defer pricing until usage data exists.

## What each downstream deliverable must contain
- **Launch plan (final/launch-plan.md):** 30/60/90-day milestones gated on the existing scaffold; success criteria per phase (e.g., registry mirror live → trust metadata on N servers → execution gateway demo); all milestones buildable within 60 min/day; explicit "ship small, verify" checkpoints with live-verification steps.
- **5 posts (final/posts/):** each grounded in a cited stat from `category-scan.md` (e.g., 97M SDK downloads/month; 177,436 tools; 33% critical-vuln rate; ~78% scanner false-positive rate); voice: evidence-first, no hype; each post maps to a launch-plan phase.
- **Outreach list (final/outreach-list.md):** targets must be real and verifiable — MCP registry maintainers (PulseMCP, MCP Market), MCP security tool authors (mcp-audit author, Invariant Labs/MCP-Scan), and MCP ecosystem newsletters; each entry needs a source URL + date proving the person/org and contact channel exist. No guessed names or emails (standing rule).
- **Budget (logs/finance.md):** separate ASSUMED vs CONFIRMED costs. Expected shape: $0 infrastructure (local-first, GitHub free tier); assumptions only for domain, optional paid registry API tiers — each flagged as assumption with a source for the list price.
- **Fact verification (approvals.md + evidence):** every factual claim in final/ carries source link + access date; budget items labeled assumed vs confirmed; nothing published, sent, or purchased without explicit human approval.

## Verification status of this decision
- All cited claims carry source URLs and were retrieved 2026-09-06 (see evidence files).
- Operator-asset claims (existing scaffold, tests passing) come from workspace memory dated 2026-09-07 — reconfirm scaffold state before the launch plan freezes milestones.
