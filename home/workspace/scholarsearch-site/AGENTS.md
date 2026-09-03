# ScholarSearch Site Notes

## Issue Log

- 2026-09-03: Added `Skills/scholarship-discovery/scripts/audit_installer_links.py`, a fail-closed audit that scans both production databases and deactivates only active App Store, Play Store, or binary-installer URLs under validated backups and locked transactions. Dry run and commit run found 0 installer rows; a twice-daily ScholarSearch Installer-Link Audit automation is active.

- 2026-08-31: Fixed the live site rendering as unstyled text with missing visual treatment. `vite.config.ts` now loads `@tailwindcss/vite`, allowing the existing Tailwind stylesheet to compile its utility classes. Build passed, the hosted service restarted, and the live screenshot confirmed the header, icons, hero, search card, and stats panel render correctly.

- 2026-08-31: Fixed the blank production page and pagination contrast. Restored `src/main.tsx`, `src/index.css`, and `vite.config.ts`; added missing React namespace imports required by classic JSX files; removed the incorrect `/scholarsearch` router basename for the root-hosted deployment. Build passed, site republished, and the live page was screenshot-verified.
