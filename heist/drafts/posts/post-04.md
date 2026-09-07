# Post 04 — What I'm building (Phase 3: Gate + Distribution)
**Surface:** X · **Status:** DRAFT — not published; requires Don's approval · **Hook provenance:** hook-generator run 2026-09-07, contrarian variant "Most advice on MCP is written for people who've never done it." used as-is (batch 4).

---

Most advice on MCP is written for people who've never done it. So here's what I'm actually doing instead of advising.

A local catalog gateway:

1. **Mirrors registries** — official MCP Registry API first ([modelcontextprotocol.io/registry/about](https://modelcontextprotocol.io/registry/about), accessed 2026-09-07), secondary registries implementing the same Generic API spec next.
2. **Attaches trust data with receipts** — every security signal carries its source and date.
3. **Executes only allowlisted tools** — explicit allowlist, bearer-auth endpoints, no shell, audit log.

No paid catalog dependency. No telemetry. Local-first, because your credentials shouldn't leave your machine to check whether a server is trustworthy.

Why the official registry doesn't kill this: it verifies namespaces and publishes metadata. It doesn't mirror multiple registries or gate execution. Different layer.

Repo link goes here when Don approves publishing it.

**Sources (attach as reply when approved):** links above with access dates.
