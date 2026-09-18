# SaaS-Mailer

SaaS-Mailer is a standalone multi-tenant outbound-email workspace. The MVP vertical slice covers tenant-scoped contacts, sending-account records, campaigns, approval, queue eligibility, mock delivery, idempotency, retries, suppression, and event history.

## Run

```bash
bun test
bun run src/server.ts
```

The default development dashboard is available at `/`. Development and tests use a deterministic mock adapter. Production uses Gmail or Microsoft OAuth adapters with encrypted credentials and refresh-before-expiry.

## Hosted PostgreSQL

PostgreSQL mode is selected when `DATABASE_URL` is set. Production additionally requires `APP_ENV=production` and the other production secrets. `openProductionDatabase()` creates a Bun PostgreSQL pool and runs the idempotent startup migration in `db/migrations/postgres/001_initial.sql` inside a transaction. SQLite remains the fallback when no database URL is configured. The HTTP server and durable worker use the same PostgreSQL queue and send processor.

Operational commands:

```bash
APP_ENV=production DATABASE_URL="$DATABASE_URL" bun run src/server.ts
pg_dump --format=custom --file=saas-mailer.dump "$DATABASE_URL"
pg_restore --clean --if-exists --dbname="$DATABASE_URL" saas-mailer.dump
```

For a timestamped local backup, run `DATABASE_URL=... bun run backup:postgres`. Set `BACKUP_DIR` to change the output directory and `BACKUP_RETENTION_DAYS` to change the default 14-day retention. The command writes custom-format dumps and never prints the connection string. The managed `saas-mailer-backup` process runs this command every 24 hours.

Validate a dump without changing any database with `bun run validate:backup -- backups/saas-mailer-YYYYMMDDTHHMMSSZ.dump`. To validate loading into an already-created disposable database, add its name as the second argument; the check filters only PostgreSQL 18 metadata unsupported by the local PostgreSQL 15 server.

The managed `saas-mailer-restore-validation` process runs the disposable restore check every 24 hours and removes its temporary database after each run. It uses the configured `DATABASE_URL` for database creation and restore connections.
Validation failures are emailed to `RESTORE_VALIDATION_ALERT_TO` (default `delowery@gmail.com`); set `RESTORE_VALIDATION_ALERT_FROM` to change the sender address. Repeated identical failures are deduplicated until a validation succeeds; set `RESTORE_VALIDATION_ALERT_STATE` to relocate the state file.

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

Local development defaults to `APP_ENV=development` with PostgreSQL when `DATABASE_URL` is set; `.env.example` contains the shared local database URL. Without it, development uses the deterministic mock adapter with SQLite. Production requires `DATABASE_URL`, `SESSION_SECRET`, `CREDENTIAL_ENCRYPTION_KEY` (a hex or base64 value encoding 32 bytes), `RESEND_API_KEY`, and `OAUTH_CALLBACK_ORIGIN`; provider OAuth credentials and worker limits are parsed by `loadConfig()` at startup. Resend sending accounts use the verified `mailer@noesisgroup.com` identity and store no provider secret per account. Configuration errors identify variable names only and never secret values.

## MVP boundaries

Authentication now uses password-backed users, membership-aware organization sessions, and an HttpOnly session cookie. The `x-organization-id` header is ignored for tenant selection. Gmail and Microsoft OAuth accounts send through their provider APIs; the mock adapter is used only in development and tests.
