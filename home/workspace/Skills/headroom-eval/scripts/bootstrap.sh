#!/usr/bin/env bash
# One-shot bootstrap: creates a venv, installs deps, starts the headroom proxy
# in the background, and writes a sanity-check.
#
# Re-runnable. Safe to run on a fresh sandbox.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$REPO_ROOT/.venv"

if [ ! -d "$VENV" ]; then
  python3 -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"
pip install -q --upgrade pip
pip install -q -r "$REPO_ROOT/scripts/requirements.txt"

# Headroom proxy (only if you want the headroom arm in the run)
if command -v headroom >/dev/null 2>&1; then
  if ! curl -fsS http://localhost:8787/health >/dev/null 2>&1; then
    echo "[bootstrap] starting headroom proxy on :8787"
    nohup headroom serve --port 8787 > "$REPO_ROOT/headroom.log" 2>&1 &
    sleep 2
    if curl -fsS http://localhost:8787/health >/dev/null 2>&1; then
      echo "[bootstrap] headroom proxy up"
    else
      echo "[bootstrap] WARN: headroom proxy did not respond; control-only run will still work" >&2
    fi
  else
    echo "[bootstrap] headroom proxy already running"
  fi
else
  echo "[bootstrap] 'headroom' CLI not on PATH; control-only runs will still work" >&2
fi

echo "[bootstrap] ready. try: python3 $REPO_ROOT/scripts/run_ab.py --input $REPO_ROOT/sample-input/sample.json --arms control"
