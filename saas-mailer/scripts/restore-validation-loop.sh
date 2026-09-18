#!/usr/bin/env bash
set -euo pipefail

log_file="${RESTORE_VALIDATION_LOG:-/var/log/saas-mailer-restore-validation.log}"
backup_dir="${BACKUP_DIR:-/home/workspace/saas-mailer/backups}"
interval="${RESTORE_VALIDATION_INTERVAL_SECONDS:-86400}"
alert_to="${RESTORE_VALIDATION_ALERT_TO:-delowery@gmail.com}"
alert_from="${RESTORE_VALIDATION_ALERT_FROM:-saas-mailer@localhost}"
alert_state_file="${RESTORE_VALIDATION_ALERT_STATE:-$backup_dir/.restore-validation-alert-state}"

clear_alert_state() {
  rm -f "$alert_state_file"
}

alert_failure() {
  local reason="$1"
  local subject="SaaS-Mailer restore validation failed"
  if [[ -f "$alert_state_file" ]] && [[ "$(cat "$alert_state_file")" == "$reason" ]]; then
    printf '%s restore alert suppressed: unchanged failure\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" >> "$log_file"
    return 0
  fi
  if ! printf 'Restore validation failed at %s UTC.\n\n%s\n\nLog: %s\n' \
    "$(date -u '+%Y-%m-%d %H:%M:%S')" "$reason" "$log_file" |
    mail -r "$alert_from" -s "$subject" "$alert_to" >> "$log_file" 2>&1; then
    printf '%s restore alert failed\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" >> "$log_file"
    return 0
  fi
  printf '%s' "$reason" > "$alert_state_file"
}

while true; do
  printf '%s restore validation begin\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" >> "$log_file"
  latest="$(find "$backup_dir" -maxdepth 1 -type f -name 'saas-mailer-*.dump' -size +0c -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -n1 | cut -d' ' -f2- || true)"
  if [[ -z "$latest" ]]; then
    reason="no non-empty backup found in $backup_dir"
    printf '%s restore validation failed: %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" "$reason" >> "$log_file"
    alert_failure "$reason"
  else
    disposable_db="saas_mailer_restore_$(date -u +%Y%m%d%H%M%S)_$$"
    admin_database="${DATABASE_URL%/*}/postgres"
    if psql --dbname="$admin_database" -v ON_ERROR_STOP=1 -c "CREATE DATABASE \"$disposable_db\"" >> "$log_file" 2>&1 && \
      bun run validate:backup -- "$latest" "$disposable_db" >> "$log_file" 2>&1; then
      printf '%s restore validation passed: %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" "$latest" >> "$log_file"
      clear_alert_state
    else
      reason="validation failed for $latest"
      printf '%s restore validation failed: %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" "$latest" >> "$log_file"
      alert_failure "$reason"
    fi
    psql --dbname="$admin_database" -v ON_ERROR_STOP=0 -c "DROP DATABASE IF EXISTS \"$disposable_db\"" >> "$log_file" 2>&1 || true
  fi
  sleep "$interval"
done
