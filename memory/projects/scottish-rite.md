---
name: scottish-rite-project
description: Scottish Rite website — Vite/React build deployed to scottish-rite-jaknyfe.zocomputer.io and wildcatart.com
type: project
---

# Scottish Rite Website

## Overview
Deployed Scottish Rite website for the Tucson chapter. Has been iteratively debugged for blank pages, 404s, and asset routing issues.

## Key Paths
- Source: `/home/workspace/scottish-rite/`
- Build output: `/home/workspace/scottish-rite/dist/`
- Serve directory: `/home/workspace/scottish-rite-site/`
- Vite config: `/home/workspace/scottish-rite/vite.config.ts`

## Deployment Method
1. Build: `cd /home/workspace/scottish-rite && bun run build`
2. Copy: `cp -r dist/* /home/workspace/scottish-rite-site/`
3. Push to git: `cd /home/workspace/scottish-rite-site && git add . && git commit -m "Update [description]" && git push origin master`
4. Automation: "Website Deployment to ServerByt Platform" (ID: b06329d6-b397-4555-975a-c4a827eada73) for wildcatart.com

## Known Issues (Resolved)
- Blank/white pages → fixed via Vite `base` path and `<base href>` in index.html
- Asset 404s → ensured asset paths match the serve directory
- Tailscale `tun` kernel support missing (can't use Tailscale for this deployment)

## URLs
- Zo hosting: https://scottish-rite-jaknyfe.zocomputer.io/
- Zo Space preview: https://jaknyfe.zo.space/scottish-rite/
- Custom domain: wildcatart.com (via ServerByt automation)

## Status
Active. Assets must be validated before publishing — always run build → copy → git push workflow.