# Knights of St. Andrew Website — Agent Instructions

## Overview
This is a standalone Vite + React website for the Knights of St. Andrew (KSA) of the Valley of Tucson Scottish Rite.
It features an animated hero section, virtues accordion, history timeline, activities gallery, leadership roster, and a petition-to-join form.

## Hosting Target
- **Zo Computer** — `https://scottish-rite-kst-andrew-jaknyfe.zocomputer.io/`
- **Stack**: Vite 8 + React 19 + TypeScript
- **Source**: `/home/workspace/scottish-rite-kst-andrew/` (Vite project)
- **Entry**: `src/main.tsx`
- **Build**: `bun run build` → `dist/`
- **Deploy target**: Served via a user service that builds and serves the `dist/` folder

## Deployment Rule
When making edits, updates, or changes to the Knights of St. Andrew website:

1. `cd /home/workspace/scottish-rite-kst-andrew && bun run build`
2. `cp dist/index.html dist/assets/* /home/workspace/scottish-rite-kst-andrew/` (already in place)
3. Restart the user service to pick up the new build:
   - The service entrypoint is: `/home/workspace/scottish-rite-kst-andrew/serve.sh`
   - Which runs: `cd /home/workspace/scottish-rite-kst-andrew && bun run build && cd dist && python3 -m http.server 51001 --bind 0.0.0.0`
   - To restart: `update_user_service` with the service ID (currently `svc_hdrtSM4VFtc`)

## User Preferences
- Don wants instructions written to memory so they persist when context runs out.
- Use project AGENTS.md files to store agent-level instructions.
- Don corrects UI/layout issues precisely and expects fast convergence.

## Key Features
- **Hero**: Animated saltire grid, floating crosses, ornamental rings, emblem with pulsing effects
- **Virtues**: Nine virtues of a Knight in an accordion layout (click to expand/collapse)
- **History**: Vertical timeline of the KSA from 1993 to present
- **Activities**: Grid of service icons with hover effects
- **Leadership**: Officer cards with ranks, names, and bodies
- **Join**: Simple contact form for those interested in petitioning to join
- **Footer**: Copyright, links, and contact information

## Design Tokens
Defined in `src/App.css`:
- `--navy`: #0a1628 (primary background)
- `--navy-light`: #152238
- `--green-deep`: #1a3a2a
- `--green`: #2d6a4f
- `--green-light`: #40916c
- `--gold`: #b8953a
- `--gold-light`: #d4a84b
- `--cream`: #f5f1e8
- `--crimson`: #8b1a1a
- `--white`: #ffffff
- `--text-body`: #3a3a3a
- `--text-muted`: #6b7280
- `--font-display`: 'Georgia', 'Times New Roman', serif
- `--font-body`: system fallback stack

## Service Management
The site is served by a user service with ID `svc_hdrtSM4VFtc` (label: scottish-rite-kst-andrew).
The entrypoint script is `/home/workspace/scottish-rite-kst-andrew/serve.sh` which:
1. Changes to project directory
2. Runs `bun run build`
3. Changes to `dist/` directory
4. Serves via Python's http.server on port 51001 bound to 0.0.0.0

To view logs:
- `cat /dev/shm/scottish-rite-kst-andrew.log`
- `cat /dev/shm/scottish-rite-kst-andrew_err.log`

To restart the service after changes:
```bash
update_user_service --service-id svc_hdrtSM4VFtc
```
(Note: The service auto-restarts when updated via `update_user_service`)

## Development
- `bun run dev` for local development with hot reload
- `bun run build` for production build
- `bun run preview` to preview the built site locally

## Custom Domains
None currently configured — the site uses the default `*.zocomputer.io` subdomain.

## Issue Log

### 2026-08-11 — Zo preview was blank/unreachable
- **Problem:** Zo configured the development preview for port 51000, but Vite ignored the injected `PORT` and listened on 5173.
- **Fix:** Configured Vite to bind `0.0.0.0` and use `Number(process.env.PORT) || 5173`.
- **Result:** Browser snapshot at port 51000 shows the rendered KSA homepage; production build passes.

### 2026-06-20 — Homepage rendered blank due to undefined nav logo variable
- **Problem:** The production homepage loaded a blank navy screen even though the HTML, JS, and CSS were served correctly.
- **Tried:** Verified the deployed assets, checked browser screenshots, inspected service logs, and confirmed React root was empty.
- **Root cause:** `src/Nav.tsx` referenced `ksaLogo` without importing or defining it, which caused the app render to fail.
- **Fix:** Replaced the broken logo reference with the public asset path `/ksa-logo.png`, rebuilt the site, and restarted the service.
- **Result:** Homepage now renders correctly with the full KSA layout and hero section visible.
