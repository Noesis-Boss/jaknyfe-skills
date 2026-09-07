#!/usr/bin/env bash
# Build book from manuscript.md -> PDF + EPUB.
#
# PDF: standalone cover page (image full-bleed) prepended via pdfunite.
#      Then manuscript with TOC + title + content + About the Author.
# EPUB: --epub-cover-image embeds the cover as cover.xhtml.
#
# Usage:
#   bash scripts/build_book.sh          # PDF + EPUB
#   bash scripts/build_book.sh --pdf    # PDF only
#   bash scripts/build_book.sh --epub   # EPUB only
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BOOK_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$BOOK_ROOT"

PDF=0
EPUB=0
for arg in "$@"; do
  case "$arg" in
    --pdf)  PDF=1 ;;
    --epub) EPUB=1 ;;
    "")     PDF=1; EPUB=1 ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done
{ [ "$PDF" -eq 1 ] && [ "$EPUB" -eq 1 ] || true; }
if [ "$PDF" -eq 0 ] && [ "$EPUB" -eq 0 ]; then
  PDF=1; EPUB=1
fi

TITLE="Outsource Your Own Brain"
COVER="Outsource-Your-Own-Brain_cover_art.png"
OUT_PDF="Outsource-Your-Own-Brain.pdf"
OUT_EPUB="Outsource-Your-Own-Brain.epub"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

if [ "$PDF" -eq 1 ]; then
  echo "=== Building PDF ==="

  # 1. Build cover page as a standalone PDF (full-bleed, no margins).
  cat > "$TMPDIR/cover.tex" <<EOF
\\documentclass[letterpaper]{article}
\\usepackage[margin=0in]{geometry}
\\usepackage{graphicx}
\\begin{document}
\\thispagestyle{empty}
\\centering
\\includegraphics[width=\\paperwidth,height=\\paperheight,keepaspectratio]{$COVER}
\\end{document}
EOF
  cp "$COVER" "$TMPDIR/"
  xelatex -output-directory="$TMPDIR" "$TMPDIR/cover.tex" >/dev/null 2>&1

  # 2. Build the main book body (TOC + title page + content + back matter).
  pandoc manuscript.md \
    --pdf-engine=xelatex \
    --include-in-header=assets/pdf-header.tex \
    --toc --toc-depth=1 \
    -V geometry:margin=1in \
    -V mainfont="Noto Serif" \
    -V fontsize=12pt \
    -V classoption:oneside \
    -o "$TMPDIR/book_body.pdf"

  # 3. Prepend cover page so it is page 1.
  pdfunite "$TMPDIR/cover.pdf" "$TMPDIR/book_body.pdf" "$OUT_PDF"

  WORDS=$(pdftotext "$OUT_PDF" - 2>/dev/null | wc -w)
  PAGES=$(pdfinfo "$OUT_PDF" 2>/dev/null | awk '/^Pages:/ {print $2}')
  echo "Built $OUT_PDF - ${PAGES} pages, ${WORDS} words"
fi

if [ "$EPUB" -eq 1 ]; then
  echo "=== Building EPUB ==="
  pandoc manuscript.md \
    --epub-cover-image="$COVER" \
    --css="assets/epub-override.css" \
    --standalone \
    -o "$OUT_EPUB"

  COVER_DECLARED=$(unzip -p "$OUT_EPUB" EPUB/content.opf 2>/dev/null | grep -c 'meta name="cover')
  echo "Built $OUT_EPUB - cover declared: $COVER_DECLARED (1=yes)"
fi
