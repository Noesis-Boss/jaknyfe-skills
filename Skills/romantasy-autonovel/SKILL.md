---
name: romantasy-autonovel
description: Generate a Romantasy novel draft using the Enemies‑to‑Lovers + forced‑proximity outline stored in memory. Provides commands to create character sheets, chapter outlines, and full‑text scaffolding.
---
## Usage

- `npm run generate:characters` – pulls the character concept from memory and writes `file characters.md`.
- `npm run generate:outline` – builds the three‑act outline (uses the saved outline.md) and writes `file full-outline.md`.
- `npm run generate:draft` – combines characters and outline into a starter manuscript `file draft.md`.
- `bun run scripts/compile_pdf.ts [options]` – assembles `chapters/ch_*.md` into a printable PDF (Pandoc + xelatex). Options: `--title <text>`, `--author <name>`, `--output <file>`, `--chapters-dir <dir>`, `--paper <letter|a4|book>`, `--font-size <pt>`, `--margin <size>`, `--no-toc`, `--two-up`, `--quiet`.

## Scripts

The skill ships a small TypeScript CLI (`file scripts/main.ts`). Run it with `bun run scripts/main.ts <action>` where `<action>` is one of `characters`, `outline`, or `draft`. A separate script `file scripts/compile_pdf.ts` handles PDF assembly.

## Dependencies

- `bun` (runtime already available).
- No external packages; uses Node’s `fs` and the Zobodhi memory tool via a shell command.
- For PDF compilation: `pandoc` ≥ 2.17 and a TeX distribution with `xelatex` (TeX Live recommended).

## Example

```bash
cd $(pwd)/Skills/romantasy-autonovel
bun run scripts/main.ts draft
# produces draft.md in the same folder

# Compile chapter files into a printable PDF
cd /path/to/novel-project
bun run /home/workspace/Skills/romantasy-autonovel/scripts/compile_pdf.ts \
  --title "My Novel" \
  --author "Author Name" \
  --output my-novel.pdf \
  --paper letter \
  --font-size 12
```

Feel free to extend the skill with more actions (e.g., scene‑by‑scene expansion, export to PDF, etc.).

## New Action: generate novel

- `bun run scripts/generate_novel.ts` – reads the full outline and expands each chapter into a PG‑13 romantic fantasy narrative (≈90 000 words). The output is written to `file novel.md`.

## New Action: compile_pdf

- `bun run scripts/compile_pdf.ts` – stitches every `chapters/ch_*.md` (alphanumerically sorted, including suffixed filenames like `ch_20b.md`) into a single manuscript, then runs Pandoc + xelatex to produce a print-ready PDF. Honors `--top-level-division=part` so `# Part N: Title` headers inside chapter files render as book parts. Strips placeholder headings (`# Expansion for Ch N — …`) so they don't pollute the TOC. Writes a side-by-side `manuscript.md` for downstream export (ePub, HTML, etc.).

  Verified output: `Bound by Ash and Thorn` — 27 chapters, 99,780 words, 307-page PDF with clean TOC (all 27 entries, no expansion notes).