# SaaS-Mailer

SaaS-Mailer is a standalone multi-tenant outbound-email workspace. The MVP vertical slice covers tenant-scoped contacts, sending-account records, campaigns, approval, queue eligibility, mock delivery, idempotency, retries, suppression, and event history.

## Run

```bash
bun test
bun run src/server.ts
```

The default development dashboard is available at `/`. The current MVP uses a deterministic mock sending adapter. Provider credentials are encrypted server-side; real Gmail, Outlook, and SMTP adapters are later work.

## Configuration

Local development defaults to `APP_ENV=development` and the deterministic mock adapter. Copy `.env.example` to `.env` only when local overrides are needed. Production requires `DATABASE_URL`, `SESSION_SECRET`, `CREDENTIAL_ENCRYPTION_KEY` (a hex or base64 value encoding 32 bytes), and `OAUTH_CALLBACK_ORIGIN`; provider OAuth credentials and worker limits are parsed by `loadConfig()` at startup. Configuration errors identify variable names only and never secret values.

## MVP boundaries

Authentication now uses password-backed users, membership-aware organization sessions, and an HttpOnly session cookie. The `x-organization-id` header is ignored for tenant selection. No real outbound email is sent by the mock adapter.
