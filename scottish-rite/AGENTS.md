# Scottish Rite Website — Agent Instructions

## Two Hosting Targets

The Scottish Rite site is deployed to TWO separate hosts with different codebases:

### 1. Zo Computer — `https://scottish-rite-jaknyfe.zocomputer.io/`
- **Stack**: Vite 4 + React 19 + JSX components
- **Source**: `/home/workspace/scottish-rite/` (Vite project)
- **Components**: `components/*.jsx` (sr-hero, sr-nav, sr-sections, sr-people, sr-contact)
- **Entry**: `src/main.tsx` → `src/App.tsx`
- **Build**: `bun run build` → `dist/`
- **Deploy target**: `/home/workspace/scottish-rite-site/` (git-pushed, zo computer pulls)

### 2. NoesisGroup — `https://noesisgroup.com/scottish_rite/`
- **Stack**: Single HTML file + React 18 + Babel standalone (NO Vite build)
- **Source of truth**: The `index.html` file itself (all components inline in `<script type="text/babel">`)
- **Server**: Apache/Plesk at `65.38.97.58`, user `noesisuser`
- **Deploy path**: `/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html`
- **Deploy method**: SCP the edited HTML file directly
- **SSH**: `sshpass -p '@EUjgrN9fkr5li8$' ssh noesisuser@65.38.97.58`

## Deployment Rule (ALWAYS — Both Targets)

When making edits, updates, or changes to the Scottish Rite website:

### Zo Computer (Vite build):
1. `cd /home/workspace/scottish-rite && bun run build`
2. `cp dist/index.html dist/assets/* /home/workspace/scottish-rite-site/`
3. `cd /home/workspace/scottish-rite-site && git add . && git commit -m "Update [description]" && git push origin master`

### NoesisGroup (single HTML):
1. Fetch current HTML: `sshpass -p '@EUjgrN9fkr5li8$' scp noesisuser@65.38.97.58:/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html /tmp/noesisgroup-scottish-rite.html`
2. Edit the HTML file locally (update officers, layout, etc.)
3. Upload: `sshpass -p '@EUjgrN9fkr5li8$' scp /tmp/noesisgroup-scottish-rite.html noesisuser@65.38.97.58:/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html`
4. Verify: `curl -sL https://noesisgroup.com/scottish_rite/ | grep 'Officer Name'`

**NEVER serve directly from Vite dist/ output for noesisgroup.com — it's a completely different codebase.**

## CRITICAL — Zip Extraction
When extracting a zip INTO the Scottish Rite project:
- The zip extracts to `/home/workspace/scottish-rite/`, NOT `scottish-rite-site/`
- The zip contains `.jsx` component files that OVERWRITE the proper `.tsx` files in `src/components/`
- These `.jsx` files use `const SRNav` (no export) instead of `export const SRNav` — they WILL break the build
- AFTER extracting, ALWAYS run: `rm src/components/*.jsx` before building
- Then build, copy to scottish-rite-site/, commit and push as normal

## User Preferences
- Don wants instructions written to memory so they persist when context runs out.
- Use project AGENTS.md files to store agent-level instructions.
- Don corrects UI/layout issues precisely and expects fast convergence.
