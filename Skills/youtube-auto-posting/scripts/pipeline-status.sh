#!/usr/bin/env bash
# youtube-auto-posting: show pipeline state for a channel workdir
# Usage: pipeline-status.sh /home/workspace/youtube/<channel> [video-slug]
dir="${1:-/home/workspace/youtube}"
slug="$2"
echo "== youtube-auto-posting pipeline status =="
if [ -n "$slug" ]; then
  vdir="$dir/videos/$slug"
  if [ ! -d "$vdir" ]; then echo "video folder not found: $vdir"; exit 1; fi
  echo "-- video: $slug"
  for f in titles-hooks.md script.md retention-notes.md final-metadata.md; do
    if [ -f "$vdir/$f" ]; then
      printf "DONE  %s (%s lines, modified %s)\n" "$f" "$(wc -l < "$vdir/$f")" "$(date -r "$vdir/$f" '+%Y-%m-%d %H:%M')"
    else
      printf "TODO  %s\n" "$f"
    fi
  done
else
  for f in channel-profile.md ideas.md; do
    if [ -f "$dir/$f" ]; then
      printf "DONE  %s (%s lines, modified %s)\n" "$f" "$(wc -l < "$dir/$f")" "$(date -r "$dir/$f" '+%Y-%m-%d %H:%M')"
    else
      printf "TODO  %s\n" "$f"
    fi
  done
  if [ -d "$dir/videos" ]; then
    echo "-- videos:"
    for v in "$dir/videos"/*/; do
      [ -d "$v" ] || continue
      n=$(ls "$v" 2>/dev/null | wc -l)
      printf "  %s (%s files)\n" "$(basename "$v")" "$n"
    done
  fi
fi
if [ -f "$dir/config.json" ]; then echo "config.json:"; cat "$dir/config.json"; fi
