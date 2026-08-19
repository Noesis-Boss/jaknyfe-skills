# SaaS-Mailer

SaaS-Mailer is a standalone multi-tenant outbound-email workspace. The MVP vertical slice covers tenant-scoped contacts, sending-account records, campaigns, approval, queue eligibility, mock delivery, idempotency, retries, suppression, and event history.

## Run

```bash
bun test
bun run src/server.ts
```

The default development dashboard is available at `/`. The current MVP uses a deterministic mock sending adapter. Provider credentials are encrypted server-side; real Gmail, Outlook, and SMTP adapters are later work.

## MVP boundaries

Authentication and organization membership are still provisional at the HTTP boundary. Requests currently provide `x-organization-id`; production authentication must replace that header before public launch. No real outbound email is sent by the mock adapter.
