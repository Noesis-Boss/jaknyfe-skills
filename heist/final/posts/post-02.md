# Post 02 — Security framing (Phase 2: Trust)
**Surface:** X · **Status:** DRAFT — not published; requires Don's approval · **Hook provenance:** hook-generator run 2026-09-07, contrarian variant "The thing the MCP crowd won't say out loud: the game changed in the last 73 months." — injected number replaced with "sixteen months" to match the cited source's own growth window; no other changes.

---

The thing the MCP crowd won't say out loud: the game changed in sixteen months.

Tool descriptions are supply-chain assets now — Microsoft formally classified them that way in June 2026 ([labs.cloudsecurityalliance.org](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-tool-poisoning-auto-execution-20260701), accessed 2026-09-06).

What that looks like in practice:

- SSRF exposure in 36.7% of 7,000+ servers scanned (BlueRock, 2026) ([practical-devsecops.com](https://www.practical-devsecops.com/mcp-security-statistics-2026-report), accessed 2026-09-06)
- CVE-2026-33032 ("MCPwn"), CVSS 9.8, actively exploited, patched 2026-03-15 (same source)
- OWASP's MCP Top 10 ranks tool poisoning #3 (MCP03) ([cycode.com](https://cycode.com/blog/owasp-mcp-top-10), accessed 2026-09-06; corrected in S4 audit — the source's table lists Tool Poisoning as MCP03, and labs.cloudsecurityalliance.org calls it the "third entry")

You'd never run an npm package with an unaudited postinstall script. Tool descriptions deserve the same suspicion.

**Sources (attach as reply when approved):** the three links above, with access dates.
