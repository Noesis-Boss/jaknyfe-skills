#!/usr/bin/env bash
set -uo pipefail

cluster_data=/var/lib/postgresql/15/main
runtime_dir=/var/run/postgresql
failure_threshold=3

probe() {
  pg_isready -q -h 127.0.0.1 -p 5432 || return 1
  local result
  result=$(runuser -u postgres -- psql -X -v ON_ERROR_STOP=1 -Atqc 'SELECT 1' -d postgres 2>/dev/null) || return 1
  [[ "$result" == "1" ]]
}

remove_stale_runtime_files() {
  if pgrep -x postgres >/dev/null 2>&1; then
    return 1
  fi

  local pid
  for file in "$cluster_data/postmaster.pid" "$runtime_dir/15-main.pid" "$runtime_dir/.s.PGSQL.5432.lock"; do
    if [[ -f "$file" ]]; then
      pid=$(head -n 1 "$file")
      if [[ ! "$pid" =~ ^[0-9]+$ ]] || kill -0 "$pid" 2>/dev/null; then
        return 1
      fi
      rm -f "$file"
    fi
  done
  rm -f "$runtime_dir/.s.PGSQL.5432"
}

recover() {
  if pgrep -x postgres >/dev/null 2>&1; then
    pg_ctlcluster 15 main restart
  else
    remove_stale_runtime_files || return 1
    pg_ctlcluster 15 main start
  fi
}

log() {
  printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*"
}

if [[ "${1:-}" == "--check" ]]; then
  if probe; then
    echo 'PostgreSQL readiness and SELECT 1 passed.'
  else
    echo 'PostgreSQL readiness or SELECT 1 failed.' >&2
    exit 1
  fi
  exit 0
fi

failures=0
while true; do
  if probe; then
    if (( failures > 0 )); then
      log 'PostgreSQL probe recovered.'
    fi
    failures=0
  else
    failures=$((failures + 1))
    log "PostgreSQL probe failed (${failures}/${failure_threshold})."
    if (( failures >= failure_threshold )); then
      log 'Attempting PostgreSQL recovery.'
      if recover; then
        sleep 5
        if probe; then
          log 'PostgreSQL recovery succeeded.'
        else
          log 'PostgreSQL remains unhealthy after recovery attempt.'
        fi
      else
        log 'PostgreSQL recovery command failed.'
      fi
      failures=0
      sleep 30
    fi
  fi
  sleep 10
done
