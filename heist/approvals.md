# S4 Fact-Check Audit & Palermo Verdict — MCP Catalog & Trust Gateway Package
**Auditor stage:** S4 · **Date:** 2026-09-07 · **Scope:** heist/final/, heist/evidence/, heist/logs/finance.md · **Paper only — nothing published, sent, or purchased during this audit.**

---

## Verdict: **PASS** (after one documented revision pass — details below; zero unresolved VETO items)

---

## 1. Definition-of-Done audit (checkbox → actual file)

| DoD item | File verified | Result |
|---|---|---|
| Three opportunities documented in evidence/ with sources | `evidence/opportunities/opportunity-1.md`, `-2.md`, `-3.md` (all with source URLs + access dates) | ✅ PASS |
| Chosen opportunity justified in final/ | `final/choice.md` (Opportunity 2, named tradeoffs vs Opp 1 and 3) | ✅ PASS |
| Launch plan + 5 posts + outreach list in final/ | `final/launch-plan.md`, `final/posts/post-01…05.md`, `final/outreach-list.md` | ✅ PASS |
| Budget estimate in logs/finance.md | `logs/finance.md` — ASSUMPTIONS and CONFIRMED in separate tables; confirmed total $0 | ✅ PASS |
| Palermo verdict recorded in approvals.md | This file. **Note:** `mission.md` was not found as a file in heist/; the DoD was audited from the mission statement supplied to S4. `heist/approvals/` exists as an empty directory; the mission names `approvals.md`, so this file is the verdict of record. | ✅ PASS |

## 2. Claim-by-claim live verification (2026-09-07 unless noted)

| Claim | Source | Live check |
|---|---|---|
| 97M MCP SDK downloads/month, March 2026, up from ~2M Nov 2024, 4,750%/16 months | digitalapplied.com (2026-09-06) | ✅ verbatim match |
| ~5,000 → 177,436 MCP tools, 35x, Jan 2025–Feb 2026; downloads 80K→14M (UK AISI/BoE) | micheallanham.substack.com (2026-09-06) | ✅ table match |
| 33% of 1,000 servers critical (Enkrypt AI, Oct 2025) | practical-devsecops.com (2026-09-06) | ✅ verbatim |
| SSRF in 36.7% of 7,000+ servers (BlueRock, 2026) | practical-devsecops.com | ✅ verbatim |
| ~78% false-positive rate, YARA-based scanners (AppSec Santa, April 2026) | practical-devsecops.com | ✅ verbatim |
| CVE-2026-33032 "MCPwn", CVSS 9.8, actively exploited, patched 2026-03-15 | practical-devsecops.com | ✅ verbatim |
| Microsoft June 2026: tool descriptions = supply-chain assets | labs.cloudsecurityalliance.org | ✅ verbatim ("formally classifies…") |
| OWASP MCP Top 10 exists | cycode.com | ✅ verified; **ranking error found in post-02 — fixed, see §3** |
| Registry preview launched 2025-09-08; GitHub repo invites Discussions/Issues | blog.modelcontextprotocol.io | ✅ verbatim |
| Official registry read API public | registry-authorization.md | ✅ "remains public for reading" verbatim |
| PulseMCP Sub-Registry API implements Generic Registry API spec; partner contact unpublished-pricing; 21,950+ servers | pulsemcp.com/api, /servers | ✅ all three (live count 21,961) |
| mcp-audit: exists, Apache-2.0, OWASP MCP Top 10 mapping, invites issues | github.com/adudley78/mcp-audit | ✅ via GitHub API + README (devgenius article 403s to bots — see §4) |
| modelcontextprotocol/registry + invariantlabs repos exist | GitHub API | ✅ (mcp-scan → redirects to snyk/agent-scan — see §3, Fix 2) |
| GitHub Free covers public repo/issues/actions at $0 | github.com/pricing | ✅ ($0/Free confirmed) |
| Scaffold: 6/6 tests pass; bearer auth on POST /catalog/refresh + /tools/execute; CLI allowlist add/remove/list; MCP stdio tools | `Projects/mcp-catalog-gateway/` | ✅ `bun test` = 6 pass 0 fail (incl. allowlisted-execution test); `src/auth.ts` uses `CATALOG_API_TOKEN`; both POST routes return 401 without auth; CLI + `src/mcp.ts` present |
| MCP Market claims 20,980+ servers | mcpmarket.com (2026-09-06) | ⚠️ bot-blocked (HTTP 429) on recheck — S1 verification of 2026-09-06 stands; channel verification already deferred to send time by the file's own compliance note |

## 3. Failures found → one revision pass (executed 2026-09-07, itemized; nothing silent)

**Fix 1 — `final/posts/post-02.md` (failed criterion: claim-vs-source verification).**
- Was: "OWASP now maintains an MCP Top 10 with tool poisoning at the top."
- Source says: cycode's table lists Tool Poisoning as **MCP03** (third); CSA source calls it "the third entry."
- Now: "OWASP's MCP Top 10 ranks tool poisoning #3 (MCP03)" with correction note. ✅ re-verified against both captured sources.

**Fix 2 — `final/outreach-list.md` target #3 (failed criterion: contact channel must be proven by the cited source).**
- Was: claims README publishes `mcpscan@invariantlabs.ai` as the integration contact.
- Live README (accessed 2026-09-07) contains **no such email**; repo redirects to `snyk/agent-scan` (Invariant absorbed into Snyk; tool now "Agent Scan"); README directs registry integrations to `evo.ai.snyk.io/#contact-us` with "designated APIs."
- Now: entry rewritten — Snyk Evo contact form as channel, acquisition noted, email claim withdrawn, opener updated to "Agent Scan (formerly MCP-Scan)." ✅ re-verified against captured README.

**Fix 3 — currency: `$690` → `€690` in `evidence/category-scan.md`, `evidence/opportunities/opportunity-1.md`, `evidence/opportunities/opportunity-2.md`, `final/choice.md` (failed criterion: claim-vs-source; Optimum Web lists "MCP Security Gateway — €690").** ✅ all four fixed.

**Fix 4 (minor, same pass) — `final/posts/post-01.md`:** "35x in one year" → "35x in 13 months (Jan 2025–Feb 2026, per source table)" to match the source's table window.

**Fix 5 (minor, same pass) — `final/choice.md`:** stale internal path `final/outreach.md` → `final/outreach-list.md` (3 occurrences → the one reference corrected).

## 4. Audit notes (caveats, not failures)

- **devgenius.io mcp-audit article**: 403 to automated fetchers on 2026-09-07. Load-bearing claim (repo exists, Apache-2.0, OWASP mapping) verified directly via GitHub API + repo README instead. Article URL retained as secondary cite.
- **MCP Market (mcpmarket.com)**: 429 rate-limit on 2026-09-07 recheck; S1 verification (2026-09-06) stands. Outreach target #6 already requires channel verification at send time — no unresolved gap.
- **`heist/drafts/`** contains pre-revision working copies (S3 snapshots); `final/` is the package of record. Drafts deliberately left as-is to preserve the audit trail.
- **mission.md** not present in heist/; DoD audited from the mission statement supplied to this stage.

## 5. Constraint compliance

- **Paper only:** confirmed — no posts published, no outreach sent, nothing purchased during S1–S4. Every post and opener is marked DRAFT pending Don's approval.
- **Sources + dates:** every factual claim in final/ and evidence/ carries a source URL and access date (post-revision).
- **Budget separation:** `logs/finance.md` keeps CONFIRMED ($0, sourced) strictly separate from ASSUMPTIONS (unbudgeted pending dated pricing).

## 6. Handoff

Package is ready for Don's approval. Decision points awaiting Don: (1) approve/edity any of the 5 posts, (2) approve outreach send order starting with the mcp-audit GitHub issue, (3) approve repo publication (post-04 links the repo only "when Don approves publishing it"). No external action has been taken on any of them.
