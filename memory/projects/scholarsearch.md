---
name: scholarsearch-project
description: ScholarSearch — Zo frontend and publishing scaffolding with AdSense integration
type: project
---

# ScholarSearch

## Overview
Zo frontend and publishing scaffolding for a scholarship discovery tool. Includes Google AdSense integration and API routes for scholarship data.

## Key Paths
- Source: `/home/workspace/scholarsearch/`
- Site scaffold: `/home/workspace/scholarsearch-site/`
- Build script: `/home/workspace/scholarsearch-site/build.js`
- Vite config: `/home/workspace/scholarsearch-site/vite.config.ts`
- zosite.json: `/home/workspace/scholarsearch-site/zosite.json`

## Known Work
- Inserted Google AdSense into `scholarsearch/index.html`
- Created Zo-site/space structure under `/home/workspace/scholarsearch-site`
- Added Zo space routes: `/scholarsearch` (page) and `/api/scholarships` (API)
- bunfig.toml configured

## Status
**Live at:** https://noesisgroup.com/scholarsearch/

Deployed 2026-06-27 to noesisgroup.com hosting (Plesk/psacln) via SSH.
- Frontend: Vite/React SPA built with base path `/scholarsearch/`
- API: PHP + SQLite (`api.php`) served at `/scholarsearch/api.php/api/*`
- Database: 8,255 scholarships, 31 categories
- Deploy script: `file 'deploy_scholarsearch_noesisgroup.sh'`

## Issue Log - 2026-06-27: noesisgroup.com deploy
- **Problem**: Page loaded HTML but React didn't hydrate — root was empty.
- **Root cause**: `BrowserRouter basename="/"` mismatched subpath `/scholarsearch/`.
- **Fix**: Changed `basename="/scholarsearch/"` in `src/App.tsx`, rebuilt, re-uploaded.
- **Secondary issue**: Frontend `fetch('/api/...')` used relative path → updated to `/scholarsearch/api.php/api/...`.
- **Verification**: Screenshot confirmed hero, search bar, scholarship cards render. API stats returned 8,255 scholarships across 31 categories.

## Issue Log - 2026-06-02
- **Problem**: Missing 'src/pages/Home.tsx' and static 'index.html' preventing React hydration.
- **Fix**: Reconstructed 'Home.tsx' based on 'index.html' structure. Updated 'index.html' to mount React. Fixed server routing in 'server.ts'.
- **Status**: Fixed and pushed to git. Dev server verified on port 57263.
- **Enhancement (2026-06-02)**: Improved UI contrast and accessibility across all components.
- **Verification**: Confirmed via screenshot 'scholar-contrast-fixed.png'.
- **Enhancement (2026-06-02)**: Fixed contrast issues in FAQ and section headers. Darkened text and labels for better readability.