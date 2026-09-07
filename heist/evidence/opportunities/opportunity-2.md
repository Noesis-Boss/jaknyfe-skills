# Opportunity 2: MCP Catalog & Trust Gateway (discovery + vetting + allowlisted execution)
**Recorded:** 2026-09-06 · Paper only · Sources as cited

## The wedge
A local catalog/gateway that (a) mirrors official/community MCP registries into SQLite, (b) layers security metadata (CVE notes, tool-description risk, maintainer signals) onto every entry so "listed" ≠ "trusted", and (c) executes only allowlisted tools behind local auth — a personal trust layer for MCP tool selection.

## Evidence for
- Discovery is fragmented: registry counts disagree wildly (5,000 vs 10,000+ vs 20,980 servers across PulseMCP/MCP Market/official), and no source provides per-server trust metadata. [callsphere.tech](https://callsphere.tech/blog/mcp-ecosystem-5000-servers-model-context-protocol-production-guide-2026), [marsdevs.com](https://www.marsdevs.com/blog/model-context-protocol-mcp), [mcpmarket.com](https://mcpmarket.com/categories/developer-tools?page=133)
- "Registry presence is not a signal of safety" (Feb 2026 case); guidance is explicit allowlists — exactly this product's core mechanic. [optimum-web.com](https://www.optimum-web.com/blog/mcp-server-supply-chain-trust-gap)
- Anthropic's own 2026 roadmap includes a curated verified registry with security ratings — validating the need, but targeting enterprise, not local/personal use. [digitalapplied.com](https://www.digitalapplied.com/blog/mcp-97-million-downloads-model-context-protocol-mainstream)
- Tool census: 177,436 tools by Feb 2026 (35x in ~13 months) — discovery/triage load grows with it. [micheallanham.substack.com](https://micheallanham.substack.com/p/the-state-of-the-model-context-protocol)
- Operator head start: `mcp-catalog-gateway` already scaffolded (registry sync + SQLite persistence, catalog_search/catalog_stats MCP server, CLI allowlist add/remove/list, bearer auth on refresh/execution) with passing tests — see workspace memory, 2026-09-07 entries. This is 20–30% of the product already built.

## Evidence against
- Anthropic's verified registry could absorb the trust-metadata layer for free. [digitalapplied.com](https://www.digitalapplied.com/blog/mcp-97-million-downloads-model-context-protocol-mainstream)
- Monetization unproven: adjacent gateways charge €690+ (enterprise framing); personal-tier pricing untested. [optimum-web.com](https://www.optimum-web.com/blog/mcp-server-supply-chain-trust-gap)

## Fit with operator constraints
- Strong: local-first (no hosting cost), reuses existing scaffold and skills, ~60 min/day compatible, open-source-friendly distribution (GitHub + npm), premium tier optional later.

## Verdict (S2 input)
Fastest path from existing assets to a differentiated product in the hottest sub-segment. **Recommended pick.**
