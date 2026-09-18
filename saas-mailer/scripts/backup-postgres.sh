#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${DATABASE_URL:-}" ]]; then
  printf '%s\n' "DATABASE_URL is required" >&2
  exit 1
fi

backup_dir="${BACKUP_DIR:-backups}"
retention_days="${BACKUP_RETENTION_DAYS:-14}"
mkdir -p "$backup_dir"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
output="$backup_dir/saas-mailer-$timestamp.dump"
temporary_output="$output.tmp"

pg_dump_command="${PG_DUMP_BIN:-$(command -v pg_dump)}"
if [[ -x /usr/lib/postgresql/18/bin/pg_dump ]]; then
  pg_dump_command="${PG_DUMP_BIN:-/usr/lib/postgresql/18/bin/pg_dump}"
fi

rm -f "$temporary_output"
trap 'rm -f "$temporary_output"' EXIT
"$pg_dump_command" --format=custom --file="$temporary_output" "$DATABASE_URL"
if [[ ! -s "$temporary_output" ]]; then
  printf 'Backup failed: dump is empty\n' >&2
  exit 1
fi
mv -f "$temporary_output" "$output"
find "$backup_dir" -maxdepth 1 -type f -name 'saas-mailer-*.dump' -mtime "+$retention_days" -delete
printf 'Created %s\n' "$output"
