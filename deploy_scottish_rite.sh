#!/usr/bin/env bash
# Deploy Scottish Rite website to both hosting targets:
#   1. zo computer (scottish-rite-jaknyfe.zocomputer.io) — Vite-built SPA
#   2. noesisgroup.com/scottish_rite — single-file React 18 + Babel standalone

set -e

# ── 1. ZO COMPUTER (Vite build) ──────────────────────────────────────────────

cd /home/workspace/scottish-rite-kst-andrew

# Clean build
rm -rf dist
bun run build

# Copy to scottish-rite-site (served by zo computer via routes.json)
cp dist/index.html dist/assets/* /home/workspace/scottish-rite-site/

# Commit and push (zo computer pulls from git)
cd /home/workspace/scottish-rite-site
git add .
git commit -m "Update Scottish Rite site $(date +%Y-%m-%d)"
git push origin master

echo "✅ zo computer deployment done"

# ── 2. NOESISGROUP.COM (single HTML file) ────────────────────────────────────

# The noesisgroup version is a single HTML file with inline React 18 + Babel.
# It is NOT built by Vite. The source of truth is the HTML file itself.
# To update: edit the HTML locally, then SCP it to the server.

NG_USER="noesisuser"
NG_HOST="65.38.97.58"
NG_PATH="/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html"
LOCAL_HTML="/tmp/noesisgroup-scottish-rite.html"

# Copy current HTML from server for local editing
sshpass -p '@EUjgrN9fkr5li8$' scp -o StrictHostKeyChecking=no \
  ${NG_USER}@${NG_HOST}:${NG_PATH} \
  ${LOCAL_HTML}

echo "ℹ️  noesisgroup.com HTML fetched to ${LOCAL_HTML}"
echo "ℹ️  Edit this file locally, then run the upload command below:"
echo ""
echo "  sshpass -p '@EUjgrN9fkr5li8$' scp -o StrictHostKeyChecking=no \\\\"
echo "    ${LOCAL_HTML} ${NG_USER}@${NG_HOST}:${NG_PATH}"
echo ""
echo "✅ Deployment script complete"
