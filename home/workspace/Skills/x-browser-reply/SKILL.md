---
name: x-browser-reply
description: Reply to X/Twitter tweets via Playwright headless browser to bypass API reply restrictions. Use when the user needs to reply to tweets where they aren't the author or mentioned, which X's API blocks with 403.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# X Browser Reply

Bypasses X API reply restrictions by automating a real Chromium browser session with Playwright.

## When to Use

- X API returns `403 Forbidden: You can only reply to posts where you are mentioned or are the author`
- User wants to reply to public tweets they don't own
- X login is broken in Zo's built-in browser but Playwright works with cookies

## Prerequisites

1. **Playwright** — installed system-wide (`pip install playwright && playwright install chromium`)
2. **X cookies** — exported from a logged-in browser session as JSON

## Getting X Cookies

1. Log into X in a regular browser (Chrome/Firefox)
2. Install a cookie exporter extension (e.g., "EditThisCookie", "Get cookies.txt LOCALLY")
3. Export cookies for `x.com` as JSON
4. Save to `/home/workspace/.secrets/x-cookies.json` or pass path via `--cookies`

## Usage

```bash
# Reply to a tweet by ID
python3 /home/workspace/Skills/x-browser-reply/scripts/reply.py \
  --tweet-id 2091461809807179856 \
  --text "I completely agree" \
  --cookies /home/workspace/.secrets/x-cookies.json

# Reply using full URL
python3 /home/workspace/Skills/x-browser-reply/scripts/reply.py \
  --url "https://x.com/codewithimanshu/status/2091461809807179856" \
  --text "Great point!" \
  --cookies /home/workspace/.secrets/x-cookies.json
```

## How It Works

1. Launches headless Chromium via Playwright with system Chrome binary
2. Injects X session cookies to authenticate
3. Navigates to the target tweet URL
4. Clicks the reply button (data-testid="reply")
5. Types reply text in the composer with human-like delay
6. Clicks the submit button
7. Verifies success via URL change

## Limitations

- **Cookies expire** — X sessions don't last forever; re-export when login fails
- **Rate limiting** — rapid replies may trigger X's anti-spam; add delays between replies
- **Headless detection** — X may show CAPTCHA for headless browsers; use `--headless false` if needed
- **Zo's broken login** — Zo's built-in browser can't log into X, so we bypass it entirely with Playwright + exported cookies

## Troubleshooting

| Error | Fix |
|---|---|
| `Not logged in` | Re-export X cookies |
| `Could not find reply button` | Page didn't load; try `--headless false` to see what's happening |
| `Could not submit` | May be rate limited; wait and retry |
| CAPTCHA | Use `--headless false` and solve manually, or wait for cooldown |
