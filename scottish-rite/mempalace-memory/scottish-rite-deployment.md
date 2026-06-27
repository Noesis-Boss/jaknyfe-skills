# Scottish Rite Site — Deployment Memory

## Anti-Patterns Learned 2026-04-29

### Problem: Huge inline bundle served instead of compiled assets
- **Wrong**: Serving `/home/workspace/scottish-rite/dist/` directly via `python3 -m http.server`
- **Why**: Vite's `dist/index.html` in dev/dev mode had a 1.6MB+ inline bundle (all React compiled on-page via Babel) instead of the proper 171KB external JS bundle + 1.9KB HTML
- **Result**: Page load was 1.6MB+ of inline JS per request

### Solution: Two-directory pattern
1. **Source**: `/home/workspace/scottish-rite/` — Vite project with TypeScript source
2. **Serve directory**: `/home/workspace/scottish-rite-site/` — git-tracked, only deploy artifacts

**Build workflow** (must follow every time):
```bash
cd /home/workspace/scottish-rite
bun run build
cp dist/index.html /home/workspace/scottish-rite-site/
cp dist/assets/* /home/workspace/scottish-rite-site/assets/
```

Then push to GitHub per user_rule.

## Source-of-Truth: `scottish-rite-site/` is always the canonical deploy source

**The `scottish-rite-site/` directory is the single source of truth for all three deployment targets** (zo.space API route, external hosting on port 3102, and wildcatart.com rsync). It must always contain the correct, production-built artifacts.

**When new content is uploaded via zip or direct copy:**
- Unzip extracts to `scottish-rite/` (Vite source dir) — this is NOT a deployment target
- `scottish-rite/dist/` is an intermediate build output — NOT a deployment target
- **Always copy uploaded content to `scottish-rite-site/`** as the final step before deploying
- For zo.space specifically: `scottish-rite-site/index.html` is read directly; update it in place if the zip contains an `index.html`
- For external hosting: restart the service (`update_user_service` with `service_id=svc_zLzh3iJP_c4`) to pick up new files in `scottish-rite-site/`

**Never let `scottish-rite/` or `scottish-rite/dist/` be the deployment source.** They are Vite source + build intermediates. Only `scottish-rite-site/` is the serve directory.

## Service Info
- Service: `svc_zLzh3iJP_c4` → `python3 -m http.server 3102` serving `/home/workspace/scottish-rite-site/`
- Public URL: `https://scottish-rite-jaknyfe.zocomputer.io/`
- Port: 3102

## Always-On Rule
When deploying Scottish Rite site changes:
1. Always build first: `bun run build` in the source directory
2. Always copy artifacts to the serve directory
3. Never serve from the Vite `dist/` directly
