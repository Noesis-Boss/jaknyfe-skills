# Don Lowery's Zo Workspace

Personal Zo Computer for **jaknyfe** (Don Lowery). Use this as a routing map for settled project guidance.

## Active projects

- **Syndicate** (`Projects/syndicate/`, dev at `http://localhost:57548`) — EXCLUSIVE active focus. Multi-tenant SaaS agent-orchestration platform. Boardroom view across companies + per-company boards (Board / Projects / Agents / Tasks / Skills / Memory / Events). SQLite-backed (`data/syndicate.sqlite`). See `Projects/syndicate/AGENTS.md` for schema, API, and the working features.
- **zo.space homepage** (`https://jaknyfe.zo.space/`) — single-page hub. Live stock/crypto tickers (SPCX, BTC, DOGE) at top, animated pegasus flying across the page, UFO visits with beam + laser every ~26s, randomly-pulsing "card ripple" shimmer on project cards, particle field, animated rings + sun behind the profile photo, 11 project cards + Web Showcase modal. Source lives in the `/` route on `jaknyfe.zo.space` (Next.js bundle). Quote data is proxied through `/api/quote` (caches Yahoo Finance for 60s).
- **Scottish Rite site** — Vite/React build deployed to `https://scottish-rite-jaknyfe.zocomputer.io/`. See `Projects/scottish-rite-site/AGENTS.md` for the build/push workflow.
