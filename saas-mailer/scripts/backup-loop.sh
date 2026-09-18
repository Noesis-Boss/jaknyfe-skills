#!/usr/bin/env bash
set -euo pipefail

log_file="${BACKUP_LOG:-/var/log/saas-mailer-backup.log}"
while true; do
  printf '%s backup begin\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" >> "$log_file"
  bun run backup:postgres >> "$log_file" 2>&1 || printf '%s backup failed\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" >> "$log_file"
  sleep 86400
done
