#!/bin/bash
# Nightly Minecraft world backup loop: run backup at start, then every 24h.
# Matches the snapshot-loop pattern. Managed service: minecraft-world-backup
BACKUP=/home/workspace/bin/mc-world-backup.sh
LOG=/var/log/minecraft-backup-loop.log

while true; do
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') loop: starting backup" >>"$LOG"
  "$BACKUP" >>"$LOG" 2>&1
  sleep 86400
done
