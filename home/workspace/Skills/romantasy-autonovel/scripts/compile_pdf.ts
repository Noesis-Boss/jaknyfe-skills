#!/usr/bin/env bun
// compile_pdf.ts — Assemble chapter .md files into a printable PDF.
//
// Auto-discovers chapters/ch_*.md (sorted alphanumerically), stitches them
// into a single manuscript.md with a Pandoc title page, then compiles via
// Pandoc + xelatex. Splits chapters into Parts by detecting top-level
// `# Part N: Title` headers in the chapter files (or, if absent, just runs
// straight through as a single Part).
//
// Usage:
//   bun run scripts/compile_pdf.ts [options]
//
// Options:
//   --title <text>       Book title (default: derived from parent folder)
//   --author <name>      Author name (default: env $AUTHOR or "Anonymous")
//   --output <file>      Output PDF path (default: <title>.pdf)
//   --manuscript <file>  Intermediate manuscript path (default: manuscript.md)
//   --chapters-dir <d>   Source chapters directory (default: chapters)
//   --paper <size>       letter | a4 | book (6x9 trimmed) (default: letter)
//   --font-size <pt>     10 | 11 | 12 | 13 | 14 (default: 12)
//   --two-up             Use twocolumn layout (default off)
//   --no-toc             Suppress the table of contents
//   --margin <size>      LaTeX margin, e.g. "1in", "2cm" (default: 1in)
//   --quiet              Suppress per-step progress logs

import { execSync, spawnSync } from "node:child_process";
import {
  existsSync,
  readdirSync,
  readFileSync,
  writeFileSync,
  mkdirSync,
} from "node:fs";
import { basename, dirname, join, resolve } from "node:path";

const SKILL_DIR = resolve(dirname(new URL(import.meta.url).pathname), "..");
const WORK_DIR = process.cwd();

// ---------- args ----------
function parseArgs(argv: string[]): Record<string, string | boolean> {
  const out: Record<string, string | boolean> = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) {
        out[key] = true;
      } else {
        out[key] = next;
        i++;
      }
    }
  }
  return out;
}

const args = parseArgs(process.argv.slice(2));
const quiet = !!args.quiet;

function log(...m: unknown[]) {
  if (!quiet) console.log("•", ...m);
}

function die(msg: string): never {
  console.error("✗", msg);
  process.exit(1);
}

// ---------- locate chapters ----------
const chaptersDir = resolve(
  typeof args["chapters-dir"] === "string"
    ? (args["chapters-dir"] as string)
    : "chapters"
);
if (!existsSync(chaptersDir)) {
  die(`Chapters directory not found: ${chaptersDir}`);
}

const chapterFiles = readdirSync(chaptersDir)
  .filter((f) => /^(ch|chapter)[-_]?\d+([a-zA-Z]?(?:[._-]\d+)?)?\.md$/i.test(f) || /^\d+\.md$/.test(f))
  .sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" })
  );

if (chapterFiles.length === 0) {
  die(`No chapter .md files found in ${chaptersDir} (expected ch_NN.md).`);
}
log(`Found ${chapterFiles.length} chapter files.`);

// ---------- title / author / output ----------
function deriveTitle(): string {
  const folder = basename(resolve(WORK_DIR));
  return folder
    .replace(/[-_]+/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

const title =
  typeof args.title === "string" ? (args.title as string) : deriveTitle();
const author =
  typeof args.author === "string"
    ? (args.author as string)
    : process.env.AUTHOR || "Anonymous";

const outName =
  typeof args.output === "string"
    ? (args.output as string)
    : title.replace(/\s+/g, "-") + ".pdf";
const manuscriptPath = resolve(
  typeof args.manuscript === "string"
    ? (args.manuscript as string)
    : "manuscript.md"
);

// ---------- paper / typography ----------
const paper = (typeof args.paper === "string" ? args.paper : "letter") as string;
const fontSize =
  typeof args["font-size"] === "string"
    ? (args["font-size"] as string)
    : "12";
const twoUp = !!args["two-up"];
const noToc = !!args["no-toc"];
const margin =
  typeof args.margin === "string" ? (args.margin as string) : "1in";

const paperMap: Record<string, [string, string]> = {
  letter: ["letterpaper", "11pt"],
  a4: ["a4paper", "11pt"],
  book: ["6x9", "11pt"], // memoir trim — Pandoc stock
};
const [paperGeom, baseSize] = paperMap[paper] ?? paperMap.letter;

// ---------- assemble manuscript ----------
const titlePage = [
  "---",
  `title: "${title.replace(/"/g, '\\"')}"`,
  `author: "${author.replace(/"/g, '\\"')}"`,
  `documentclass: book`,
  `classoption: [${baseSize},${paperGeom},oneside,openany]`,
  `geometry: margin=${margin}`,
  "fontsize: 11pt",
  "linestretch: 1.4",
  "mainfont: 'PT Serif'",
  "sansfont: 'PT Sans'",
  "monofont: 'PT Mono'",
  "colorlinks: true",
  "linkcolor: midnightblue",
  "urlcolor: midnightblue",
  "toccolor: black",
  "---",
  "",
];

const blocks: string[] = titlePage;
let chapterCount = 0;
// Match any leading level-1 heading: "# Chapter Twenty: ..." or "# One: ..." etc.
const chapterTitleRe = /^#\s+(.+?)\s*$/m;
// Strip development placeholders that aren't real chapters.
const expansionRe = /^#\s+Expansion(?:\s+for\s+Ch\.?\s*\d+)?\s*[—\-–:].*\n([\s\S]*?)(?=^#\s|\Z)/gm;

for (const f of chapterFiles) {
  const raw = readFileSync(join(chaptersDir, f), "utf8").trimEnd();
  // Drop "Expansion for Ch N — …" placeholder sections.
  const cleaned = raw.replace(expansionRe, "");
  const m = cleaned.match(chapterTitleRe);
  if (!m) continue; // skip files with no chapter title
  blocks.push(cleaned);
  blocks.push("\n\n\\newpage\n\n");
  chapterCount++;
}

const manuscript = blocks.join("\n");
mkdirSync(dirname(manuscriptPath), { recursive: true });
writeFileSync(manuscriptPath, manuscript, "utf8");
log(`Wrote manuscript: ${manuscriptPath}`);

// ---------- pandoc ----------
function run(cmd: string): void {
  log(`$ ${cmd}`);
  const r = spawnSync(cmd, { stdio: "inherit", shell: true });
  if (r.status !== 0) die(`Command failed (exit ${r.status}): ${cmd}`);
}

const pandocArgs = [
  manuscriptPath,
  "-o",
  outName,
  "--pdf-engine=xelatex",
  "--from=markdown+yaml_metadata_block",
  "--top-level-division=part",
];

if (!noToc) pandocArgs.push("--toc", "--toc-depth=1");
if (twoUp) pandocArgs.push("--two-column");

run(`pandoc ${pandocArgs.map((a) => (a.includes(" ") ? `"${a}"` : a)).join(" ")}`);

// ---------- summary ----------
const sizeBytes = (() => {
  try {
    return readFileSync(outName).byteLength;
  } catch {
    return 0;
  }
})();

const wordCount = manuscript
  .replace(/---[\s\S]*?---/, "")
  .split(/\s+/)
  .filter(Boolean).length;

console.log("");
console.log("✅ Compiled:", outName);
console.log("   chapters:", chapterCount);
console.log("   words:   ", wordCount.toLocaleString());
console.log("   size:    ", (sizeBytes / 1024).toFixed(1), "KB");