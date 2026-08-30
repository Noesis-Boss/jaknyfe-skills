#!/usr/bin/env bash
# skillspector-run.sh — pre-install security gate wrapper for NVIDIA SkillSpector
# Usage:
#   skillspector-run.sh <path-or-url> [--llm] [--json]
# Exit codes: 0 = LOW/SAFE, 1 = MEDIUM/CAUTION (allowed with warning), 2 = HIGH/CRITICAL (blocked), 3 = tool error
set -u
INPUT="${1:-}"
[ -z "$INPUT" ] && { echo "Usage: skillspector-run.sh <path-or-url> [--llm] [--json]" >&2; exit 3; }

SKILLSPECTOR_BIN="${SKILLSPECTOR_BIN:-/root/.local/bin/skillspector}"
[ -x "$SKILLSPECTOR_BIN" ] || SKILLSPECTOR_BIN="$(command -v skillspector || true)"
[ -n "$SKILLSPECTOR_BIN" ] || { echo "ERROR: skillspector CLI not found. Run: uv tool install git+https://github.com/NVIDIA/skillspector.git" >&2; exit 3; }

EXTRA=("--no-llm")
OUTFMT=json
for a in "${@:2}"; do
  case "$a" in
    --llm)  EXTRA=() ;;
    --json) OUTFMT=json ;;
  esac
done

REPORT="$(mktemp /tmp/skillspector-scan-XXXX.json)"
"$SKILLSPECTOR_BIN" scan "$INPUT" --format json --output "$REPORT" "${EXTRA[@]}" >/dev/null 2>&1
RC=$?
[ $RC -ne 0 ] && [ ! -s "$REPORT" ] && { echo "ERROR: skillspector scan failed (rc=$RC)" >&2; rm -f "$REPORT"; exit 3; }

python3 - "$REPORT" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
ra = d.get("risk_assessment", {})
skills = d.get("skills") or [{"skill": d.get("skill", {}), "risk_assessment": ra, "issues": d.get("issues", [])}]
worst = 0
sev_rank = {"INFO":0,"LOW":1,"MEDIUM":2,"HIGH":3,"CRITICAL":4}
worst_band = "LOW"
for s in skills:
    r = s.get("risk_assessment", {})
    sc = r.get("score") or 0
    worst = max(worst, sc)
    band = (r.get("severity") or "LOW").upper()
    if sev_rank.get(band,0) > sev_rank.get(worst_band,0):
        worst_band = band
    name = (s.get("skill") or {}).get("name", "?")
    rec = r.get("recommendation", "?")
    print(f"[skillspector] {name}: score={sc} severity={band} recommendation={rec}")
    for f in (s.get("issues") or [])[:5]:
        if (f.get("severity") or "").upper() in ("HIGH","CRITICAL"):
            loc = (f.get("location") or {}).get("file","?")
            print(f"  !! {f['severity']} {f.get('category','?')} @ {loc}: {(f.get('explanation') or '')[:100]}")
print(f"[skillspector] overall: score={worst} band={worst_band}")
if worst_band in ("HIGH","CRITICAL"): sys.exit(2)
if worst_band == "MEDIUM": sys.exit(1)
sys.exit(0)
PY
VERDICT=$?
[ "${KEEP_REPORT:-0}" = "1" ] && echo "[skillspector] report: $REPORT" >&2 || rm -f "$REPORT"
exit $VERDICT
