#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s INPUT_VIDEO [OUTPUT_DIR]\n' "${0##*/}"
  printf 'Probes a render and extracts start, midpoint, and end frames for visual review.\n'
}

if [[ ${1:-} == --help || ${1:-} == -h ]]; then usage; exit 0; fi
if [[ $# -lt 1 || $# -gt 2 ]]; then usage >&2; exit 2; fi
input=$1
out_dir=${2:-"${input%.*}-review"}
[[ -f $input ]] || { printf 'Input not found: %s\n' "$input" >&2; exit 1; }
command -v ffprobe >/dev/null && command -v ffmpeg >/dev/null || { printf 'ffprobe and ffmpeg are required.\n' >&2; exit 1; }
mkdir -p "$out_dir"
ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate -of json "$input" > "$out_dir/probe.json"
duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$input")
awk -v d="$duration" 'BEGIN { if (d <= 0) exit 1 }' || { printf 'Invalid or zero duration.\n' >&2; exit 1; }
mid=$(awk -v d="$duration" 'BEGIN { printf "%.3f", d / 2 }')
end=$(awk -v d="$duration" 'BEGIN { t=d-0.1; if (t<0) t=0; printf "%.3f", t }')
for point in "start:0" "midpoint:$mid" "end:$end"; do
  name=${point%%:*}; time=${point#*:}
  ffmpeg -nostdin -v error -ss "$time" -i "$input" -frames:v 1 -q:v 2 -y "$out_dir/$name.jpg"
done
printf 'Probe: %s/probe.json\nReview frames: %s/{start,midpoint,end}.jpg\n' "$out_dir" "$out_dir"
