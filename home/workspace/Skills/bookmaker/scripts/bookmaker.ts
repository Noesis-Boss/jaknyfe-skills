#!/usr/bin/env bun
import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { resolve, join } from "node:path";

// Resolve skill paths relative to this script so it works from any cwd
const SCRIPT_DIR = import.meta.dir;
const SKILL_DIR = resolve(SCRIPT_DIR, "..");
const OUTPUT_DIR = join(SKILL_DIR, "assets", "output");
const PROMPTS_FILE = join(SKILL_DIR, "assets", "prompts.md");

type Args = Record<string, string | number>;

function parseArgs(argv: string[]): { cmd?: string; rest: string[]; flags: Args } {
  const [cmd, ...rest] = argv;
  const flags: Args = {};
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (!a.startsWith("--")) continue;
    const key = a.slice(2);
    const next = rest[i + 1];
    if (!next || next.startsWith("--")) {
      flags[key] = "true";
    } else {
      flags[key] = next;
      i++;
    }
  }
  return { cmd, rest, flags };
}

function getFlag(flags: Args, key: string, fallback = ""): string {
  return String(flags[key] ?? fallback);
}

function ensureOutputDir(): string {
  mkdirSync(OUTPUT_DIR, { recursive: true });
  return OUTPUT_DIR;
}

function writeStage(stage: number, name: string, body: string): string {
  const dir = ensureOutputDir();
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const file = join(dir, `stage${stage}-${name}-${stamp}.md`);
  writeFileSync(file, body);
  return file;
}

// Prompt builders — mirrors assets/prompts.md, fills brackets from flags
function buildPrompt(stage: number, f: Args): string {
  switch (stage) {
    case 1:
      return `Assume the role of a seasoned publishing strategist. Develop five commercially viable book concepts in ${getFlag(f, "niche", "[your niche]")}.

For each:

• Powerful title + persuasive subtitle
• Target reader demographics
• Differentiated positioning statement
• Market size estimate
• Why readers would pay $20-$30
• Relevant trends aligning with demand

Validate high-potential ideas before committing months to writing.`;
    case 2:
      return `Construct a chapter-by-chapter framework for ${getFlag(f, "genre", "[genre]")} book titled ${getFlag(f, "title", "[your title]")} for ${getFlag(f, "audience", "[target audience]")}. Include 10-15 chapters.

Per chapter:

• Benefit-driven title
• 3-5 essential concepts
• Word count (1,500-3,000)
• Reader transformation
• Transition to next chapter
• Hook for Chapter One
• Satisfying final chapter close

Delivers complete structural roadmap before drafting.`;
    case 3:
      return `Draft complete manuscript for Chapter ${getFlag(f, "number", "[number]")}: ${getFlag(f, "title", "[title]")} focused on ${getFlag(f, "topic", "[topic]")}.

Specs:

• Readership: ${getFlag(f, "audience", "[audience]")}
• Tone: ${getFlag(f, "tone", "[conversational/authoritative]")}
• Length: ${getFlag(f, "length", "1,500-3,000 words")}

Include:

• Compelling opening
• 3-4 sections with subheadings
• Specific examples/case studies
• Practical, actionable insights
• Bridge to next chapter

Use strong, active language. Avoid generic phrasing.`;
    case 4:
      return `Create eight original narrative pieces demonstrating ${getFlag(f, "concept", "[core concept]")} for ${getFlag(f, "genre", "[genre]")} book.

Each story (150-250 words):

• Vivid details, authentic dialogue
• Clear narrative arc (beginning, conflict, resolution)
• Resonates with ${getFlag(f, "audience", "[target audience]")}
• Meaningful takeaway without being instructional

Goal: Craft emotionally engaging illustrations deepening reader connection.`;
    case 5:
      return `Developing Chapter ${getFlag(f, "number", "X")} on ${getFlag(f, "subject", "[subject]")}. Compile authoritative research:

• 3-5 peer-reviewed studies with accessible summaries
• 2-3 compelling statistics from reputable sources
• 1-2 expert quotations from recognized authorities
• 1 relevant case study demonstrating concept
• Synthesis paragraph supporting central argument

Include proper citations. Note how each strengthens reader trust.`;
    default:
      throw new Error(`Unknown stage: ${stage}`);
  }
}

const STAGE_NAMES: Record<number, string> = {
  1: "idea-architect",
  2: "blueprint",
  3: "chapter-draft",
  4: "narrative",
  5: "evidence",
};

function requireFlags(f: Args, stage: number): string[] {
  const needs: Record<number, string[]> = {
    1: ["niche"],
    2: ["genre", "title", "audience"],
    3: ["number", "title", "topic", "audience", "tone", "length"],
    4: ["concept", "genre", "audience"],
    5: ["number", "subject"],
  };
  const req = needs[stage] ?? [];
  const missing = req.filter((k) => !f[k]);
  return missing;
}

function runStage(stage: number, f: Args): void {
  const missing = requireFlags(f, stage);
  if (missing.length > 0) {
    console.error(`Stage ${stage} (${STAGE_NAMES[stage]}) missing flags: --${missing.join(" --")}`);
    process.exit(1);
  }
  const prompt = buildPrompt(stage, f);
  console.log(`\n=== STAGE ${stage}: ${STAGE_NAMES[stage]} ===\n`);
  console.log(prompt);
  console.log("");
  // Persist the filled prompt so the user has a durable trail
  const file = writeStage(stage, STAGE_NAMES[stage], prompt);
  console.log(`[saved → ${file}]`);
}

async function runPipeline(f: Args): Promise<void> {
  const niche = getFlag(f, "niche");
  const genre = getFlag(f, "genre");
  const title = getFlag(f, "title");
  const audience = getFlag(f, "audience");
  const tone = getFlag(f, "tone");
  const length = getFlag(f, "length", "2000");

  if (!niche || !genre || !title || !audience) {
    console.error("pipeline requires: --niche --genre --title --audience (--tone optional)");
    process.exit(1);
  }

  console.log("\n========================================");
  console.log("  BOOKMAKER PIPELINE");
  console.log("========================================\n");

  // Stage 1 — ideas (uses niche)
  console.log(">> Stage 1/5: Idea Architect (niches) →", niche, "\n");
  runStage(1, { niche });

  // Stage 2 — blueprint (uses the chosen title as the winner)
  console.log("\n>> Stage 2/5: Blueprint for", title, "\n");
  runStage(2, { genre, title, audience });

  // Stage 3 — ask for a chapter count (default to first chapter)
  const chapterCount = parseInt(getFlag(f, "chapters", "0"), 10) || 1;
  for (let n = 1; n <= chapterCount; n++) {
    console.log(`\n>> Stage 3/5: Draft Chapter ${n}\n`);
    runStage(3, { number: n, title: `${title} - Chapter ${n}`, topic: genre, audience, tone, length });
  }

  // Stage 4 — narrative illustrations
  console.log("\n>> Stage 4/5: Narrative illustrations\n");
  runStage(4, { concept: title, genre, audience });

  // Stage 5 — evidence for chapter 1 (illustrative)
  console.log("\n>> Stage 5/5: Evidence (Chapter 1)\n");
  runStage(5, { number: 1, subject: genre });

  console.log("\n========================================");
  console.log("  PIPELINE COMPLETE");
  console.log(`  Outputs in: ${OUTPUT_DIR}`);
  console.log("========================================\n");
}

const HELP = `Bookmaker CLI — prompt chain for commercially viable nonfiction books

Usage:
  bun run bookmaker.ts stage <1-5> [flags]
  bun run bookmaker.ts pipeline [flags]
  bun run bookmaker.ts list
  bun run bookmaker.ts --help

Commands:
  stage <N>     Run a single stage with the required flags.
  pipeline      Run stages 1→2→3→4→5 sequentially, saving each to assets/output/.
  list          Print all five prompt templates (no flags needed).

Stage flags:
  Stage 1 (Idea Architect):     --niche "..."
  Stage 2 (Blueprint):         --genre "..." --title "..." --audience "..."
  Stage 3 (Chapter Draft):     --number N --title "..." --topic "..."
                                --audience "..." --tone "..."  --length W
  Stage 4 (Narrative):         --concept "..."  --genre "..."  --audience "..."
  Stage 5 (Evidence):          --number N --subject "..."

Pipeline flags (applies --niche to stage 1, rest to 2+):
  --niche --genre --title --audience [--tone] [--length W] [--chapters N]

Notes:
  • The scripts print filled prompts to stdout. Use the chat agent
    to execute the prompt and draft prose — the script chains prompts,
    it does not itself generate book content.
  • Filled prompts are saved to assets/output/ as a manuscript trail.
  • Use assets/prompts.md for copy-paste, no-CLI usage.

Full skill docs: SKILL.md
Source repo: https://github.com/zocomputer/skills (bookmaker)
`;

function list(): void {
  if (!existsSync(PROMPTS_FILE)) {
    console.error(`prompts file not found at ${PROMPTS_FILE}`);
    process.exit(1);
  }
  const { readFileSync } = require("node:fs");
  console.log(readFileSync(PROMPTS_FILE, "utf8"));
}

// --- main ---
const { cmd, flags } = parseArgs(process.argv.slice(2));

if (!cmd || cmd === "--help" || cmd === "-h" || cmd === "help") {
  console.log(HELP);
  process.exit(0);
}

if (cmd === "list") {
  list();
  process.exit(0);
}

if (cmd === "stage") {
  const n = parseInt(String(flags[Object.keys(flags).find((k) => k === "_0") ?? ""]), 10) ||
    parseInt(getFlag(flags, "_0"), 10) ||
    parseInt(process.argv[3] ?? "", 10);
  if (!n || n < 1 || n > 5) {
    console.error("stage requires a number 1-5 as the first positional arg");
    process.exit(1);
  }
  runStage(n, flags);
  process.exit(0);
}

if (cmd === "pipeline") {
  runPipeline(flags);
} else {
  console.error(`Unknown command: ${cmd}\n\n${HELP}`);
  process.exit(1);
}
