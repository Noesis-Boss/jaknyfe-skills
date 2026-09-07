# Category Scan: MCP (Model Context Protocol) Developer Tooling
**Scan date:** 2026-09-06 · **Method:** web research (search + article capture) · **Status:** reconstructed S1 input (original S1 run timed out)

## Category definition
Tooling built around the Model Context Protocol (MCP), the open standard (Anthropic, Nov 2024, now Linux Foundation-governed) connecting AI agents to external tools/data. Sub-segments: server registries/discovery, security scanning & allowlisting, gateways/proxies, execution/runway infra, and agent-skills packaging/distribution.

## Why this category (evidence)
- MCP SDK downloads hit **97M/month by March 2026**, up from ~2M at Nov 2024 launch (4,750% growth in 16 months) — infrastructure-grade adoption. [digitalapplied.com](https://www.digitalapplied.com/blog/mcp-97-million-downloads-model-context-protocol-mainstream) (accessed 2026-09-06; article cites March 2026)
- Tool census (UK AI Security Institute / Bank of England): **~5,000 MCP tools (Jan 2025) → 177,436 (Feb 2026), 35x**; cumulative downloads 80K → 14M. [micheallanham.substack.com](https://micheallanham.substack.com/p/the-state-of-the-model-context-protocol) (accessed 2026-09-06; data window Jan 2025–Feb 2026)
- Public MCP registries list **5,000–20,980+ servers** depending on source (MCP Market alone claims 20,980 servers). [callsphere.tech](https://callsphere.tech/blog/mcp-ecosystem-5000-servers-model-context-protocol-production-guide-2026), [mcpmarket.com](https://mcpmarket.com/categories/developer-tools?page=133) (both accessed 2026-09-06)
- Security gap is documented and severe: **33% of 1,000 scanned servers had critical vulnerabilities** (Enkrypt AI, Oct 2025); SSRF in 36.7% of 7,000+ servers (BlueRock, 2026); CVE-2026-33032 "MCPwn" CVSS 9.8 actively exploited, patched 2026-03-15. [practical-devsecops.com](https://www.practical-devsecops.com/mcp-security-statistics-2026-report) (accessed 2026-09-06)
- **Registry presence is not a trust signal** — Feb 2026 case proved listed servers can be unsafe; guidance converges on explicit allowlists. [optimum-web.com](https://www.optimum-web.com/blog/mcp-server-supply-chain-trust-gap) (accessed 2026-09-06)
- OWASP published an **MCP Top 10** (tool poisoning, shadow MCP servers, etc.); Microsoft (June 2026) classifies MCP tool descriptions as supply-chain assets. [cycode.com](https://cycode.com/blog/owasp-mcp-top-10), [labs.cloudsecurityalliance.org](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-tool-poisoning-auto-execution-20260701) (accessed 2026-09-06)
- Scanner quality problem: one independent audit found a **~78% false-positive rate** from YARA-based MCP scanners (AppSec Santa, April 2026) — trust in existing tooling is low. [practical-devsecops.com](https://www.practical-devsecops.com/mcp-security-statistics-2026-report) (accessed 2026-09-06)

## Competitive landscape (quick map)
- **Discovery/catalogs:** PulseMCP, MCP Market, official MCP registry (curated, security ratings on Anthropic 2026 roadmap). Sources above.
- **Security scanning:** mcp-audit (open-source CLI, Apache 2.0, offline, maps to OWASP MCP Top 10) — [blog.devgenius.io](https://blog.devgenius.io/i-built-an-open-source-security-scanner-for-mcp-servers-heres-why-f2842acfbc64) (accessed 2026-09-06); MCP-Scan (Invariant), ScanMCP, Akto, StackHawk remote testing — [akto.io](https://www.akto.io/blog/mcp-security-tools), [stackhawk.com](https://www.stackhawk.com/blog/introducing-remote-mcp-server-testing) (accessed 2026-09-06)
- **Gateways:** MCP Security Gateway **from €690** (Optimum Web listing); MintMCP, MCP Total, Golf.dev. [optimum-web.com](https://www.optimum-web.com/blog/mcp-server-supply-chain-trust-gap), [mcpmanager.ai](https://mcpmanager.ai/blog/mcp-security-tools) (accessed 2026-09-06)
- **Skills packaging/distribution:** skills.sh (Vercel), LobeHub marketplace, vskill, ai-skills CLI (45+ agent sync), prompts.chat registry. [avikmukherjee.me](https://avikmukherjee.me/blog/ai-skills-registry), [lobehub.com](https://lobehub.com/skills/maxcarlson-scripts-agent_skills) (accessed 2026-09-06)

## Scan verdict
Category is growing 35x/year with a documented trust/security vacuum and fragmented discovery. Buyer pain is real (no reliable central trust mechanism), but scanning is crowding fast and enterprise gateways are priced out of solo reach. Three opportunity candidates extracted → `opportunity-1.md` … `opportunity-3.md`.
