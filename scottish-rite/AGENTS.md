# Scottish Rite Website — Agent Instructions

## Two Hosting Targets

The Scottish Rite site is deployed to TWO separate hosts with different codebases:

### 1. Zo Computer — `https://scottish-rite-jaknyfe.zocomputer.io/`
- **Stack**: Vite 4 + React 19 + JSX components
- **Source**: `/home/workspace/scottish-rite/` (Vite project)
- **Components**: `components/*.jsx` (sr-hero, sr-nav, sr-sections, sr-people, sr-contact)
- **Entry**: `src/main.tsx` → `src/App.tsx`
- **Build**: `bun run build` → `dist/`
- **Deploy target**: `/home/workspace/scottish-rite-site/` (git-pushed, zo computer pulls)

### 2. NoesisGroup — `https://noesisgroup.com/scottish_rite/`
- **Stack**: Single HTML file + React 18 + Babel standalone (NO Vite build)
- **Source of truth**: The `index.html` file itself (all components inline in `<script type="text/babel">`)
- **Server**: Apache/Plesk at `65.38.97.58`, user `noesisuser`
- **Deploy path**: `/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html`
- **Deploy method**: SCP the edited HTML file directly
- **SSH**: `sshpass -p '@EUjgrN9fkr5li8$' ssh noesisuser@65.38.97.58`

## Deployment Rule (ALWAYS — Both Targets)

When making edits, updates, or changes to the Scottish Rite website:

### Zo Computer (Vite build):
1. `cd /home/workspace/scottish-rite && bun run build`
2. `cp dist/index.html dist/assets/* /home/workspace/scottish-rite-site/`
3. `cd /home/workspace/scottish-rite-site && git add . && git commit -m "Update [description]" && git push origin master`

### NoesisGroup (single HTML):
1. Fetch current HTML: `sshpass -p '@EUjgrN9fkr5li8$' scp noesisuser@65.38.97.58:/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html /tmp/noesisgroup-scottish-rite.html`
2. Edit the HTML file locally (update officers, layout, etc.)
3. Upload: `sshpass -p '@EUjgrN9fkr5li8$' scp /tmp/noesisgroup-scottish-rite.html noesisuser@65.38.97.58:/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html`
4. Verify: `curl -sL https://noesisgroup.com/scottish_rite/ | grep 'Officer Name'`

**NEVER serve directly from Vite dist/ output for noesisgroup.com — it's a completely different codebase.**

## CRITICAL — Zip Extraction
When extracting a zip INTO the Scottish Rite project:
- The zip extracts to `/home/workspace/scottish-rite/`, NOT `scottish-rite-site/`
- The zip contains `.jsx` component files that OVERWRITE the proper `.tsx` files in `src/components/`
- These `.jsx` files use `const SRNav` (no export) instead of `export const SRNav` — they WILL break the build
- AFTER extracting, ALWAYS run: `rm src/components/*.jsx` before building
- Then build, copy to scottish-rite-site/, commit and push as normal

## User Preferences
- Don wants instructions written to memory so they persist when context runs out.
- Use project AGENTS.md files to store agent-level instructions.
- Don corrects UI/layout issues precisely and expects fast convergence.

## Issue Log

### 2026-08-13 — Restore dynamic event cards and full-size calendar modal
- Problem: the CalendarWiz feed was not producing visible event cards, and the modal did not encompass the full calendar.
- Solution: intercepted CalendarWiz's live `document.write` feed, extracted the current event names and dates into responsive cards, and changed the modal to `96vw` by `94vh` with a full-size iframe.
- Verification: deployed commit `03f7133`; live screenshots confirm six current event cards and the expanded calendar modal: `Media/screenshots/tsr-events-cards-fixed.png` and `Media/screenshots/tsr-calendar-modal-full.png`.

### 2026-08-13 — Raise hero white graphic again
- Problem: the white hero graphic still sat too low on the cameo.
- Solution: changed its vertical offset from `top: '-5rem'` to `top: '-8rem'` in `components/sr-hero.jsx`.
- Verification: rebuilt and pushed commit `ba09141`, synced `/tsr/`, and verified the live page by browser screenshot: `Media/screenshots/tsr-hero-graphic-higher.png`.

### 2026-08-13 — Restore event cards and modal-only calendar
- Problem: the full CalendarWiz iframe was displayed inline on the Events section, replacing the dynamic event cards; the first restored modal loader rendered blank.
- Solution: restored CalendarWiz `ucfeeder.php` for dynamic event cards, removed the inline calendar, and used the verified direct CalendarWiz iframe only inside the modal opened by `View Full Calendar`.
- Verification: deployed commits `7d7c83d` and `7330579`; browser shows dynamic event cards, and clicking `View Full Calendar` opens a populated modal iframe. Screenshot: `Media/screenshots/tsr-calendar-modal-fixed.png`.

### 2026-08-13 — Align hero graphic and tagline with cameo
- Problem: the white graphic and `Building Better Men Since 1882` tagline were not aligned to the top and bottom of the cameo image.
- Solution: moved the white graphic upward and shifted the tagline downward to the cameo’s lower section; buttons follow below.
- Verification: deployed commit `7711741`; browser screenshot confirms the requested alignment. Screenshot: `Media/screenshots/tsr-hero-cameo-aligned.png`.

### 2026-08-13 — Remove hero separator line
- Problem: an unwanted gold separator line remained beneath the hero graphic.
- Solution: removed the separator element from the hero component.
- Verification: deployed commit `b73c4aa`; browser screenshot confirms the line is gone. Screenshot: `Media/screenshots/tsr-no-separator.png`.

### 2026-08-13 — Remove hero lettering and raise hero graphic
- Problem: the hero contained unwanted red `Tucson Scottish Rite` lettering, and the white graphic sat too low over the cameo.
- Solution: removed the red lettering and moved the white hero graphic upward by 3rem.
- Verification: deployed commit `958e01c`; browser screenshot shows the red line removed and the white graphic positioned over the cameo’s upper section. Screenshot: `Media/screenshots/tsr-hero-adjusted.png`.

### 2026-08-13 — Restore `/tsr/` hero cameo and white nav logo
- Problem: the NoesisGroup `/tsr/` build had lost the building cameo from the hero, and the upper-left nav logo was rendering in full color.
- Solution: restored the original building vignette asset and hero layer, restored the white logo filter, and changed Vite output URLs to relative paths so the same build works at `/tsr/`.
- Verification: rebuilt and pushed commits `99561c7` and `5d864bb`; `https://noesisgroup.com/tsr/` browser screenshot shows the cameo, white nav logo, white hero mark, and rendered navigation/content. Screenshot: `Media/screenshots/tsr-fixed.png`.

### 2026-08-12 — wildcatart.com blank page
- Problem: `public_html/scottish-rite/index.html` was missing React/ReactDOM/Babel runtime imports and contained three malformed JSX closures plus two stray gallery insertions, leaving the root blank.
- Solution: restored the three CDN imports, removed the stale React integrity attribute, corrected the three `}}> ` closures, and removed the misplaced gallery blocks over SSH. No intended layout or feature logic changed.
- Verification: live page returned HTTP 200; browser rendered a populated React root (2,177,427 characters), 10 sections, and visible headings including “A Brotherhood Rooted in Tucson” and “Contact the Valley”.

### 2026-08-11 — Broken image links
- Problem: live site referenced missing `/uploads/logo-1776712250947.png`; the new Vite bundle was unavailable under its newly generated asset filename.
- Solution: changed logo references to `/images/logo.png`, bundled logo/gallery assets, reused an existing served bundle path, and deployed commits `101dc90`, `13eac33`, and `c17068f`.
- Verification: live page rendered; logo and all eight gallery images reported nonzero natural widths.

### 2026-08-11 — NoesisGroup `/tsr` deployment
- Deployed the standalone `Scottish Rite.html` source to `/var/www/vhosts/noesisgroup.com/httpdocs/tsr/index.html`.
- Verification: `https://noesisgroup.com/tsr/` returned HTTP 200 and browser rendering showed the Tucson Scottish Rite navigation, hero, sections, and embedded images.

### 2026-08-11 — Sync Zo build to `/tsr`
- Problem: `/tsr` was serving the older standalone HTML version instead of the Vite/React version at `scottish-rite-jaknyfe.zocomputer.io`.
- Solution: rebuilt the Vite source, changed shared image references to resolve relatively on both hosts, uploaded `dist/` to `/tsr`, and pushed Zo sync commit `87f4163`.
- Verification: both live pages render the same navigation, hero, sections, and eight gallery images; `/tsr` images report nonzero natural widths.

### 2026-08-11 — Restore CalendarWiz
- Problem: the site had reverted to hard-coded event cards; the older CalendarWiz `ucfeeder.php` integration also failed when dynamically injected because it relies on `document.write`.
- Solution: restored the CalendarWiz calendar and full-calendar modal using direct responsive iframe URLs for calendar `tucsonscottishrite`.
- Verification: Zo and `/tsr` both render the CalendarWiz iframe; clicking `View Full Calendar` creates the modal iframe. Commits: `7c8c54c`, `06271fb`, `c66e6d5`.
