# Scottish Rite Deploy Memory

## Key Paths
- Build source: `/home/workspace/scottish-rite/`
- Live site: `https://scottish-rite-jaknyfe.zocomputer.io/`
- Git serve dir: `/home/workspace/scottish-rite-site/`

## Deploy Sequence
1. `cd /home/workspace/scottish-rite && bun run build`
2. `cp dist/index.html dist/assets/* /home/workspace/scottish-rite-site/`
3. `cd /home/workspace/scottish-rite-site && git add . && git commit -m "desc" && git push`

## Zip Extraction Fix
The zip extracts to `/home/workspace/scottish-rite/`. The zip contains `.jsx` component files that overwrite the proper `.tsx` files AND they lack `export` statements (e.g. `const SRNav` vs `export const SRNav`).
AFTER extracting: `rm /home/workspace/scottish-rite/src/components/*.jsx`
THEN build.
