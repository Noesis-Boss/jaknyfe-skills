# Scottish Rite Website — Agent Instructions

## Deployment Rule (ALWAYS)
When making edits, updates, or changes to the Scottish Rite website at https://scottish-rite-jaknyfe.zocomputer.io/:
1. Build from source: `cd /home/workspace/scottish-rite && bun run build`
2. Copy artifacts: `cp dist/index.html dist/assets/* /home/workspace/scottish-rite-site/`
3. Commit and push: `cd /home/workspace/scottish-rite-site && git add . && git commit -m \"Update [description]\" && git push origin master`
4. NEVER serve directly from Vite dist/ output.

## Known Fixes Needed (from USER)
- Fix 1: [NOT YET RECORDED — pending user's details]
- Fix 2: [NOT YET RECORDED — pending user's details]
- Fix 3: [NOT YET RECORDED — pending user's details]

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