# Zo Sidebar (Chrome MV3 extension)

Chrome extension: chat with Zo Computer from a sidebar; optional browser-control actions
executed by the background service worker. Uses a **local relay** (`relay/relay.ts`) that
proxies `POST /zo/ask` to `https://jaknyfe.zo.computer/zo/ask`, injecting the Zo API token
per-request (no token sent to the relay client).

## Architecture
- `manifest.json` — MV3. `background.service_worker = background.js`; `side_panel.default_path = sidepanel.html`;
  content script `token-capture.js` on `*://*.zo.computer/*` scans the Advanced settings page for `zo_sk_...` tokens.
- `background.js` — service worker. Opens a long-lived port (`name: 'sidebar'`) to the sidepanel.
  Handles: `getSettings`, `saveSettings`, `login` (opens zo settings tab), `setToken`, `clearToken`,
  `send` (runs the chat + browser-control loop), `resetChat`. Stores token under `chrome.storage.local.zoToken`.
  Streams assistant text via port messages: `auth`, `settings`, `tokenCaptured`, `user`, `assistantStart`,
  `token`, `assistantEnd`, `actionStart`, `actionEnd`, `error`, `notice`, `chatReset`.
- `sidepanel.js` — connects to background via `chrome.runtime.connect({name:'sidebar'})`, renders the chat,
  and sends the above message types. **Token storage is unified on `zoToken` (set via `setToken` → background).**
- `relay/relay.ts` — Bun server on `http://127.0.0.1:18720`. Forwards to upstream `/zo/ask`, adding
  `Authorization: Bearer <token>` and `Accept: application/json`; proxies SSE stream back.
- `token-capture.js` — content script; polls page text for `zo_sk_...`, posts `tokenCaptured` to background.

## Build / run
- Relay: `cd /home/workspace/zo-chrome-sidebar && bun run relay/relay.ts` (or `bun build relay/relay.ts --outfile relay && ./relay`).
- Load unpacked: chrome://extensions → Developer mode → Load unpacked → select `zo-chrome-sidebar/`.
- **Important:** dragging a new folder into chrome://extensions duplicates the extension. Remove ALL existing
  "Zo Sidebar" entries before loading a new version, or the version number will look stale.

## Issue Log
### 2026-07-10 — Paste token / login / no-response / TypeError (resolved at v0.1.9)
- **Symptom:** "Paste token" button did nothing; pasted token didn't save; "Log in to Zo" never flipped to
  "Connected"; no chat response; console `TypeError: DEFAULT_SETTINGS is not defined` and
  `Cannot read properties of null (reading 'style')`.
- **Root cause:** `sidepanel.js` referenced element IDs that didn't exist in `sidepanel.html`
  (`inputWrap`, `tokenInput`, `pasteButton`, `tokenInputWrap`) → null `.style` throws. It was also a broken
  divergent design (local relay fetch + undefined `DEFAULT_SETTINGS`) that never wired the Send button or
  connected to the background port. Token storage was inconsistent (sidepanel saved `token`, background read `zoToken`).
- **Fix:** Rewrote `sidepanel.js` to use the correct port protocol to `background.js`; fixed all element IDs to
  match the HTML; fixed `updateAuth` logic (connected → show composer + hide paste; not connected → hide composer
  + show paste); wired Send/Enter, New chat, settings, login, paste-token, clear-token; unified token on `zoToken`;
  added `try/catch` error handling in `token-capture.js`; bumped version 0.1.8 → 0.1.9.
- **Verification:** `node --check` passes on all JS; `bun build relay` OK; grep confirms no stray IDs and no
  `DEFAULT_SETTINGS` reference in `sidepanel.js`; manifest version = 0.1.9.
- **Still open / next:** Verify Hermes-free browser-automation wiring (the `browserControl` toggle + action loop)
  end-to-end in a real Chrome session. Confirm relay auto-start on user login (currently manual `bun run`).
