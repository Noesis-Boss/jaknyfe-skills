#!/usr/bin/env bash
# youtube-auto-posting: show pipeline state for a channel workdir
# Usage: pipeline-status.sh /home/workspace/youtube/<channel>
dir="${1:-/home/workspace/youtube}"
echo "== youtube-auto-posting pipeline status =="
for f in channel-profile.md ideas.md titles-hooks.md script.md retention-notes.md; do
  if [ -f "$dir/$f" ]; then
    printf "DONE  %s (%s lines, modified %s)\n" "$f" "$(wc -l < "$dir/$f")" "$(date -r "$dir/$f" '+%Y-%m-%d %H:%M')"
  else
    printf "TODO  %s\n" "$f"
  fi
done
if [ -f "$dir/config.json" ]; then echo "config.json present:"; cat "$dir/config.json"; fi
