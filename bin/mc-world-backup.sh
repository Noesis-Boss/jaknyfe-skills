#!/bin/bash
# Safe nightly backup of Minecraft world data to Archive/minecraft-backups/
# Flushes via RCON first, then tars world dirs. Retains last 14. Logs to /var/log/minecraft-backup.log
set -u

MC=/home/workspace/Projects/minecraft-server
DEST=/home/workspace/Archive/minecraft-backups
LOG=/var/log/minecraft-backup.log
KEEP=14
STAMP=$(date -u +%Y%m%d-%H%M%S)

mkdir -p "$DEST"

# Flush world to disk if server is running (password from /root/.zo_secrets)
if [ -f /root/.zo_secrets ]; then
  . /root/.zo_secrets
  export MINECRAFT_RCON_PASSWORD
fi
if pgrep -f "paper.jar" >/dev/null 2>&1; then
  (cd "$MC" && timeout 20 python3 rcon.py "save-all flush" >>"$LOG" 2>&1)
  sleep 5
fi

TARBALL="$DEST/mc-world-$STAMP.tar.gz"
cd "$MC"
WORLDS=""
for w in world world_nether world_the_end; do
  [ -d "$w" ] && WORLDS="$WORLDS $w"
done
if tar czf "$TARBALL" $WORLDS 2>>"$LOG"; then
  SIZE=$(du -h "$TARBALL" | cut -f1)
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') OK $TARBALL ($SIZE) worlds:$WORLDS"
else
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') FAILED creating $TARBALL"
  rm -f "$TARBALL"
  exit 1
fi

ls -1t "$DEST"/mc-world-*.tar.gz 2>/dev/null | tail -n +$((KEEP + 1)) | while read -r old; do
  rm -f "$old"
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') pruned $old"
done
