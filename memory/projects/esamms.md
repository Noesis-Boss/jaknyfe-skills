---
name: esamms
description: eSAMMs project — two deployment targets (Zo-hosted + ServerByt/wildcatart.com), vite base config, SSH key status
type: project
---

# eSAMMs Project

## Two Deployment Targets

### 1. Zo-Hosted (primary)
- **URL:** `https://esamms-jaknyfe.zocomputer.io/`
- **Config:** `zosite.json` → `publish` block
- **Entrypoint:** `bun run prod`
- **Port:** 57138 (published)
- **Vite base:** `/`
- **Deploy method:** `publish_site esamms --public=true`

### 2. ServerByt / wildcatart.com (legacy/mirror)
- **URL:** `https://esamms.wildcatart.com/`
- **SSH:** `wildcatart.com@ssh.us.stackcp.com` (port 22)
- **SSH key location:** `~/.ssh/serverbyt_key` and `/root/.ssh/serverbyt_key` (same file)
- **Server home:** `/home/sites/42a/b/be19d0f08d/`
- **Document root:** `~/public_html/esamms/` (lowercase — matches subdomain name)
- **Deploy command:** `rsync -avz -e "ssh -i ~/.ssh/serverbyt_key -p 22 -o StrictHostKeyChecking=no" --delete /home/workspace/esamms/dist/ wildcatart.com@ssh.us.stackcp.com:public_html/esamms/`
- **Vite base:** `/`
- **SSH key was lost on 2026-06-29, restored 2026-06-30 from user's backup**

## Key Rule
- `vite.config.ts` must ALWAYS use `base: "/"` — both deployments serve from domain root.
- Never change `base` to `/esamms/` — that was the cause of the blank page.

## Source
- Workspace: `/home/workspace/esamms/`
- vite.config.ts: `base: "/"`
- zosite.json: publish port 57138
