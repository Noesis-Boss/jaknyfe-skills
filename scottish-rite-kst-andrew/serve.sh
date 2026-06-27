#!/bin/bash
set -e
cd /home/workspace/scottish-rite-kst-andrew
bun run build
cd dist
exec python3 -m http.server 51001 --bind 0.0.0.0
