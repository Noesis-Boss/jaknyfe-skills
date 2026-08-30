# ScholarSearch Frontend

Frontend interface for the ScholarSearch scholarship database platform.

### 2026-08-09 - Publication gate for unverified imports
- New scholarship records are unpublished until their application URL is independently verified.
- Public search, category counts, totals, and international counts require both `active = 1` and `url_status = 'verified'`.
- Existing audited inventory remains unchanged: 2,050 active verified records.

### 2026-08-09 - Validated research batches
- Processed the saved 1,048-record discovery queue in batches of 200 with `scripts/import-research-batch.ts`.
- Added 346 new records after live URL/content validation; rejected generic pages, media URLs, failures, and duplicates.
- Live inventory now contains 2,478 active verified records. No active record has a non-verified `url_status`.

### 2026-08-09 - Strict application-link audit
- Audited active application URLs against live HTTP destinations and stored results in `url_status`, `last_checked`, and `link_notes`.
- Only `url_status='verified'` records remain active; broken, suspicious, missing, and unverified links are inactive and hidden by the existing `active = 1` API filter.
- Database backups are stored under `data/link-audit-backups/`.
- Audit utility: `scripts/audit-application-links.ts`.
- Deep-researched replacements restored 9 records to active status: Regeneron STS, Schwarzman Scholars, Morehead-Cain, Robertson Scholars, Rhodes, and Gates Cambridge. Official destination evidence is recorded in each row's `link_notes`.

## Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Styling**: Tailwind CSS 4 with shadcn/ui components
- **Backend**: Bun + Hono server
- **Icons**: Tabler Icons

## Development

```bash
cd /home/workspace/scholarsearch-site
bun run dev
```

## Build

```bash
bun run build
```

## Issue Log
### 2026-08-30 - Bold.org application-link cleanup
- **Problem**: 422 active records used Bold.org aggregate or middleman destinations.
- **Fix**: Crawled each Bold.org source page, tested candidate external links, retained only matched official sponsor/admin application endpoints, and deactivated unresolved records.
- **Verification**: 339 records recovered; 83 deactivated; 0 active records retain Bold.org in application, form, or website fields. Backup: `data/processed/scholarships.db.backup-bold-20260830-153551`.

### 2026-08-30 - Scholarships360 application-link cleanup
- **Problem**: 156 active records used Scholarships360 listing/detail URLs as application destinations.
- **Fix**: Crawled each active source page and replaced only matched external sponsor/application endpoints; unresolved and category/article records were deactivated. Scholarships360, social, and scholarship-search destinations were not accepted.
- **Verification**: 0 active `scholarships360.org` application URLs remain; 16 recovered records remain active with external endpoints; 140 records were deactivated. Database backup: `data/processed/scholarships.db.backup-s360-20260830-150109`.
- **Note**: `bun run build` remains blocked independently because the repository has no `index.html`; no frontend deployment was performed.

### 2026-08-25 - Release gate accepted unverified active rows
- **Problem**: The operational report measured verified coverage but allowed the release gate to pass when the daily audit target was met and no rows were overdue, even if active rows still had non-verified URL states.
- **Fix**: The gate now requires every active row to be verified (`active_verified_records === active_records`), with a regression fixture covering the failure.
- **Verification**: TypeScript tests and production build passed; strict production report now correctly fails while 393 active rows remain non-verified.

### 2026-08-24 - Undergraduate statistics count
- **Problem**: The homepage showed only 2 undergraduate scholarships because the stats card counted `category = 'Undergraduate'`; most records classify level in `education_level`.
- **Fix**: Added verified `education_level` aggregates to `/api/stats` and updated homepage stat cards and drill-down filters to use the correct field.
- **Verification**: Database and live API report 737 undergraduate records; production build passed; live screenshot shows Undergraduate 737.

### 2026-08-24 - Scholarships.com URL cleanup
- **Problem**: 501 active verified records pointed to the `scholarships.com` aggregator, including directory pages and aggregator detail pages rather than official sponsor submission sites.
- **Fix**: Deactivated all active records whose application, website, or form URL used the actual `scholarships.com` domain. The separate `accessscholarships.com` domain was not changed.
- **Verification**: Database audit reports 501 deactivated and 0 remaining active verified records using `scholarships.com`; the Cancer Pathways record remains active with its official Cancer Pathways URL. Backup: `data/processed/scholarships.db.backup-20260824-scholarships-com`.

### 2026-08-24 - Cancer Pathways Teen Writing Contest destination
- **Problem**: The active Cancer Pathways Teen Writing Contest record linked to the Scholarships.com iOS app installer instead of the contest site.
- **Fix**: Updated the live record in `data/processed/scholarships.db` to the verified official contest page `https://cancerpathways.org/programs/teen-writing-contest/` and its submission-information page.
- **Verification**: Official page returned HTTP 200; live ScholarSearch API now returns the Cancer Pathways URL; the live search result was screenshot-verified. Backup: `data/processed/scholarships.db.backup-20260824-cancer-pathways`.

### 2026-08-12 - Admin dashboard demo metrics removed
- **Problem**: Overview still displayed hardcoded user-growth values, percentage badges, and an active-profile count derived by subtracting three from the user count.
- **Fix**: User growth now groups live account creation dates; KPI counts use live users, completed profiles, and verified scholarships. Outreach remains `0` with an explicit `Not connected` state because no provider exists.
- **Verification**: `bun run build` passed and service `svc__BI1M5KYZBE` restarted with the production build. Authenticated screenshot verification remains blocked because the current browser session is not signed in as the administrator.

### 2026-08-12 - Admin dashboard live navigation
- **Feature**: Connected the Users, Profiles, Scholarships, Outreach, and Settings sidebar links to actual dashboard views.
- **Live data**: Users and scholarships use existing admin APIs; Profiles now uses a protected `/api/admin/profiles` endpoint joining users with profile records. Settings reflects the current administrator session.
- **Outreach**: Remains an explicit provider-connection state because no outreach data source is configured.
- **Verification**: Build passed, service restarted, live browser opened each management view, and `agent-browser a11y` reported zero violations.

### 2026-08-12 - Individual scholarship source ingestion
- **Requirement**: Scholarship search sites such as Bold.org must contribute individual scholarship records, not category/listing pages.
- **Pipeline fix**: `scripts/import-research-batch.ts` now rejects known listing/category/search/blog URL paths before validation. The sitemap discovery workflow already restricts Bold.org to `/scholarships/<slug>` pages and extracts individual page data.
- **Data cleanup**: Deactivated 154 active listing pages in the site database and 260 in the primary database. Backups are stored under `data/link-audit-backups/`.
- **Verification**: Both databases report zero active listing-path records. A live Bold.org sample fetched 20 individual pages; all parsed candidates were already duplicates. Live ScholarSearch now reports 2,538 active verified scholarships.

### 2026-08-12 - Finder counter mismatch for Graduate category
- **Problem**: Selecting the `Graduate` category displayed 2 scholarship cards while the result counter reported 3.
- **Root cause**: The results query required `active = 1 AND url_status = 'verified'`, but both result-count queries counted all active rows and included an unverified record.
- **Fix**: Added the same verified-link predicate to both `/api/scholarships` count paths.
- **Verification**: Live API now returns `total: 2` and 2 results for `category=Graduate`; live browser selection shows `2 found` and both Cambridge scholarships.

### 2026-08-12 - Profile form text contrast
- **Problem**: Profile select values, field text, and textarea placeholder text rendered too light against the white form controls.
- **Fix**: Added explicit dark text and readable placeholder classes to the editable profile controls.
- **Verification**: Rebuilt and restarted the public ScholarSearch service. Live profile page screenshot verified the corrected form rendering.

### 2026-08-12 - Administrator account level and dashboard access
- **Feature**: Added `Administrator` account-level display to the account page and an `Admin dashboard` link visible only when the authenticated role is `admin`.
- **Security**: Public registration can no longer self-select the admin role; server-side admin endpoints continue to require an authenticated admin role.
- **Account**: Promoted `delowery@gmail.com` to `admin` in `data/users.db`.
- **Deploy**: Restarted service `svc__BI1M5KYZBE` and verified the live authenticated dashboard at `https://scholarsearch-jaknyfe.zocomputer.io/admin` with browser screenshot and accessibility inspection.

### 2026-08-12 - Premium management dashboard
- **Feature**: Replaced the legacy admin screen with a responsive `/admin` operations dashboard for users, profiles, scholarships, and outreach planning.
- **UI**: Added collapsible desktop sidebar, mobile drawer, navy/gold dark mode, KPI cards, animated user-growth chart, scholarship category mix, recent-user table, outreach empty state, loading skeletons, and reduced-motion-compatible chart behavior.
- **Data**: Reuses `/api/admin/users` and `/api/admin/scholarships`; outreach remains an intentional setup state because no outreach API exists yet.
- **Verification**: `bun run build` passed. Authenticated local browser render verified the dashboard shell, chart, tables, and outreach state. `agent-browser a11y` reports zero violations.

### 2026-08-08 - Blank page / no login / "5,000+" only — root cause found
- **Problem**: User reported (a) page only showed "5,000+ Scholarships" with no scholarship previews, (b) no visible login.
- **Root cause 1 (blank crash)**: `getStatGroups()` in `src/pages/Home.tsx` called `L.category.toLowerCase()` on every stats row. `/api/stats` returned one `{"category":null,"count":381}` row (381 scholarships with NULL category in DB). Null `.toLowerCase()` threw during render → React unmounted the ENTIRE app → blank page. This is why login disappeared too — the whole tree crashed, not just the results.
- **Fix 1**: server.ts `getCategories()` now groups NULL categories as 'Uncategorized' (COALESCE) — API never emits nulls. **Worked**.
- **Root cause 2 (no previews)**: `Home.tsx` fetched `/api.php/api/scholarships` and `/api.php/api/stats` (PHP-era paths), but the Bun server only has `/api/*`. SPA fallback returned index.html → `res.json()` threw → no results, stats stuck at fallback "5,000+".
- **Fix 2**: changed fetches to `/api/scholarships` and `/api/stats`. **Worked**.
- **Also hardened**: localStorage access in AuthProvider, Profile, Admin, theme-provider wrapped in try/catch with in-memory fallback (sandboxed/private browsers that block storage would otherwise crash the app the same way).
- **Verified live** (https://scholarsearch-jaknyfe.zocomputer.io, Zo browser + agent-browser): nav shows Sign in / Sign up (logged out); stats sidebar shows real 10,747 total; 12 scholarship cards render with amounts/Apply buttons; login → register → profile page saves (interests persisted to DB).
- **Deploy**: `bun run build` (fresh hashes, no CF cache) + `update_user_service` restart (entrypoint `bun run prod` rebuilds anyway).
- **Status**: COMPLETE — verified rendered live + login flow tested end-to-end.


### 2026-06-29 - Add Masonic scholarships
- **Action**: Tagged

### 2026-06-29 - Text intensity and styling updates
- **Problem**: Bold/black text was overpowering the page intensity
- **Fix**: Reduced text intensity by changing text-black to text-gray-800, text-gray-700, etc.
- **Changed Search button**: bg-yellow-400 to match left border color (border-yellow-400)
- **Added dropshadow**: Single pixel black dropshadow on "Total Scholarships" numerical value
- **Month abbreviation**: Added helper function to abbreviate month names to 3-letter format in deadline dates
- **Status**: Deployed to noesisgroup.com/scholarsearch/

### 2026-07-18 Audit (full site, `impeccable audit`): Verified `service_doctor` shows service RUNNING (port 57137); build clean; 502 root cause = `Failed to resolve /scholarsearch/assets/index-B5AmAu-1.js` (base path mismatch). Fix applied: rebuilt (`base: "/"`), copied artifacts (`cp -r dist/*` to serve dir), restarted service (`update_user_service`). Site then returned 503 (restart in progress); final screenshot verification NOT completed — service still settling. Not marking complete until 503 clears and screenshot verifies rendered page.

### 2026-08-07 - Login/profile system live + cache-busting fix
- **Build**: Sign up / Sign in / Sign out (JWT in localStorage), profile page (GET/PUT `/api/profiles/me`), auth endpoints (`/api/auth/register|login|me|logout`). All in `src/pages/auth/`, `src/components/auth/AuthProvider.tsx`, `src/pages/Profile.tsx`.
- **Problem**: User could not see login on live site. Root cause: a stale `dist/` (built 07:24 UTC) contained an old bundle with no auth routes — `vite build` was only transforming 4 modules (build cache). Cleared cache (`rm -rf node_modules/.vite`), full rebuild transformed 6136 modules → auth routes included.
- **Second issue**: Cloudflare had cached old JS/CSS URLs (`/assets/index-*.js`) as `text/html` (SPA fallback) for 4h, so browsers got HTML-as-JS and React never mounted → blank page. Fix: rebuilt twice with real source changes (added `autocomplete` attrs to login/signup forms, `scroll-behavior: smooth` to `src/styles.css`) producing fresh asset hashes with no CF cache. Assets now serve `text/javascript`/`text/css`.
- **Bug found during verification**: `Profile.tsx` called `PATCH /api/profiles/{id}` (404 → SPA fallback → hang). Fixed to `GET`/`PUT /api/profiles/me`.
- **Verified live** (Zo browser, https://scholarsearch-jaknyfe.zocomputer.io): home nav shows Sign in/Sign up when logged out, user name + Sign out when logged in; profile page loads name/email/education/state/field/interests and saves; scholarship badge 5,000+ intact.
- **Note**: `bun run prod` rebuilds on every service restart — the service restart re-runs `vite build`, so any deploy is a fresh build from source.
### 2026-08-07 - Login/profile system live + cache-busting fix
- **Problem 1**: Vite build silently served a stale bundle — `bun run build` transformed only "4 modules" and kept emitting the OLD asset hash (no auth routes in bundle). Cause: stale `node_modules/.vite` transform cache. Fix: `rm -rf node_modules/.vite` (the `clear-cache` script) before `vite build`. Full build = 6136 modules → new hash with auth routes. **Worked**.
- **Problem 2**: Live site blank / "no login" even after deploy. Root cause: SPA fallback (`app.get("*")`) served index.html (200, `content-type: text/html`) for missing asset paths, and Cloudflare cached those HTML-as-JS responses for 4h (`max-age=14400`) under the real asset URLs. So browsers loaded HTML where JS was expected → nothing rendered. Fix: (a) fixed the dev-mode asset route that 404'd (the `preview`/`dev` route had `c.req.path.replace("/scholarsearch/assets/", "")` pattern that didn't match `/assets/...`; production route serves `/assets/*` correctly), (b) deployed a new build → fresh asset hashes → no CF cache entries, (c) verified `Content-Type: text/javascript` / `text/css` on live asset URLs. **Worked** — nav now shows Sign in / Sign up, login redirects to /profile.
- **Problem 3**: Profile page stuck on "Saving..." + empty Name/Email. Root cause: frontend called `PATCH /api/profiles/:id` and `GET /api/profiles/:id`, but server only implements `GET /api/profiles/me` + `PUT /api/profiles/me`; `PATCH /api/profiles/:id` fell through to SPA fallback (HTML 200) → `res.json()` threw → spinner never reset. Fix: Profile.tsx now uses `GET /api/profiles/me` and `PUT /api/profiles/me`; Name/Email read from auth `user` context (server profile row has no name/email columns). **Worked** — verified live: login as browsertest2@example.com → profile prefills, Education/State/Field/Interests save + persist.
- **Deploy notes**: service `svc__BI1M5KYZBE` (scholarsearch, port 57137, https://scholarsearch-jaknyfe.zocomputer.io) entrypoint is `bun run prod` = `build && serve` — it rebuilds on every restart, so any manual dist edits are wiped. After every deploy: `curl -sI <asset-url>` and confirm `content-type: text/javascript` before declaring done.
- **Status**: COMPLETE — verified rendered live (Zo browser session): nav Sign in/Sign up (logged-out), user name + Sign out (logged-in), /profile loads, saves, persists.

### 2026-08-07 - Aggregate amounts pared to individual annual values
- **Problem**: Large-amount scholarships showed multi-year aggregates (e.g. $241,800 Montevallo, $100K ROTC, $250K Breakthrough) while most entries show annual individual awards — misleading comparisons.
- **Fix**: Two-pass cleanup on BOTH `scholarsearch/data/processed/scholarships.db` and `scholarsearch-site/data/processed/scholarships.db`:
  1. `apply_annual_fixes.py`: 74 curated rows updated to annual/individual values (verified via web search) — ROTC → "full tuition + fees + stipend (renewable annually)", Breakthrough → $62,500/yr, Montevallo → $60,450/yr, Soros → $45,000/yr, Echoing Green → $40,000/yr, Thiel → $50,000/yr, Truman → $15,000/yr, GE-Reagan/Amazon FE → $10,000/yr, Cal Grant A/B → $12,570/yr, Crain → $5,000, AIST → $3,000, ACIA → $8,000, Anthony Muñoz → $20,000, etc.
  2. `cleanup_aggregates.py`: DELETED junk rows that were aggregator/listicle pages, not scholarships — Bold.org category pages ("1,000s of Scholarships by…", "60 Florida Scholarships…", "210+ Merit…"), FAQ/content pages ("Frequently Asked Questions", "Eagle Scholarship Portal", "Creative writing scholarships"), scraped junk names ("…This scholarship has been verified by…"), fabricated entries ("Princeton University No Essay Scholarship" — Princeton offers no such thing), duplicate Regeneron "Scholarship - $250,000" rows, and listicle dupes.
- **Result**: Main DB 11,265 → 10,983; site DB 11,503 → 11,183. All $100K+ remaining rows are legit individual awards (Regeneron top prize, Schwarzman full-funding, Wellcome multi-year grant) with displays explicit about award type.
- **Status**: COMPLETE — verified via SQL audits on both DBs; no amount > $50K remains that is a misleading aggregate.

### 2026-08-08 - Blank page / no login / no scholarship previews on live site (FIXED)
- **Problem reported**: Site showed only the "5,000+" badge, no scholarship previews, no login nav.
- **Root cause 1 (crash)**: `/api/stats` returned a row with `category: null` (381 rows with NULL category in DB). `Home.tsx getStatGroups()` called `category.toLowerCase()` on null → threw during render → React unmounted the ENTIRE app (blank page). Sandbox browsers reproduced; real users saw either blank or partial paint.
- **Fix 1**: `server.ts getCategories()` → `SELECT COALESCE(category, 'Uncategorized') ...`. API now emits zero null categories (verified: `nulls: 0`, total 10,747).
- **Root cause 2 (PHP-era paths)**: `Home.tsx` fetched `/api.php/api/scholarships` and `/api.php/api/stats` — routes that don't exist on the Bun server (only `/api/*`), so stats never loaded (stuck at fallback "5,000+") and results stayed empty. `Admin.tsx` also used `/scholarsearch/api.php/api/*`.
- **Fix 2**: Home.tsx now uses `/api/scholarships` and `/api/stats`; Admin.tsx uses `/api/admin/*`. Grep `api.php` in src = 0 hits.
- **Hardening**: wrapped all `localStorage` access (AuthProvider, Profile, Admin, theme-provider) in try/catch `safeGet/safeSet/safeRemove` helpers so browsers with blocked storage (incognito/strict privacy) can't crash the app.
- **Verified live** (https://scholarsearch-jaknyfe.zocomputer.io, Zo browser screenshot): nav shows Sign in / Sign up when logged out; stats sidebar shows Total 10,747 / Undergraduate 3,576 / etc.; 12 scholarship cards render (Regeneron, Schwarzman, Stamps...) with amounts, locations, Apply buttons; pagination works. Login flow tested end-to-end locally: /login renders, register + login + profile GET/PUT /api/profiles/me save and persist (verified via API `updated_at`).
- **Deploy**: build is rebuilt on every service restart (`bun run prod` = `build && serve`); asset hashes fresh, serve `text/javascript` (cf-cache-status MISS).
- **Status**: COMPLETE — screenshot-verified live.

### 2026-08-08 - Blank page / no login / no scholarship previews — ROOT CAUSE FOUND
- **Symptoms**: Site showed only "5,000+ Scholarships" badge, no preview cards, and no Sign in/Sign up in nav.
- **Cause 1**: `src/pages/Home.tsx` fetched `/api.php/api/scholarships` and `/api.php/api/stats` — legacy PHP paths that don't exist on the Bun server (routes are `/api/*`). Fetches fell through to the SPA fallback (index.html), `res.json()` threw, stats/results never loaded → badge stuck at fallback "5,000+", zero cards.
- **Cause 2 (the blank page)**: `getCategories()` in `server.ts` returned a row with `category = NULL` (381 scholarships with no category). `getStatGroups()` in Home.tsx called `category.toLowerCase()` on it → React render threw → **entire app unmounted** → blank white page, no nav, no login. This is why the login was invisible despite being in the bundle.
- **Fixes**:
  1. Home.tsx: `/api.php/api/*` → `/api/*` (both fetchResults and fetchStats).
  2. server.ts `getCategories()`: `COALESCE(category, 'Uncategorized')` + `WHERE category IS NOT NULL` → nulls eliminated from API.
  3. Home.tsx `getStatGroups()`: `(L.category || "uncategorized")` guard so a null never crashes render.
- **Verified** (agent-browser + Zo browser, live https://scholarsearch-jaknyfe.zocomputer.io): nav shows Sign in / Sign up; stats sidebar 10,747 total / 3,576 Undergraduate; 12 scholarship preview cards (Regeneron, Schwarzman, Stamps, Wharton, Harvard…) with amounts, locations, Apply buttons; login form renders; test registration → profile page loads, education/state/field/interests SAVE and persist (verified via `PUT /api/profiles/me` row update).
- **Status**: COMPLETE. If user reports blank page again: check `/api/stats` for null categories and confirm asset `content-type: text/javascript` (CF cache).

### 2026-08-08 - Blank homepage / "5,000+ only, no previews" / login not visible — FIXED
- **Problem**: User reported site stuck at "5,000+ Scholarships" with no working scholarship previews, and no visible login.
- **Root cause 1 (previews dead)**: `Home.tsx` fetched `/api.php/api/scholarships` + `/api.php/api/stats`, but the Bun server exposes `/api/*` (no `api.php`). Both fetches returned SPA-fallback HTML → `res.json()` threw → stats stayed null ("5,000+" fallback badge) and results stayed empty. Admin.tsx had the same stale `/scholarsearch/api.php/...` paths.
- **Root cause 2 (whole app blank in some browsers)**: `/api/stats` returned a row with `category = NULL` (DB has 1 uncategorized row); `getStatGroups()` called `L.category.toLowerCase()` → TypeError during render → React unmounted the entire tree → blank page, no nav, no login. (Sandbox browsers crashed; user's browser likely showed the pre-crash paint = "5,000+" badge only.)
- **Fix**:
  1. `Home.tsx` → `/api/scholarships` + `/api/stats` (Admin.tsx → `/api/admin/...`).
  2. `getStatGroups()`: `(L.category || "Uncategorized").toLowerCase()` guard.
  3. `server.ts` `getCategories()`: `COALESCE(category, 'Uncategorized')` — API no longer emits nulls (verified: 0 nulls).
  4. `AuthProvider.tsx` / `Profile.tsx` / `theme-provider.tsx`: localStorage wrapped in a safe try/catch in-memory fallback (sandbox browsers block storage).
- **Verified live** (2026-08-08, Zo browser + agent-browser): nav shows **Sign in / Sign up** (logged out); stats sidebar renders Total 10,747 / Undergraduate 3,576 / etc.; 12 scholarship cards (Regeneron, Schwarzman, Stamps…) with amounts + Apply buttons; `/login` form works; register → `/profile` saves Education/State/Field/Interests via `PUT /api/profiles/me` (persisted, verified in DB).
- **Deploy note**: rebuild (`bun run build`), restart `svc__BI1M5KYZBE` (`bun run prod` rebuilds anyway). Fresh asset hash `index-Dvmgme7V.js` — `cf-cache-status: MISS`, serves `text/javascript`.
- **Status**: COMPLETE.

### 2026-08-12 - University scholarship directories are crawl sources
- **Problem**: University financial-aid pages such as WWU's Special Interest Scholarships page were being treated as scholarship records/providers even though they only list links to individual scholarships.
- **Fix**: Added `Skills/scholarship-discovery/scripts/crawl_directory_sources.py`. It fetches a directory, follows scholarship-related links, scrapes each detail page, inserts only individual records, and rejects navigation/index pages. WWU produced 18 links; 6 navigation pages were marked rejected and 12 individual scholarship records remain active. Existing WWU directory records are not active search results.
- **Status**: COMPLETE — crawler rerun is idempotent; second run inserted 0 duplicates.

## Feature Log
### 2026-08-24 - Scholarships.com discovery-only source policy
- **Requirement**: Use Scholarships.com to discover references, but never publish its aggregator URLs as scholarship application links.
- **Implementation**: `scripts/import-research-batch.ts` now treats Scholarships.com as discovery-only, extracts qualifying external references, validates the referenced destination, and records the external URL plus provenance. `scripts/audit-application-links.ts` rejects any Scholarships.com URL that reaches the audit stage.
- **Verification**: Both scripts bundle successfully; a live Scholarships.com test page resolved to an external reference and was recognized as a duplicate without inserting a Scholarships.com URL. Existing active aggregator records were already deactivated under the prior cleanup.

### 2026-08-25 - Discovery verification implementation resumed
- Added bounded official-link recovery in `Skills/scholarship-discovery/scripts/link_recovery.py`: three crawl levels, ten-page cap, two restricted searches, and a 60-second budget, with attempt and evidence retention.
- Added `Skills/scholarship-discovery/scripts/discovery_pipeline.py` for normalization, deduplication, verification gating, recovery handoff, and per-source reporting.
- Updated `scripts/audit-application-links.ts` and `scripts/run-link-audit-loop.sh` to select due records, process 500 per run, prioritize unstable/old records, and schedule the next check within 15 days.
- Verification: 7 Python tests pass; audit script bundles successfully. Commits: `8b022160`, `96b072d5`.

### 2026-08-25 - Discovery fixture and release validation
- Added a second verification pass after recovered-link discovery so recovered URLs count only when independently accepted as A/B official application destinations.
- Added fixture tests for report metrics and recovered-link publication gating.
- Full Vite build passed; TypeScript tests passed (2); Python verification/recovery tests passed (7); pipeline fixture passed.
- Production dry-run remained read-only. Current baseline is 2,666 active records, 2,049 active verified records, 617 active records with non-verified status, and 3 checks today; the 500/day release gate is correctly not met.

### 2026-08-25 - Release gate blockage cleared
- **Problem**: The audit queue prioritized old verified records, leaving 393 active legacy-status rows (`active`, `200`, or `unchecked`) outside the release-gate coverage set.
- **Fix**: Prioritized every active non-verified row before verified rows and included records with missing application URLs in the bounded audit queue. The audit deactivated failed, suspicious, and missing-link records; it did not promote failures to verified.
- **Verification**: 500-record audit completed; final report shows 2,443 active / 2,443 verified, 1,503 checks today, 0 overdue, and `release_gate_passed: true`. Vite build passed, TypeScript tests passed (3), and Python tests passed (7).
