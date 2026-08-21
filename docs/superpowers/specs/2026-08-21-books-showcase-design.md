# Books Showcase Design

## Objective

Create a public Zo Space page at `/books` that presents Don Lowery's three-book catalog in an immersive editorial showcase inspired by the motion language of the ThreeUI reference, without copying its branding or copy.

## Catalog

1. *Outsource Your Own Brain* — use the existing designed cover.
2. *Bound by Ash and Thorn* — use the existing designed cover.
3. *Project Orion: Alpha Protocol* — use the supplied cover at `/home/.z/chat-uploads/project_orion_book_cover-0016693da393.png`.

## Experience

- Dark olive and restrained gold art direction; oversized editorial title and asymmetric three-cover composition.
- Each physical-looking cover has perspective, layered shadows, subtle pointer parallax, hover lift, and staggered entrance choreography.
- Cards open a focused book-detail state. Menu controls, arrow keys, and touch swipes move between titles.
- Ambient grain, depth layers, and smooth transitions remain, with a complete reduced-motion fallback and keyboard-accessible controls.
- Existing covers are treated as source artwork: no regeneration, redrawing, or alteration.

## Technical Boundaries

- Implement as an isolated public Zo Space page route: `https://jaknyfe.zo.space/books`.
- Upload only the provided Project Orion cover plus any existing source covers required by the page as Space assets.
- Use the platform's installed React and Tailwind capabilities; no package installation.

## Definition of Done

The public route renders all three correct covers and titles, retains the core motion effects, works with mouse, keyboard, touch, and reduced-motion preferences, and is verified with a full-page screenshot.
