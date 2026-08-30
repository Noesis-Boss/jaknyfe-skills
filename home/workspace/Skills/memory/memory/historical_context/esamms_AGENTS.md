# AGENTS.md

## Project Notes
- Zo Site project for eSAMMs (electronic Southern Arizona Master Masons).
- Source lives in this directory and is published via `zosite.json`.
- Public production URL: `https://esamms-jaknyfe.zocomputer.io`

## Issue Log

### 2026-05-04 — eSAMMs site not showing on hosting platform
**Problem**
- The eSAMMs site existed in `/home/workspace/esamms` but was not showing on the hosting platform.

**What was tried**
1. Checked Zo Space routes — **failed / not relevant**.
   - Result: eSAMMs was not a zo.space route.
2. Inspected site project files (`README.md`, `zosite.json`, `package.json`, `server.ts`) — **worked**.
   - Result: confirmed eSAMMs is a Zo Site with publish config.
3. Ran production build (`bun run build`) — **worked**.
   - Result: build completed successfully.
4. Published the site with the Zo Sites publish flow — **worked**.
   - Result: created hosted service `esamms` and assigned public URL.
5. Visually verified the rendered site in browser — **worked**.
   - Result: homepage rendered correctly with hero, calendar section, lodge cards, and footer.

**Final solution**
- Published the Zo Site from `/home/workspace/esamms` to the hosting platform.
- Confirmed public URL: `https://esamms-jaknyfe.zocomputer.io`
- Confirmed the hosted service now appears in the service list as `esamms`.