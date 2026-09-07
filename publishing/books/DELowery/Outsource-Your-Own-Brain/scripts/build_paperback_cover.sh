#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BOOK_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$BOOK_ROOT"

OUT="Outsource-Your-Own-Brain_paperback_cover.pdf"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cat > "$TMPDIR/cover.tex" <<'EOF'
\documentclass{article}
\usepackage[paperwidth=12.9225in,paperheight=9.25in,margin=0in]{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{fontspec}
\setmainfont{Noto Serif}
\setsansfont{Noto Sans}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\topskip}{0pt}
\definecolor{cream}{HTML}{F7F0E3}
\definecolor{navy}{HTML}{071A2D}
\definecolor{teal}{HTML}{117D88}
\begin{document}
\begin{tikzpicture}
  \fill[cream] (0in,0in) rectangle (12.9225in,9.25in);

  % Back panel: trim begins at 0.125in; barcode area is intentionally clear.
  \node[anchor=north west,inner sep=0,align=left,text width=4.55in]
    at (0.72in,8.55in) {\sffamily\bfseries\fontsize{24}{28}\selectfont\color{navy}Your business should not depend on you remembering everything.};
  \node[anchor=north west,inner sep=0,align=left,text width=4.55in]
    at (0.72in,7.25in) {\sffamily\fontsize{11.2}{15}\selectfont\color{navy}
    Every day, solopreneurs switch between client work, research, email, marketing, planning, writing, and decisions that cannot be delegated. The cost is more than lost time. It is fragmented attention, unfinished work, and less energy for the thinking that moves the business forward.

    \vspace{0.16in}
    \textit{Outsource Your Own Brain} introduces a practical operating system for using AI to handle repetitive cognitive work while keeping human judgment, accountability, and control where they belong.

    \vspace{0.16in}
    You’ll learn how to capture ideas before they disappear, reduce context switching and mental overload, use AI for research and routine production, build dependable workflows, protect quality and privacy, and preserve the human skills clients value most: judgment, relationships, creativity, and responsibility.

    \vspace{0.16in}
    The goal is not to let AI run your business. The goal is to stop spending your best attention on work that can be captured, organized, prepared, or checked with assistance.};

  \node[anchor=south west,inner sep=0,align=left,text width=4.55in]
    at (0.72in,1.58in) {\sffamily\fontsize{11.2}{15}\selectfont\color{navy}
    For consultants, writers, coaches, designers, and other independent professionals, this book offers a grounded way to work faster and think more clearly—without surrendering the decisions only you can make.};
  \node[anchor=south west,inner sep=0,align=left]
    at (0.72in,0.65in) {\sffamily\bfseries\fontsize{16}{19}\selectfont\color{navy}D. E. LOWERY, MBA};

  % KDP barcode reserve: leave white and unobstructed.
  \fill[white] (4.35in,0.18in) rectangle (5.95in,1.12in);
  \draw[navy,line width=0.5pt] (4.35in,0.18in) rectangle (5.95in,1.12in);
  \node[anchor=south west,inner sep=0] at (4.45in,0.23in)
    {\includegraphics[width=1.4in,height=0.78in]{assets/isbn-9798194009725.png}};

  % Spine.
  \node[rotate=-90,align=center,inner sep=0]
    at (6.46125in,7.35in) {\sffamily\bfseries\fontsize{12}{14}\selectfont\color{navy}OUTSOURCE YOUR OWN BRAIN};
  \node[rotate=-90,align=center,inner sep=0]
    at (6.46125in,1.05in) {\sffamily\bfseries\fontsize{11}{13}\selectfont\color{navy}D. E. LOWERY, MBA};

  % Existing front cover art, placed on the right trim panel.
  \node[anchor=south west,inner sep=0]
    at (6.7975in,0.125in) {\includegraphics[width=6in,height=9in]{Outsource-Your-Own-Brain_cover_art.png}};
\end{tikzpicture}
\end{document}
EOF

cp Outsource-Your-Own-Brain_cover_art.png "$TMPDIR/"
xelatex -interaction=nonstopmode -halt-on-error -output-directory="$TMPDIR" "$TMPDIR/cover.tex" >/dev/null
pdfseparate "$TMPDIR/cover.pdf" "$TMPDIR/cover-page-%d.pdf"
COVER_PAGES=$(pdfinfo "$TMPDIR/cover.pdf" | awk '/^Pages:/ {print $2}')
cp "$TMPDIR/cover-page-${COVER_PAGES}.pdf" "$OUT"

SIZE=$(pdfinfo "$OUT" | awk '/^Page size:/ {$1=""; sub(/^ +/, ""); print}')
PAGES=$(pdfinfo "$OUT" | awk '/^Pages:/ {print $2}')
echo "Built $OUT - ${PAGES} page, size: ${SIZE}"
