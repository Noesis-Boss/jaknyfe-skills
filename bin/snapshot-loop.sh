#!/bin/bash
# Nightly snapshot loop: runs bin/snapshot-workspace.sh daily, logs to /var/log/workspace-snapshot.log
set -u
LOG=/var/log/workspace-snapshot.log
while true; do
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') snapshot run begin" >> "$LOG"
  /home/workspace/bin/snapshot-workspace.sh >> "$LOG" 2>&1
  sleep 86400
done
