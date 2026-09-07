#!/bin/bash
# Nightly snapshot of high-value workspace paths to Archive/snapshots/
# Retains the last 14 snapshots. Logs to /var/log/workspace-snapshot.log
set -u

SRC=/home/workspace
SNAP_DIR="$SRC/Archive/snapshots"
LOG=/var/log/workspace-snapshot.log
KEEP=14
PATHS="Skills bin memory AGENTS.md MEMORY.md USER.md"
STAMP=$(date -u +%Y%m%d-%H%M%S)

mkdir -p "$SNAP_DIR"

# Only include paths that currently exist
EXISTING=""
for p in $PATHS; do
  [ -e "$SRC/$p" ] && EXISTING="$EXISTING $p"
done

cd "$SRC"
TARBALL="$SNAP_DIR/workspace-snapshot-$STAMP.tar.gz"
if tar czf "$TARBALL" \
     --exclude='node_modules' \
     --exclude='.git' \
     --exclude='__pycache__' \
     $EXISTING 2>>"$LOG"; then
  SIZE=$(du -h "$TARBALL" | cut -f1)
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') OK $TARBALL ($SIZE) paths:$EXISTING"
else
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') FAILED creating $TARBALL"
  rm -f "$TARBALL"
  exit 1
fi

# Retention: keep newest $KEEP snapshots
ls -1t "$SNAP_DIR"/workspace-snapshot-*.tar.gz 2>/dev/null | tail -n +$((KEEP + 1)) | while read -r old; do
  rm -f "$old"
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') pruned $old"
done
