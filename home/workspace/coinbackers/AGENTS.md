# CoinBackers

## Issue Log

- 2026-09-02: Added JSON-backed campaign persistence in `data/campaigns.json`; campaign creation and pledges now save after successful API writes and reload after server restarts. Build passed, restart persistence returned HTTP 200, and Explore rendered in `coinbackers-persistence-verified.png`.

- 2026-09-02: Completed the campaign creation upload path. Added `/api/upload` with image-type and 5MB validation, generated safe unique filenames under `dist/uploads`, and added visible form errors for failed uploads or campaign creation. Build passed, upload returned HTTP 201, and the create page was screenshot-verified at `coinbackers-create-upload-verified.png`.

- 2026-09-01: Fixed remaining link-driven runtime errors. Added campaign detail, campaign creation, pledge, and price API endpoints; added missing React imports to all JSX pages. Build passed and browser navigation `/` → `/explore` → `/campaign/1` now renders without `ReferenceError: React is not defined`.

- 2026-09-01: Coin opacity appeared unchanged because the arbitrary Tailwind opacity utility was not reliable in the served bundle; moved the 90%-transparent setting to inline image style and bumped the asset cache key to `v=3`.
- 2026-09-01: Verified all homepage destinations and fixed direct-route 404s by adding an SPA fallback in `server.ts`; `/`, `/explore`, `/create`, `/dashboard`, and `/campaign/1` now return 200 while missing assets still return 404.

- 2026-09-01: Added an explicit Hono route for `/images/coins/:file` after nested PNG requests returned zero-byte responses during verification.

## Feature Log

- 2026-09-02: Added a Dashboard wallet-connection affordance. Browser wallets use `eth_requestAccounts`; environments without a provider use a clearly labeled local demo address, persisted in local storage. Build passed and the rendered Dashboard was screenshot-verified at `coinbackers-wallet-verified.png`.

- 2026-09-02: Added live Explore search and category filtering for Technology, Sustainability, and Community campaigns. Search/category states update the visible project count and empty state; build and rendered-page screenshot passed at `coinbackers-explore-filters-final.png`.

- 2026-09-01: Added a white CoinBackers header with coin icon and a functional “Back to Main” link to the Explore Projects page. Build passed and the rendered page was screenshot-verified at `coinbackers-explore-back-main-verified.png`.

- 2026-09-01: Generated 24 distinct coin artwork PNGs, removed the magenta key background, and arranged them as randomized low-opacity watermarks inside the purple hero. Build passed and the rendered hero was screenshot-verified at `coinbackers-watermarks-verified.png`.

- 2026-09-01: Updated the homepage navigation to use the same white surface as the content area and added a CoinBackers coin icon beside the brand title. Vite build passed and the rendered page was screenshot-verified.

- 2026-09-01: Fixed missing homepage navigation. Added a visible responsive header in `src/pages/Home.tsx` with CoinBackers branding, Home, Explore, Dashboard, and Start Campaign links; desktop and mobile layouts use the existing hero palette. Vite build passed and the rendered page was screenshot-verified at `coinbackers-nav-verified.png`.

- 2026-09-01: Fixed blank home page. Cause was classic React JSX in `Home.tsx` and `hero.tsx` without `React` imports; added imports and raised the watermark layer above the hero background. Vite build passes and the rendered home page was browser screenshot-verified.
