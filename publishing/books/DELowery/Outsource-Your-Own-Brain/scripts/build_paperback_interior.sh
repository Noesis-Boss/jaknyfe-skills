#!/usr/bin/env bash
# Build the 6 x 9 inch black-ink, no-bleed paperback interior for KDP.
# The cover is intentionally excluded; KDP receives the interior separately.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BOOK_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$BOOK_ROOT"

OUT="Outsource-Your-Own-Brain_paperback_interior.pdf"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

echo "=== Building 6 x 9 paperback interior ==="
pandoc manuscript.md \
  --pdf-engine=xelatex \
  --include-in-header=assets/paperback-header.tex \
  --toc --toc-depth=1 \
  -V geometry="paperwidth=6in,paperheight=9in,inner=0.85in,outer=0.65in,top=0.65in,bottom=0.65in" \
  -V mainfont="Noto Serif" \
  -V fontsize=11pt \
  -V classoption:twoside \
  -o "$OUT"

WORDS=$(pdftotext "$OUT" - 2>/dev/null | wc -w)
PAGES=$(pdfinfo "$OUT" 2>/dev/null | awk '/^Pages:/ {print $2}')
SIZE=$(pdfinfo "$OUT" 2>/dev/null | awk '/^Page size:/ {$1=""; sub(/^ +/, ""); print}')
echo "Built $OUT - ${PAGES} pages, ${WORDS} words, ${SIZE}"
