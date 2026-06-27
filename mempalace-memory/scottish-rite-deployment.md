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

## Service Info
- Service: `svc_zLzh3iJP_c4` → `python3 -m http.server 3102` serving `/home/workspace/scottish-rite-site/`
- Public URL: `https://scottish-rite-jaknyfe.zocomputer.io/`
- Port: 3102

## Always-On Rule
When deploying Scottish Rite site changes:
1. Always build first: `bun run build` in the source directory
2. Always copy artifacts to the serve directory
3. Never serve from the Vite `dist/` directly
