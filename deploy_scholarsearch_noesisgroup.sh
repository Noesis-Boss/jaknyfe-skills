#!/usr/bin/env bash
# Deploy ScholarSearch site to noesisgroup.com/scholarsearch/
# Usage:
#   ./deploy_scholarsearch_noesisgroup.sh deploy  — build and upload
#   ./deploy_scholarsearch_noesisgroup.sh verify  — check live site

set -e

NG_USER="noesisuser"
NG_HOST="65.38.97.58"
NG_PASS='@EUjgrN9fkr5li8$'
NG_PATH="/var/www/vhosts/noesisgroup.com/httpdocs/scholarsearch"
LOCAL_DIST="/home/workspace/scholarsearch-site/dist"
LIVE_URL="https://noesisgroup.com/scholarsearch/"
API_PHP="/home/workspace/scholarsearch-site/api.php"
DB="/home/workspace/scholarsearch/data/processed/scholarships.db"

deploy() {
  echo "Building..."
  cd /home/workspace/scholarsearch-site
  bun run build

  echo "Uploading dist files..."
  sshpass -p "$NG_PASS" rsync -avz \
    -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    $LOCAL_DIST/ ${NG_USER}@${NG_HOST}:${NG_PATH}/

  echo "Uploading api.php..."
  sshpass -p "$NG_PASS" rsync -avz \
    -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    $API_PHP ${NG_USER}@${NG_HOST}:${NG_PATH}/api.php

  echo "Uploading database..."
  sshpass -p "$NG_PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    ${NG_USER}@${NG_HOST} "mkdir -p ${NG_PATH}/data"
  sshpass -p "$NG_PASS" rsync -avz \
    -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    $DB ${NG_USER}@${NG_HOST}:${NG_PATH}/data/scholarships.db

  echo "✅ Deployed to ${LIVE_URL}"
}

verify() {
  echo "Verifying live site..."
  curl -sL "${LIVE_URL}api.php/api/stats" | head -c 200
  echo ""
  echo "✅ Verification complete"
}

case "${1:-}" in
  deploy)
    deploy
    ;;
  verify)
    verify
    ;;
  *)
    echo "Usage: $0 {deploy|verify}"
    exit 1
    ;;
esac
