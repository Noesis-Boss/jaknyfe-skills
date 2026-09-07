# Issue Log

## 2026-07-12 — Magic link endpoint 500

- **Problem**: `GET /api/auth/magic/verify` returned an Internal Server Error after clicking a magic link.
- **Root cause**: Chained `.header(...)` call on Hono's `Response` object in `server.ts`.
  - `c.redirect("/", 302).header("Set-Cookie", ...)` throws because `.header()` is not a function on `Response`.
  - Same bug existed in Google OAuth callback and logout handlers.
- **Fix applied**:
  - Replaced chained `.header(...)` with `res.headers.set(...)` after `c.redirect(...)`/`c.json(...)`.
  - Restarted the `weightloss-tracker` service to load new code.
- **Result**: Service now returns 200 on homepage and 302 on verify endpoint without crashing.
