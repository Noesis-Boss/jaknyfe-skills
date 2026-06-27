# Session Log: 2026-06-27

## Task: Deploy ScholarSearch to noesisgroup.com/scholarsearch/

### Deployment Summary

**Live URL**: https://noesisgroup.com/scholarsearch/

### What was done

1. **Built the site** with `bun run build` in `/home/workspace/scholarsearch-site`
2. **Updated `vite.config.ts`** — set `base: "/scholarsearch/"` for subpath deployment
3. **Updated `src/App.tsx`** — set `BrowserRouter basename="/scholarsearch/"` so React Router resolves paths correctly
4. **Updated `src/pages/Home.tsx`** — changed API fetch calls from `/api/*` to `/scholarsearch/api.php/api/*` (direct PHP path)
5. **Created `.htaccess`** — SPA routing rules to handle React Router paths
6. **Created `/home/workspace/deploy_scholarsearch_noesisgroup.sh`** — deployment script
7. **Uploaded to noesisgroup.com** via SSH+sshpass+rsync:
   - `dist/*` → `/var/www/vhosts/noesisgroup.com/httpdocs/scholarsearch/`
   - `api.php` → same directory
   - `data/scholarships.db` → same directory
8. **Committed changes** to git on master branch (local commit `36550f9`)

### Critical issues fixed

- **Issue 1: Blank page** — React wasn't hydrating because `BrowserRouter basename` was `/` instead of `/scholarsearch/`. Fixed by updating `App.tsx`.
- **Issue 2: rsync --delete wiped API** — The `--delete` flag in rsync removed `api.php` and the database directory. Fixed by re-uploading them separately after the main rsync.
- **Issue 3: API path** — Frontend originally called `/api/scholarships` which would require `.htaccess` rewrites. Changed to direct path `/scholarsearch/api.php/api/scholarships` which works without rewriting.

### Verification

- **API Health**: `https://noesisgroup.com/scholarsearch/api.php/api/health` → `{"status":"ok"}`
- **API Stats**: `https://noesisgroup.com/scholarsearch/api.php/api/stats` → 8,255 scholarships, 31 categories
- **API Scholarships**: `https://noesisgroup.com/scholarsearch/api.php/api/scholarships` → returns results (e.g., Fulbright, Marshall)
- **Frontend**: React hydrates correctly, shows search bar, stats sidebar, scholarship cards (Marshall Scholarship visible), news/stats sections

### Server paths

- Document root: `/var/www/vhosts/noesisgroup.com/httpdocs/`
- App directory: `/var/www/vhosts/noesisgroup.com/httpdocs/scholarsearch/`
- Database: `/var/www/vhosts/noesisgroup.com/httpdocs/scholarsearch/data/scholarships.db`
- API: `/var/www/vhosts/noesisgroup.com/httpdocs/scholarsearch/api.php`

### SSH credentials

- Host: 65.38.97.58 (ssh config alias: noesisgroup)
- User: noesisuser
- Password: `@EUjgrN9fkr5li8$` (stored in `/home/workspace/deploy_noesisgroup.sh`)

### Known issues

- **Git push rejected** — Remote has commits not in local. Needs `git pull --rebase` before push.
- **Search functionality** — The `.htaccess` rewrites aren't working (mod_rewrite may not be enabled), but the direct `/api.php/api/*` path works fine for the frontend.

### Deployment script

```bash
/home/workspace/deploy_scholarsearch_noesisgroup.sh
```

### Screenshots saved

- `/home/workspace/scholarsearch-noesisgroup-deployed.jpg` — Full page
- `/home/workspace/scholarsearch-noesisgroup-cards.png` — Scholarship cards section