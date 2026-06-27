#!/usr/bin/env bash
# Deploy Scottish Rite site to noesisgroup.com/scottish_rite/
# Usage:
#   ./deploy_noesisgroup.sh fetch    — download current HTML from server
#   ./deploy_noesisgroup.sh upload   — upload local HTML to server
#   ./deploy_noesisgroup.sh verify   — check live site for key content

set -e

NG_USER="noesisuser"
NG_HOST="65.38.97.58"
NG_PATH="/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html"
LOCAL_HTML="/tmp/noesisgroup-scottish-rite.html"
LIVE_URL="https://noesisgroup.com/scottish_rite/"

case "${1:-}" in
  fetch)
    echo "Fetching current HTML from noesisgroup.com..."
    sshpass -p '@EUjgrN9fkr5li8$' scp -o StrictHostKeyChecking=no \
      ${NG_USER}@${NG_HOST}:${NG_PATH} \
      ${LOCAL_HTML}
    echo "Saved to ${LOCAL_HTML}"
    ;;
  upload)
    if [ ! -f "${LOCAL_HTML}" ]; then
      echo "Error: ${LOCAL_HTML} not found. Run 'fetch' first." >&2
      exit 1
    fi
    echo "Uploading to noesisgroup.com..."
    sshpass -p '@EUjgrN9fkr5li8$' scp -o StrictHostKeyChecking=no \
      ${LOCAL_HTML} \
      ${NG_USER}@${NG_HOST}:${NG_PATH}
    echo "✅ Uploaded to ${NG_PATH}"
    ;;
  verify)
    echo "Verifying live site..."
    curl -sL "${LIVE_URL}" | grep -oP '.{0,30}Randy Jager.{0,30}' | head -1
    curl -sL "${LIVE_URL}" | grep -oP '.{0,30}Donald E\. Lowery.{0,30}' | head -1
    echo "✅ Verification complete"
    ;;
  *)
    echo "Usage: $0 {fetch|upload|verify}"
    exit 1
    ;;
esac
