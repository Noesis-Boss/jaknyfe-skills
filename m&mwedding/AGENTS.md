# m&mwedding — Marsha & Michael's Magical Day Gallery

## Feature Log

- 2026-08-03: Created wedding photo gallery on zo.space. 161 photos of the Marsha & Michael beach wedding (originals in `/home/workspace/m&mwedding/photos/`).
- 2026-08-03: Moved site from `/photos` → `/m&mwedding`. Old `/photos` URL now redirects to `/m&mwedding`.
- 2026-08-03: Full-size modal viewer with left/right pagination, keyboard arrows, swipe, photo counter.

## Routes (zo.space)

- Page: `/m&mwedding` (public) — masonry gallery + modal viewer
- API: `/api/m&mwedding/list` (public) — returns `{ files, count }`
- API: `/api/m&mwedding/serve/:name` (public) — serves image bytes
- Redirect: `/photos` → `/m&mwedding`

## Layout notes

- Wedding motif: Great Vibes script title, Cormorant Garamond body, sage `#8a9b7c` + gold `#c2a878` accents, heart dividers, cream `#faf6ef` background.
- Modal: click thumbnail opens full-size; arrows / swipe / ←→ keys paginate; Escape closes; counter "N of 161".
- 2026-08-03: Fixed: modal Download button downloaded only current photo regardless of selection. Now: 0 selected → downloads current photo; 1+ selected → downloads ALL selected photos as zip (button label shows count, e.g. "Download 3"). Verified live: 3-photo zip contained all 3 files.
- 2026-08-03: Title now reads "Marsha & Michael's Magical Day — Thursday, July 23rd, 2026" (date added to page title + browser tab). Verified live via screenshot.
- 2026-08-03: Location line "CANCUN, MEXICO" added below the date in header. Verified live via screenshot (file 'm&mwedding/location-check.png').
