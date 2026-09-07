# Outreach List — MCP Catalog & Trust Gateway
**Date:** 2026-09-07 · **Stage:** S3 · **Status:** DRAFT working list. **Nothing has been sent.** Every send requires Don's explicit approval. No emails, DMs, or issues opened.

**Rule compliance:** every target below is verified with a source URL + access date proving the person/org and channel exist. No guessed names or addresses. Openers are drafts only.

---

## 1. PulseMCP (registry maintainer)
- **Who/what:** PulseMCP — MCP server directory (21,950+ servers) with a Sub-Registry API implementing the Generic MCP Registry API spec plus enriched metadata (popularity, security analyses). Verified: [pulsemcp.com/api](https://www.pulsemcp.com/api), [pulsemcp.com/servers](https://www.pulsemcp.com/servers) (accessed 2026-09-07).
- **Why them:** primary secondary-registry mirror target; their enriched metadata model (security analyses as `_meta` extensions) is exactly the trust-layer pattern we're building on. Partnership channel exists on their API page.
- **Channel:** contact route on [pulsemcp.com/api](https://www.pulsemcp.com/api) (they direct partners to reach out there). Also has public GitHub org ([github.com/pulsemcp](https://github.com/pulsemcp/mcp-servers), accessed 2026-09-07).
- **Draft opener:** "Building a local gateway that mirrors registries via the Generic Registry API spec — the PulseMCP Sub-Registry API is the cleanest implementation we've found for a second source. Interested in what breaks when a third party mirrors your enriched `_meta` extensions, and whether that's a use you'd support."

## 2. Official MCP Registry maintainers (modelcontextprotocol org)
- **Who/what:** official MCP Registry at registry.modelcontextprotocol.io; open-source repo [github.com/modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry) (public REST API docs at `docs/reference/api/official-registry-api.md`). Verified (accessed 2026-09-07).
- **Why them:** Phase 1 mirror source. Alignment matters more than promotion — we want their read on aggregator behavior and whether trust/`_meta` extension patterns are welcome upstream. Public repo means GitHub Discussions/Issues are the sanctioned channel.
- **Channel:** GitHub Discussions or Issues on the registry repo (blog post explicitly invites feedback there — [blog.modelcontextprotocol.io](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview), accessed 2026-09-07).
- **Draft opener (GitHub Discussion):** "Built a local aggregator that mirrors the official registry plus secondary registries implementing the Generic API spec, and layers sourced trust metadata on entries. Question for maintainers: are downstream aggregators expected to pass through `_meta` namespaces verbatim, and is there guidance on caching/refresh etiquette for the public API?"

## 3. Invariant Labs (MCP-Scan authors)
- **Who/what:** Invariant Labs — makers of MCP-Scan, open-source MCP security scanner. Verified: [invariantlabs.ai/blog/introducing-mcp-scan](https://invariantlabs.ai/blog/introducing-mcp-scan) (2025-04-11), repo [github.com/invariantlabs-ai/mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) (accessed 2026-09-07).
- **Why them:** precedent match — they already partner with a registry (Smithery integrates MCP-Scan results into server pages; [invariantlabs.ai/blog/smithery-mcp-scan](https://invariantlabs.ai/blog/smithery-mcp-scan), accessed 2026-09-07). Their README publishes a contact for exactly this: registry/registry-like projects integrating scan results should reach out via mcpscan@invariantlabs.ai ([github.com/invariantlabs-ai/mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) README, accessed 2026-09-07). Address is theirs, published by them — not guessed.
- **Channel:** mcpscan@invariantlabs.ai (their published integration-contact address) or GitHub on the mcp-scan repo.
- **Draft opener:** "Building a local MCP catalog gateway that attaches trust metadata to registry-mirrored entries. We'd consume MCP-Scan results as one input (sourced, dated, never auto-blocking — allowlist decisions stay human). Your Smithery integration is the pattern. Is there a supported way to consume scan output programmatically for a local, non-hosted registry?"

## 4. mcp-audit author (adudley78)
- **Who/what:** mcp-audit — free, open-source (Apache 2.0), offline MCP config security scanner mapping findings to the OWASP MCP Top 10. Verified: [github.com/adudley78/mcp-audit](https://github.com/adudley78/mcp-audit) and author's write-up [blog.devgenius.io](https://blog.devgenius.io/i-built-an-open-source-security-scanner-for-mcp-servers-heres-why-f2842acfbc64) (accessed 2026-09-07).
- **Why them:** the author writes that they're building in public and explicitly invites contact from people building in the MCP ecosystem ("open an issue" / LinkedIn). Scanner-signal source for our trust layer; also a design peer on the false-positive problem.
- **Channel:** GitHub issues on the mcp-audit repo (author's stated preferred contact in the write-up).
- **Draft opener (issue):** "Building a local catalog gateway that consumes scanner output as trust metadata with sources — not competing on detection. Would you be open to a stable machine-readable output format from mcp-audit that downstream tools could cite? Happy to conform to whatever exists today and share what we build."

## 5. Smithery (registry that already consumes scanner signal)
- **Who/what:** Smithery — MCP registry that integrated Invariant's MCP-Scan so scan results appear on server registry pages. Verified via Invariant's partnership post: [invariantlabs.ai/blog/smithery-mcp-scan](https://invariantlabs.ai/blog/smithery-mcp-scan) (accessed 2026-09-07).
- **Why them:** the only observed registry already pairing listings with scan results — the closest live precedent to our thesis. Their experience (what worked, what users pushed back on) directly de-risks Phase 2.
- **Channel:** smithery.ai site — contact/docs routes to be confirmed at send time (no email asserted; none verified in this session).
- **Draft opener:** "Watching how Smithery surfaces MCP-Scan results on registry pages — that's the closest precedent to what we're building locally. Question: what did adoption look like once scan verdicts became visible, and did the false-positive noise create support burden? Building the local-first version and would rather learn than repeat."

## 6. MCP Market (registry/marketplace)
- **Who/what:** MCP Market — public MCP server marketplace claiming 20,980+ servers. Verified: [mcpmarket.com](https://mcpmarket.com/categories/developer-tools?page=133) (accessed 2026-09-06, from `heist/evidence/category-scan.md`).
- **Why them:** third mirror source and a scale datapoint for the discovery-fragmentation argument. Lower priority than 1–3; contact only after Phase 1 ships.
- **Channel:** site contact route — to be verified before any send (no address asserted).
- **Draft opener:** "Mirroring public MCP registries into a local trust layer. Interested in whether MCP Market exposes a registry-API-compatible endpoint we can mirror, or whether ingestion is submission-only."

---

## Send-order recommendation (pending Don's approval)
1. mcp-audit author (GitHub issue — lowest friction, public, invites contact)
2. Official registry maintainers (GitHub Discussion — public, sanctioned channel)
3. Invariant Labs (email — published integration address, exact-precedent ask)
4. PulseMCP (partner contact form)
5. Smithery, MCP Market (after Phase 1 demo exists)

**Compliance notes:** channels 1–3 verified this session; Smithery and MCP Market channels deliberately left unverified rather than guessed — verify at send time. All openers are drafts; nothing sent.
