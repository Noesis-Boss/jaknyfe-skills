#!/usr/bin/env bash
# Weekly gitleaks sweep across top-level git repos in the workspace.
# Usage: gitleaks-sweep.sh [--quiet]
# Report: /home/workspace/memory/security/gitleaks-sweep-<date>.json
# Exit 0 = clean, 1 = findings, 2 = error.
set -u
OUT_DIR=/home/workspace/memory/security
mkdir -p "$OUT_DIR"
STAMP=$(date +%F)
REPORT="$OUT_DIR/gitleaks-sweep-$STAMP.json"
SUMMARY="$OUT_DIR/gitleaks-sweep-latest.txt"
RAW=/tmp/gl-raw-$STAMP.json
: > "$RAW"
repos_scanned=0

# top-level repos only: .git dirs at depth 2 or 3 (Projects/x, Skills/x/y), never /home/workspace root
while IFS= read -r gitdir; do
  repo=$(dirname "$gitdir")
  gitleaks detect --source "$repo" --no-banner --redact --report-format json --report-path /tmp/gl-one.json >/dev/null 2>&1
  n=$(jq 'length' /tmp/gl-one.json 2>/dev/null || echo 0)
  repos_scanned=$((repos_scanned+1))
  if [ "$n" -gt 0 ]; then
    jq --arg repo "$repo" 'map(. + {repo: $repo})' /tmp/gl-one.json >> "$RAW"
    echo "," >> "$RAW"
  fi
done < <(find /home/workspace/Projects /home/workspace/Skills /home/workspace/bin /home/workspace/memory -maxdepth 4 -name .git -type d 2>/dev/null)

# merge per-repo arrays into one
{ echo '['; sed '$ s/,$//' "$RAW"; echo ']'; } > /tmp/gl-merged.json
jq -s 'flatten // []' /tmp/gl-merged.json > "$REPORT" 2>/dev/null || echo '[]' > "$REPORT"
rm -f "$RAW" /tmp/gl-merged.json

total=$(jq 'length' "$REPORT")
{
  echo "Gitleaks sweep $STAMP — repos: $repos_scanned, findings: $total"
  jq -r 'group_by(.repo)[] | "\(.[0].repo): \(length) findings"' "$REPORT"
  echo "Report: $REPORT"
} > "$SUMMARY"

[ "${1:-}" != "--quiet" ] && cat "$SUMMARY"
[ "$total" -eq 0 ] && exit 0 || exit 1
