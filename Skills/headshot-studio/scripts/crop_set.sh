#!/bin/sh
set -eu

src="${1:?usage: crop_set.sh <edited.jpg> <out_dir>}"
out="${2:?usage: crop_set.sh <edited.jpg> <out_dir>}"
offset_y="${OFFSET_Y:-0}"
name=$(basename "${src%.*}")
mkdir -p "$out"

w=$(identify -format '%w' "$src")
h=$(identify -format '%h' "$src")

sq=$(( w < h ? w : h ))
if [ $(( sq + offset_y )) -gt "$h" ]; then
  sq=$(( h - offset_y ))
fi
if [ "$sq" -lt 800 ]; then
  echo "source too small for 800px square: ${w}x${h}" >&2
  exit 1
fi
convert "$src" -strip -colorspace sRGB -crop "${sq}x${sq}+0+${offset_y}" +repage \
  -resize 800x800 -interlace Plane -quality 92 "$out/$name-square-800.jpg"
convert "$out/$name-square-800.jpg" -resize 160x160 -quality 92 "$out/$name-square-160-preview.jpg"

bh=$(( w / 3 ))
if [ $(( bh + offset_y )) -gt "$h" ]; then
  echo "source too short for 3:1 banner: ${w}x${h} (needs height >= $bh past offset $offset_y)" >&2
  exit 1
fi
convert "$src" -strip -colorspace sRGB -crop "${w}x${bh}+0+${offset_y}" +repage \
  -resize 1500x500! -interlace Plane -quality 92 "$out/$name-banner-1500x500.jpg"

vw=$(( h * 4 / 5 < w ? h * 4 / 5 : w ))
vh=$(( vw * 5 / 4 ))
if [ $(( vh + offset_y )) -gt "$h" ]; then
  vh=$(( h - offset_y ))
  vw=$(( vh * 4 / 5 ))
fi
convert "$src" -strip -colorspace sRGB -crop "${vw}x${vh}+0+${offset_y}" +repage \
  -resize 1000x1250! -interlace Plane -quality 92 "$out/$name-vertical-1000x1250.jpg"

ls -1 "$out/$name"-*.jpg
