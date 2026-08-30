# Tuskcentral.ai API surface (captured 2026-07-03)

Reverse-engineered from the live Angular SPA. No public docs. These endpoints are
internal; the wrapper prefers driving the real interface with Playwright, but the
endpoints are listed here for reference and for any future raw-HTTP path.

## Base

- Origin: `https://tuskcentral.ai`
- Auth: Clerk (cookie-based). Sign-in surface is at `https://clerk.tuskcentral.ai/`
  loaded as `clerk.browser.js` v5. The browser wrapper reuses the live Clerk
  session from the persistent Chromium profile.

## Endpoints

### `GET /api/v2/chat/providers` — public, no auth

Returns the full model catalog. Cached and re-fetched at app boot.

```jsonc
{
  "providers": [
    {
      "label": "Gemini 3.1 Pro Preview",
      "key": "053a0ffe-1c18-4205-af59-c8f7a64dc492",   // aiModelId
      "displayName": "Gemini 3.1Pro",
      "providerName": "Google",
      "description": "...",
      "isPremium": true,
      "createdDate": 1771509627,
      "addedDate": "2026-03-19T00:00:00Z",
      "hasWebSearch": true,
      "hasReasoning": true,
      "inputModalities": ["audio","file","image","text","video"],
      "outputModalities": ["text"],
      "logoUrl": "assets/ai-providers/google.svg",
      "options": [
        { "key": "sprint",  "label": "Fast (free)" },
        { "key": "marathon","label": "Thinking (credits)" }
      ],
      "tones": [
        { "key": "technical", "label": "Technical", "description": "..." },
        { "key": "creative",  "label": "Creative",  "description": "..." },
        { "key": "work",      "label": "Work",      "description": "..." },
        { "key": "learn",     "label": "Learn",     "description": "..." },
        { "key": "casual",    "label": "Casual",    "description": "..." }
      ]
    }
  ]
}
```

Field meanings:
- `key` — model UUID used in every chat request as `aiModelId`
- `isPremium: true` — requires Tusk credits; `sprint` is free `marathon` is paid
- `isPremium: false` — both options are free (if `marathon` exists)
- `tones[].key` — one of `technical|creative|work|learn|casual`; free models usually expose all five

### `POST /api/V2/Chat` — auth required

Request body (typical):
```json
{
  "chatId":          "019f28c7-5894-7ff1-b6f1-fce89ae729c1",  // UUID; null for first message
  "parentChatLogId": null,                                   // for threaded follow-ups
  "text":            "your prompt here",
  "aiModelId":       "053a0ffe-1c18-4205-af59-c8f7a64dc492",
  "optionKey":       "sprint",      // sprint | marathon
  "toneKey":         "technical",   // optional
  "hasWebSearch":    true,
  "hasReasoning":    true,
  "isTemporaryChat": false,
  "aiModelType":     0              // 0 = chat (other enum values not yet observed)
}
```

Response: JSON object, not SSE. Single response per request (the SPA uses
`requestAnimationFrame` to repaint, not server streaming). Sample:

```json
{
  "chatId":     "019f28c7-5894-7ff1-b6f1-fce89ae729c1",
  "sessionId":  "5b7c1c79-...",
  "chatLogId":  "ce98f3e2-...",
  "role":       "assistant",
  "content":    "{\"content\":\"<p>Hello</p>\",\"isComplete\":true}"
}
```

The outer `content` is a JSON-stringified object. Parse it once, then `content`
inside is an HTML string (uses Bootstrap classes, `<p>`, `<ul>`, `<pre><code>`,
`<table>`, etc.). The wrapper strips the wrapper JSON and decodes the HTML to
plain text + code blocks.

Status codes observed:
- `200` with sign-up wall content when unauthenticated
- `200` with credit-required content when model needs paid credits and account is empty
- `200` with full reply when authenticated and authorized
- `4xx` on bad model id, malformed body, etc.

### `GET /api/v2/chat/{chatId}` — auth required

Loads a prior conversation by chatId. Used by the SPA when you navigate to
`/chat/{chatId}`. Not needed by the wrapper — it always starts a new chat or
forwards the `chatId` it got from the previous request.

## WebView mode

The SPA supports `?tusk_webview=1` (sets a `tusk-webview` class on `<html>` and
`window.__TUSK_WEBVIEW__ = true`) for React Native in-app embedding. The wrapper
uses this so the interface renders at a known viewport without mobile CSS hacks.

## 30 models (snapshot, 2026-07-03)

Free:
- Kimi K2.5, Llama 4 Maverick, GPT-5.4 Nano, GPT-5.4 Mini, GPT-4o-mini (2024-07-18),
  DeepSeek V3.2, MiniMax M2.7, Mistral Small 3.2 24B, Command R7B (12-2024), GPT-5 Nano,
  gpt-oss-120b, Mistral Small 4, Kimi K2 Thinking, Kimi K2.6, Claude Haiku 4.5,
  DeepSeek V4 Pro, Sonar, Gemini 3.1 Flash Lite, MiniMax M2-her, gpt-oss-20b,
  Grok 4.3, Brainiac (OpenRouter), Llama 4 Scout

Premium (require credits):
- Gemini 3.1 Pro Preview, Sonar Deep Research, Sonar Pro, Claude Sonnet 4.6,
  Gemini 3.5 Flash, GPT-5.4, GPT-5.5
