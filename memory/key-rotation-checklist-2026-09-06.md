---
name: key-rotation-checklist-2026-09-06
description: Rotation checklist for API keys leaked to GitHub in the jaknyfe-skills repo (incident closed 2026-09-06). Lists key types and leak locations only — never actual values.
type: security
---

# Key Rotation Checklist — GitHub Leak 2026-09-06

Leak source: `Noesis-Boss/jaknyfe-skills` history — `freellmapi/.env`, `freellmapi/server/.env`, and a 2026-08-27 recovery snapshot of the whole workspace (`recovered-2026-08-27/...`), including a substrate-bot stash snapshot. All pushed to GitHub. Providers disabled the affected keys; replacement keys go in **Settings → Advanced → Secrets** or gitignored `.env` files only.

## Rotate now (provider keys, live exposure)

| # | Key type | Leaked in | Action |
|---|----------|-----------|--------|
| 1 | Anthropic `sk-ant-*` | freellmapi/.env, freellmapi/server/.env | Replace with new key; update freellmapi config |
| 2 | OpenAI `sk-proj-*` | freellmapi/server/.env | Replace; re-point freellmapi |
| 3 | OpenRouter `sk-or-v1-*` | freellmapi/.env | Replace; re-point freellmapi |
| 4 | GitHub fine-grained PAT | freellmapi/server/.env | Revoke; issue new PAT with minimal scopes |
| 5 | GCP API key(s) | freellmapi/.env | Restrict/regenerate in GCP Console |
| 6 | 69 agent API keys | paperclip-snapshot/agent_api_keys.json (both snapshots) | Rotate any still in use; rest are dead — leave |
| 7 | X/Twitter creds | Skills/x-twitter-by-altf1be/.env | Rotate if the altf1be bot still posts |
| 8 | Cloudflare tunnel token | cf-tunnel-helper.html | Delete old tunnel, create new token |
| 9 | Polymarket key | poly-bot/polymarket-copy-bot/.env | Rotate if poly-bot is active |
| 10 | Firecrawl key | firecrawl/README.md curl examples | Rotate at firecrawl.dev |
| 11 | Misc provider keys in gmail .eml/.html captures (7 files) | recovered snapshot | Check the emails; rotate any live keys |
| 12 | Cron script keys (heartbeat, maximize_points, void_daily) | shell scripts in snapshot | Rotate if those scripts still run |

## Lower priority (likely dead or test-only)

- ArcReel test fixtures (`test_*_api_key.py` etc.) — test values, replace with fakes
- bound-by-ash-technical-debt `.env.example` / local-live `.env` — legacy, likely dead keys
- `.env.bazaarlink`, opencode config.json — verify and rotate if live
- JWT in gmail capture — expired, verify

## Already done (no action needed)

- [x] Leak located: jaknyfe-skills history (freellmapi envs + recovered snapshot), commit lineage caa8e637/93d1753f
- [x] Other repos scanned (all 60): no active leaks on pushed refs
- [x] `*.env` gitignored workspace-wide; freellmapi envs removed from tree
- [x] Pushed refs force-pushed clean; remaining dead-key findings documented in `.gitleaksignore` (rotation pending)
- [x] Local stash (140 secrets) extracted to `Archive/stash-recovery-2026-09-06/` and cleared
- [x] Pre-push gitleaks hook installed globally (/root/.git-hooks/pre-push)
- [x] Zo rule created: never push any file containing a key/token/credential to GitHub
- [ ] Optional: full history purge with git filter-repo + force push to scrub dead keys from remote history

## Key identifiers (masked, for matching against provider dashboards)

Masked as `prefix…last4` — never store full values here. freellmapi copies were purged locally; fragments captured from the incident scan and the duplicate copies below.

| Key | Fragment | Where it lives now |
|-----|----------|--------------------|
| Anthropic | `sk-ant-api03…HgAA` | `bound-by-ash-technical-debt/local-live/.env` + recovered-2026-08-27 duplicate (same value as leaked freellmapi/.env) |
| OpenAI | `sk-proj-jluc…ZuAA` | same two files (same value as leaked freellmapi/server/.env) |
| OpenRouter | `sk-or-v1-a85…717f` | same two files (same value as leaked freellmapi/.env) |
| GCP AI API key | `AIzaSyBtos…OpA` | freellmapi/.env only (local copy purged) |
| Bazaarlink | `sk-bl-n7begeMg…BuclNeU6` | `.env.bazaarlink` (in .gitleaksignore) |
| Resend | `re_Txku8LZg_…hRE8` | `Projects/MindCraft/.env`, `weightloss-tracker/.env` |
| Google OAuth client secret | `GOCSPX-R3koX…hEVN` | `weightloss-tracker/.env` |
| Polymarket | poly-bot files excluded from archive | rotate in Polymarket dashboard if active |
| Cloudflare tunnel token | cf-tunnel-helper.html | delete old tunnel, create new token |
