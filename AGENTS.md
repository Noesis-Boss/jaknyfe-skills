# Don Lowery's Zo Workspace

Personal Zo Computer for **jaknyfe** (Don Lowery). Use this as a routing map for settled project guidance.

## Project routing

## New project convention

- Every new project must be initialized as its own Git repository before substantive implementation begins. Keep repositories isolated; do not add a new project to an unrelated existing repository.

- **Syndicate** (`Projects/syndicate/`, dev at `http://localhost:57548`) — Existing multi-tenant SaaS agent-orchestration platform kept for reference and explicitly requested maintenance. It is not a default project focus. See `Projects/syndicate/AGENTS.md` for schema, API, and working features when this project is directly requested.
- **zo.space homepage** (`https://jaknyfe.zo.space/`) — single-page hub. Live stock/crypto tickers (SPCX, BTC, DOGE) at top, animated pegasus flying across the page, UFO visits with beam + laser every ~26s, randomly-pulsing "card ripple" shimmer on project cards, particle field, animated rings + sun behind the profile photo, 11 project cards + Web Showcase modal. Source lives in the `/` route on `jaknyfe.zo.space` (Next.js bundle). Quote data is proxied through `/api/quote` (caches Yahoo Finance for 60s).
- **Scottish Rite site** — Vite/React build deployed to `https://scottish-rite-jaknyfe.zocomputer.io/`. See `Projects/scottish-rite-site/AGENTS.md` for the build/push workflow.

## Robinhood Trading Bot

- **Path**: `robinhood-trading-bot/`
- **Purpose**: London breakout day-trading bot (from video https://youtu.be/8KblOEu56dM). yfinance data, paper-sim by default, real Robinhood via env secrets.
- **Backtest results** (2026-07-01 to 2026-08-06, 13-symbol universe, capital $10,000, theta realistic & seeded): 198 trades (99 theta spreads + 99 directional day-trades), 67.2% win rate, 1.71 profit factor, +$4,156.27 P&L. Theta contributes only +$134.02 across 99 spreads (77 wins @ +$9.29, 22 losses @ -$30 = avg +$1.35/spread); the rest (+$4,022) is equity day-trading (56.6% win rate, avg +$40.63/trade, best +$846 MARA long, worst -$416 MARA short). CLI default `--symbols` only has 5 core; pass the full 13 (SPY QQQ AAPL TSLA NVDA SOFI F AAL MARA RIVN NIO RBLX DKNG) for the full universe.
- **Theta realism fix (2026-08-08)**: theta spreads are NO LONGER booked as guaranteed full-credit wins. `_estimate_credit` now clamps premium to a realistic $5–$15/contract band and bounds spread width to a ~$20–$30 max loss; `simulate_expiry` resolves each spread by POP (80% win full credit / 20% take max loss) with `random.seed(42)`. Results: 17 win @ +$9.29 each, 7 lose @ -$30.00 each -> theta nets -$52.07 across 24 spreads (71% win rate). Prior +$4,643 / 6.26 PF / 79.2% figures were inflated by the old guaranteed-win model.
- **Win rate improvements**: volume filter, breakout-strength buffer (0.75), directional bias + trend filter, max holding bars (30), trailing stop to breakeven. +20.9% absolute win rate (58.3%→79.2%) when theta spreads included.
- **Key improvements** (vs naive box breakout): volume filter, breakout-strength buffer, directional bias + trend filter, max holding bars, trailing stop to breakeven.
- **Tuning knobs** (in `config.yaml`): `breakout_strength` (0.5–1.0), `max_holding_bars` (18–60), `rr_ratio` (1.5–3.0), `entry_window_hours`.
- **Theta farming support**: ThetaFarmer (src/theta_farming.py) sells weekly credit spreads after confirmed breakouts; Broker.place_spread() (src/broker.py); backtest.py integrates both strategies; project.py (Monte Carlo) + project_theta.py (deterministic) produce capital-aware projections saved to projections.json.
- **Capital projections** (projections.json, 20k sims, with theta farming): $100 → $1,918 median (+1,818%) at 1yr (theta disabled, below $200 threshold); $300 → $9,230 median (+2,977%) at 1yr (theta enabled at 1 contract, 7% risk/trade); $1,000 → $34,307 median (+3,331%) at 1yr (theta enabled, 5 contracts/trade). Theta threshold: ~$200 (capital-aware contract scaling: `int(risk_amount / $20 max_loss)`, no floor).

## Filesystem migration

- 2026-08-13: Moved seven isolated root artifacts to `Archive/root-artifacts/` after reference and tracking checks.
- 2026-08-13: Moved 17 clearly generated root screenshots/captures to `Media/screenshots/`; tracked root images and ambiguous source/reference media remain unmoved.
- Remaining work requires project-by-project reference maps for loose root documents, scripts, databases, duplicate project directories, and tracked/generated assets. Do not bulk-move them.

## Issue Log

- 2026-08-25: Idea Desk's “Ask assistant about this idea” button was wired to a dedicated `/api/idea-desk/ask` Zo AI route. The private dashboard now opens an accessible modal with idea-specific analysis, retry handling, and contextual follow-up questions; live generation, follow-up, Escape close, and the rendered response were browser-verified in `Media/screenshots/idea-desk-assistant-response.png`.
- 2026-08-20: Idea Desk boot loop traced to a malformed `/api/idea-desk` X adapter function. Replaced the parser with syntax-safe code; API returned HTTP 200 with 22 live ideas and the dashboard screenshot rendered successfully.

## Feature Log
- 2026-09-05: Unblocked the Skills repo master push to `Noesis-Boss/jaknyfe-skills`. The backlog of 174 unpushed commits contained >100MB blobs (moltbook_karma.log 2.5GB, paperclip-backups server.log 2.0GB + postgres dump 277MB, paperclip-restore logfile 542MB) that GitHub's pre-receive hook rejected. Stripped only those four paths from unpushed history with `git filter-repo --force --refs master --invert-paths ...` (partial mode: pushed history and working tree untouched, HEAD tree verified identical). A full push then failed mid-transfer (curl 55, pack too large) and linear chunk pushes were rejected non-fast-forward because master's history contains merged orphan lineages (site rebuilds with unrelated roots). Fix: force-pushed 25-commit topo-order chunks to a scratch `sync-staging` branch to stage objects server-side, then pushed master (d2e15f1c → faa3a99a) as a normal fast-forward and deleted the scratch branch. Master and origin are now in sync.

- 2026-08-21: Added the public Zo Space page `https://jaknyfe.zo.space/broheim` for The Original Broheim, a vintage-wanderer creative-alter-ego site with Dispatches, Artifacts, Listening Room, keyboard-operable cards, reduced-motion support, and a homepage Web Showcase link; public page screenshot and accessibility checks passed.
- 2026-08-21: Added the public Zo Space book showcase at `https://jaknyfe.zo.space/books`. It presents Outsource Your Own Brain, Bound by Ash and Thorn, and Project Orion: Alpha Protocol with 3D cover motion, controls, keyboard navigation, touch swipes, detail views, and reduced-motion handling; the rendered page was screenshot-verified.
- 2026-08-21: Replaced the temporary Bound by Ash and Thorn treatment on the public books showcase with the supplied final cover; live page screenshot verified.
- 2026-08-21: Enhanced `Skills/humanizer/SKILL.md` with a transparent 0-100 AI-pattern risk evaluator, word-count confidence rules, dimension weights, interpretation bands, and before/after reporting limits. The score is editorial guidance, not proof of AI authorship.
