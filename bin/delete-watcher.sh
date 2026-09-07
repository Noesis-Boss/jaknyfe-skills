#!/bin/bash
# inotify delete watcher for /home/workspace
# Logs all delete/move-out events to /var/log/workspace-deletes.log
set -u
LOG=/var/log/workspace-deletes.log
echo "$(date -u '+%Y-%m-%d %H:%M:%S') watcher starting" >> "$LOG"
inotifywait -m -r -q -e delete,moved_from /home/workspace \
  --exclude '(/\.git/|/node_modules/|/Archive/|/__pycache__/)' 2>>"$LOG" |
  while read -r path event file; do
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') $event $path$file" >> "$LOG"
  done
