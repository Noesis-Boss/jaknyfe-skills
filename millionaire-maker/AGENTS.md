# Millionaire Maker

## Feature Log

- 2026-08-22: Retested the live report flow. The public endpoint returned HTTP 200, the popup rendered a complete final plan, accumulation and idea-matrix sections were present, and the warning text was absent. Screenshot saved as `report-verification.png`.

- 2026-08-21: Reworked final-report section formatting: pipe-delimited accumulation milestones and idea-matrix rows now render as responsive cards/tables, headings are normalized, and warning text is filtered before rendering. Local production build passed; live report generation remained upstream-pending during browser verification.

- 2026-08-21: Reformatted final-report rendering to remove `Warning: Skill descriptions...` lines, detect report sections, and group accumulation milestones into labeled cards with improved spacing and responsive styling. Local build and public input-page screenshot verified; live report interaction timed out during the model request, so the generated-report screenshot remains unconfirmed.

- 2026-08-21: Aligned the standalone final report window with the input page design system: dark olive background, Manrope/DM Mono typography, gold accents, matching card border/radius/shadow, and responsive spacing. Removed stale loading text from the public report popup. Local build and live screenshots verified.

- 2026-08-21: Reformatted the final report window with an editorial dark-gold layout, responsive typography, section hierarchy, readable paragraphs, and metadata. Local build and live page screenshot verified.

- 2026-08-20: Added unambiguous default profile values: United States, USD, and Moderate risk tolerance. Local build passed; live browser snapshot verified the defaults.

- 2026-08-20: Added `Export userdata.md` to the local and public frontend. It downloads the current profile fields in the same `Label: value` format accepted by Markdown upload; build and live screenshot verified.

## Issue Log

- 2026-08-22: Fixed report non-completion when the browser relay returned `Failed to fetch`. The public relay now allows 90 seconds, the popup shows progress immediately, client timeout/error states are explicit, and a deterministic profile-based fallback report opens when the model response is unavailable. Live endpoint returned HTTP 200; browser verification of the fallback popup is pending.

- 2026-08-21: Report generation timed out because the page wrapped the full wealth prompt in a second business-plan instruction, while the public relay prepended another instruction and waited synchronously for a long Codex response. Reduced the public handoff to 2,600 characters with one concise instruction and a 45-second timeout; timeout responses now return readable HTTP 504 JSON. The report popup no longer closes into a blank tab on failure; it displays the error. Public page screenshot verified after Space restart; substantive endpoint timing remains upstream-dependent.

- 2026-08-21: Resolved recurring public 502s caused by the relay's 18-second timeout expiring before direct Codex responses completed. Removed the immediate `auto` fallback and set the public `/api/millionaire-maker/ask` relay to one non-streaming Codex request with a 60-second timeout. After restarting the temporarily offline Zo Space host, a production-shaped POST returned HTTP 200 with a complete plan; the public page screenshot also renders correctly.

- 2026-08-21: Reduced recurring public HTTP 502 risk by capping the relay handoff at 4,000 characters and the final response at 500 words, with a 25-second upstream timeout. Short health request returned HTTP 200; live page screenshot verification remains required after the next full analysis.
- 2026-08-21: Added a bounded Codex-first request with `auto` fallback for upstream 5xx responses and non-streaming output. The public origin still returns Cloudflare HTTP 502 for substantive plan prompts while health probes return 200; this is currently an upstream Zo availability failure, not a route or build failure.

- 2026-08-21: Fixed recurring public HTTP 503s by removing the duplicate sequential model-call loop from `/api/millionaire-maker/ask`. The relay now makes one bounded request with the Codex – GPT 5.6 Luna model, returns readable upstream errors, and was verified with a live HTTP 200 response and browser screenshot.

- 2026-08-21: Confirmed and configured the available model `Codex - GPT 5.6 Luna` using identifier `byok:66b916e9-a61f-4184-badb-22020c0b2fd9`. A direct Zo submission returned `ok: True`; local build passed and the public relay was synced.

- 2026-08-21: Switched the local Vite relay and public `/api/millionaire-maker/ask` route from the BYOK model to `opencode_free`. Build passed; the public smoke test was blocked by a Cloudflare/origin HTTP 502 after the route sync, with no Zo route errors reported.

- 2026-08-21: Report generation still fails in the public browser with `Failed to fetch`; the page loads and the API route exists, but the public POST does not return a usable response. The relay was tightened to bounded 25-second upstream attempts, one short retry, a 700-word fallback prompt, and consistent 502 errors. Browser verification still failed, indicating a Zo public API/proxy exposure or upstream availability issue rather than a form/rendering problem.

- 2026-08-20: Fixed recurring 503/new-window failure on the public page. The report window now opens synchronously before the async request, receives the fresh response directly (avoiding stale React state), and closes on failure. Reduced the upstream handoff to 8,000 characters and the final report to 900 words. Public page screenshot and bounded relay smoke test verified.

- 2026-08-20: Fixed recurring public 503s by changing the frontend from two sequential `/zo/ask` calls to one bounded call that directly produces the final business-plan-builder formatted result. Public endpoint returned HTTP 200; live page screenshot verified.

- 2026-08-20: Rechecked the reported HTTP 503. The public `/api/millionaire-maker/ask` relay is present, retries transient 429/502/503/504 responses, and a live production-shaped request returned HTTP 200 with analysis output. The failure was transient upstream availability, not a route or frontend error.

- 2026-08-20: Fixed Export userdata.md and Upload .md alignment by giving the action group consistent flex spacing, minimum button height, wrapping, and responsive header behavior; public page screenshot verified.

- 2026-08-20: Public relay route was correct, but upstream `/zo/ask` intermittently returned 502, 503, and 429 during the two-pass analysis. Added a 90-second timeout, retries for 429/502/503/504, bounded backoff, and `Retry-After` handling. A direct relay smoke test previously returned HTTP 200; browser verification still needs a clean post-rate-limit run.

- 2026-08-20: Public analysis requests returned HTTP 503 upstream. Added two retries with backoff to `/api/millionaire-maker/ask` and restarted zo.space. Browser verification still reports `Failed to fetch`, so the upstream Zo ask service remains unavailable or the public API connection is failing; no successful final plan confirmed.

- 2026-08-20: Fixed recurring analysis failures by parsing relay responses before JSON decoding, surfacing HTTP/upstream errors, and reducing the business-plan handoff to 12,000 characters with a 1,500-word output cap. Both live passes returned HTTP 200; live page screenshot verified.

- 2026-08-20: Fixed business-plan pass failures by bounding the first analysis handoff to 24,000 characters, validating the second response body, and surfacing readable upstream errors.

- 2026-08-20: Fixed the business-plan-builder second pass asking for skill approval or more context. The relay prompt now explicitly executes autonomously, states assumptions for missing data, and continues to the final plan.

- 2026-08-20: Added an automatic business-plan-builder second pass after the seven-phase wealth analysis. The final plan is shown step-by-step with expected outcomes and can be opened in a clean new browser window; local build and public route verification passed.

- 2026-08-20: Fixed public Zo Space analysis failures by adding the missing `/api/millionaire-maker/ask` route expected by the page. Live POST smoke test returned HTTP 200 and a real `/zo/ask` response; page screenshot verified.
- 2026-08-20: Added a server-side `/api/ask` relay. The Run wealth analysis action sends the generated seven-phase prompt to `/zo/ask` with the current Zo model, keeps the identity token server-side, and renders loading, error, and result states. `bun run build` passes; browser screenshot verified the updated form and action.
- 2026-08-20: Allowed the Tailscale hostname `zoltan` in Vite's dev-server host allowlist.
- 2026-08-20: Added `.md` upload parsing for profile variables in `Label: value` format, with multiline support for text areas and a loaded-variable status message.
