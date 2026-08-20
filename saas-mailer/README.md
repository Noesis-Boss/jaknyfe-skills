# SaaS-Mailer

SaaS-Mailer is a standalone multi-tenant outbound-email workspace. The MVP vertical slice covers tenant-scoped contacts, sending-account records, campaigns, approval, queue eligibility, mock delivery, idempotency, retries, suppression, and event history.

## Run

```bash
bun test
bun run src/server.ts
```

The default development dashboard is available at `/`. Development and tests use a deterministic mock adapter. Production uses Gmail or Microsoft OAuth adapters with encrypted credentials and refresh-before-expiry.

## Hosted PostgreSQL

Hosted mode is selected with `APP_ENV=production` and requires `DATABASE_URL`. `openProductionDatabase()` creates a Bun PostgreSQL pool and runs the idempotent startup migration in `db/migrations/postgres/001_initial.sql` inside a transaction. Development and tests continue to use the explicit SQLite adapter from `openDatabase()`. The HTTP server opens PostgreSQL before accepting production traffic, and the durable worker uses the same PostgreSQL queue and send processor.

Operational commands:

```bash
APP_ENV=production DATABASE_URL="$DATABASE_URL" bun run src/server.ts
pg_dump --format=custom --file=saas-mailer.dump "$DATABASE_URL"
pg_restore --clean --if-exists --dbname="$DATABASE_URL" saas-mailer.dump
```

Use a pool-sized PostgreSQL connection string supplied by the hosting provider. Take a backup before migrations; startup migration failure rolls back the transaction and prevents a partially applied schema.

## PostgreSQL production persistence

Production uses `DATABASE_URL` and the PostgreSQL migration at `db/migrations/postgres/001_initial.sql`. The migration is idempotent and records its version in `schema_migrations`; startup runs it inside a transaction before the application accepts traffic. Local development and tests intentionally continue to use the explicit SQLite adapter.

Operational examples:

```bash
psql "$DATABASE_URL" -f db/migrations/postgres/001_initial.sql
pg_dump --format=custom --file=saas-mailer.dump "$DATABASE_URL"
pg_restore --clean --if-exists --dbname="$DATABASE_URL" saas-mailer.dump
```

The PostgreSQL adapter uses Bun's pooled `SQL` client. Keep pool sizing in the database provider's connection-pooler configuration; do not put credentials in logs or source files. `openProductionDatabase()` runs the migration transactionally and `repositories({ database, organizationId })` provides organization-scoped access with composite tenant foreign keys and idempotent message inserts.

## Configuration

Local development defaults to `APP_ENV=development` and the deterministic mock adapter. Copy `.env.example` to `.env` only when local overrides are needed. Production requires `DATABASE_URL`, `SESSION_SECRET`, `CREDENTIAL_ENCRYPTION_KEY` (a hex or base64 value encoding 32 bytes), and `OAUTH_CALLBACK_ORIGIN`; provider OAuth credentials and worker limits are parsed by `loadConfig()` at startup. Configuration errors identify variable names only and never secret values.

## MVP boundaries

Authentication now uses password-backed users, membership-aware organization sessions, and an HttpOnly session cookie. The `x-organization-id` header is ignored for tenant selection. Gmail and Microsoft OAuth accounts send through their provider APIs; the mock adapter is used only in development and tests.
