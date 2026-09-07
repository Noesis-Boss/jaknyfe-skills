# Opportunity 1: Solo-Dev MCP Security Scanner & Allowlist CLI
**Recorded:** 2026-09-06 · Paper only · Sources as cited

## The wedge
A local-first, offline CLI that scans a developer's installed MCP server configs, flags tool-poisoning/supply-chain risks, maps findings to the OWASP MCP Top 10, and enforces an explicit allowlist — sold free/open-source with paid team tier.

## Evidence for
- 33% of 1,000 scanned MCP servers had critical vulnerabilities (Enkrypt AI, Oct 2025); SSRF in 36.7% of 7,000+ servers (BlueRock, 2026). [practical-devsecops.com](https://www.practical-devsecops.com/mcp-security-statistics-2026-report)
- Existing scanners are noisy: ~78% false-positive rate found in one audit of YARA-based MCP scanners (AppSec Santa, April 2026) — a quality gap. Same source.
- mcp-audit (open-source, offline, OWASP-MCP-mapped) already validates demand for this exact shape. [blog.devgenius.io](https://blog.devgenius.io/i-built-an-open-source-security-scanner-for-mcp-servers-heres-why-f2842acfbc64)

## Evidence against
- Crowded: MCP-Scan (Invariant), ScanMCP, Akto, Cycode, StackHawk, MintMCP, MCP Total already ship scanning/guardrails. [akto.io](https://www.akto.io/blog/mcp-security-tools), [mcpmanager.ai](https://mcpmanager.ai/blog/mcp-security-tools)
- Solo devs rarely pay for scanners; the paying buyer is enterprise, which buys gateways (from €690) with EDR/inventory. [optimum-web.com](https://www.optimum-web.com/blog/mcp-server-supply-chain-trust-gap)
- mcp-audit is free, Apache 2.0, offline, CI-integrated — hard to differentiate a second free CLI.

## Fit with operator constraints
- ~60 min/day, $0 capital: CLI buildable. But differentiation requires security research depth (CVE-class analysis) that a solo operator can't sustain credibly.

## Verdict (S2 input)
Real pain, low willingness-to-pay solo, heavy incumbents. **Not the pick** — kept as comparison.
