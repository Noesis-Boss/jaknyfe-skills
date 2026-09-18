#!/usr/bin/env bash
set -euo pipefail

backup_file="${1:-}"
restore_db="${2:-}"
if [[ -z "$backup_file" || ! -f "$backup_file" ]]; then
  printf 'Usage: validate-backup.sh BACKUP_FILE [RESTORE_DATABASE]\n' >&2
  exit 2
fi

pg_restore_command="${PG_RESTORE_BIN:-$(command -v pg_restore)}"
if [[ -x /usr/lib/postgresql/18/bin/pg_restore ]]; then
  pg_restore_command="${PG_RESTORE_BIN:-/usr/lib/postgresql/18/bin/pg_restore}"
fi

"$pg_restore_command" --list "$backup_file" >/dev/null
printf 'Backup catalog valid: %s\n' "$backup_file"

if [[ -n "$restore_db" ]]; then
  restore_target="$restore_db"
  if [[ -n "${DATABASE_URL:-}" ]]; then
    restore_target="${DATABASE_URL%/*}/$restore_db"
  fi
  "$pg_restore_command" --no-owner --no-acl --no-comments --file=- "$backup_file" \
    | sed -e '/^SET transaction_timeout = 0;$/d' -e '/neon_superuser/d' \
    | psql -v ON_ERROR_STOP=1 --dbname="$restore_target" >/dev/null
  printf 'Backup restore valid: %s\n' "$restore_db"
fi
