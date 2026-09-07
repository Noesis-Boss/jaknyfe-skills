# Zo Sidebar — Chrome Extension

Chat with your Zo Computer from a Chrome sidebar, proxied through a tiny local
relay (so the Zo API CORS restriction never blocks the browser). Optional
browser-control lets Zo run actions on the current tab.

## Architecture

```
Chrome sidebar (MV3)  ──HTTP/SSE──▶  Local relay (Bun, 127.0.0.1:18720)
                                         │  injects Bearer token
                                         ▼
                                   api.zo.computer/zo/ask  (SSE stream)
```

- **Extension** (MV3): `manifest.json`, `background.js` (service worker), `sidepanel.html/js/css`, `token-capture.js` (content script).
- **Relay** (`relay/relay.ts`): local Bun server. Adds CORS + streams Zo's
  Server-Sent Events back to the extension. Forwards the Zo API token.

## Setup

### 1. Install the extension (dev mode)
- Chrome → `chrome://extensions` → enable **Developer mode**.
- **Load unpacked** → select this folder.
- Click the puzzle icon → pin **Zo Sidebar**.
- Click the icon → **Show side panel** (or right-click any page → *Zo Sidebar*).

### 2. Start the relay
```bash
cd relay
bun run relay.ts          # or: bun run --hot relay.ts  (auto-reload)
```
Relay listens on `http://127.0.0.1:18720`. Optional env:
`RELAY_PORT`, `ZO_API_BASE` (default `https://api.zo.computer`).

### 3. Connect to Zo (get a key)
Zo has **no token-generation API** — keys are created in the UI and shown once.
Two ways to connect:

- **Log in to Zo (recommended):** click **Log in to Zo** in the sidebar. It opens
  `zo.computer/?t=settings&s=advanced` (Access Tokens). After you log in and
  click **Create**, the `zo_sk_…` token appears on the page and the
  `token-capture.js` content script reads it automatically and stores it. The
  sidebar switches to "✓ Connected to Zo".
- **Paste token (fallback):** click **Paste token**, paste a `zo_sk_…` key you
  created manually at Settings → Advanced → Access Tokens.

The token is stored in `chrome.storage.local` and sent per-request as the
`X-Zo-Token` header; the relay forwards it to Zo as `Authorization: Bearer`.
(You can also skip the extension token entirely and set `ZO_API_KEY` as an env
var on the relay — then the relay uses it as a fallback.)

## Browser control (optional)
Enable **Enable browser control** in the sidebar settings. When on, the relay's
`/zo/ask` call passes `include_context_link: true` and the system prompt tells Zo
it can emit `browser` JSON actions. The extension executes them on the **active
tab** via its content script.

Supported actions: `navigate`, `click`, `fill`, `read`, `extract`, `scroll`,
`screenshot`, `execute_js`, `page_info`.

The action format (fenced ```browser ... ``` block):
```json
{ "action": "click", "selector": "button#submit" }
```

## Notes
- Keep the relay running while using the sidebar (it's a local process on your machine).
- The token never leaves your machine except in the HTTPS request to Zo.
- Works on `http://127.0.0.1` / `http://localhost` from the extension by design.
