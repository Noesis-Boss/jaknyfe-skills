#!/usr/bin/env bun
/**
 * faceless-yt-system runner — orchestrate the 5 stages of the faceless-youtube-system.
 *
 * Each stage is a SKILL.md; this runner only enforces:
 *   1. The handoff contract (each stage's required previous-stage output exists).
 *   2. The output file naming (so the next stage finds the previous one).
 *   3. The argument contract (niche for stage 1, video slug for stage 4).
 *
 * The actual stage content is produced by the LLM reading the stage's SKILL.md.
 * This runner does not produce the content; it tells the LLM which stage to run.
 */
import { existsSync } from "node:fs";
import { join, resolve } from "node:path";

const STAGES: Array<{
  n: number;
  label: string;
  skill: string;
  output: string;
  requires: number[];
  argHint: string;
}> = [
  { n: 1, label: "Niche & brand",        skill: "faceless-yt-niche-brand",       output: "01-niche-and-brand.md",       requires: [],    argHint: "<NICHE>" },
  { n: 2, label: "30-day content engine",skill: "faceless-yt-content-engine",    output: "02-30-day-calendar.md",       requires: [1],   argHint: "(no args)" },
  { n: 3, label: "Discoverability",      skill: "faceless-yt-discoverability",   output: "03-discoverability-pack.md",  requires: [1, 2], argHint: "(no args)" },
  { n: 4, label: "Retention script",     skill: "faceless-yt-retention-script",  output: "04-script-<SLUG>.md",         requires: [1, 2, 3], argHint: "<VIDEO-SLUG>" },
  { n: 5, label: "Monetization roadmap", skill: "faceless-yt-monetization",      output: "05-monetization-roadmap.md",  requires: [1, 2, 3], argHint: "(no args)" },
];

function findChannelDir(): string {
  // The runner expects to be run from inside the channel project directory.
  // If not, the caller must pass --dir.
  return process.cwd();
}

function checkRequirements(channelDir: string, requires: number[]): { ok: true } | { ok: false; missing: string[] } {
  const missing: string[] = [];
  for (const r of requires) {
    const stage = STAGES.find(s => s.n === r);
    if (!stage) continue;
    // Stage 4 has variable filename; just check that 01, 02, 03 exist.
    if (r === 4) continue;
    const file = join(channelDir, stage.output.replace("<SLUG>", "*"));
    // For stage 4 itself, do a glob check; otherwise an exact file check.
    if (stage.output.includes("<SLUG>")) {
      // Glob is allowed; do not require an exact match here.
      continue;
    }
    if (!existsSync(file)) missing.push(stage.output);
  }
  return missing.length === 0 ? { ok: true } : { ok: false, missing };
}

function printUsage() {
  console.log(`faceless-yt-system runner

Usage:
  bun run run.ts stage <N> [ARG]
  bun run run.ts list
  bun run run.ts check

Commands:
  stage <N> [ARG]   Run stage N with the given arg. Stage 1 needs <NICHE>,
                     stage 4 needs <VIDEO-SLUG>, others take no args.
  list               Print the 5 stages and their handoff contract.
  check              Verify the current directory has the right files for the
                     next stage to run.

Examples:
  cd ~/Projects/youtube/cooking-lab
  bun run run.ts stage 1 "home cooking for weeknight professionals"
  bun run run.ts stage 2
  bun run run.ts stage 3
  bun run run.ts stage 4 "sheet-pan-chicken-mistakes"
  bun run run.ts stage 5
`);
}

function printList() {
  console.log("faceless-yt-system — 5 stages\n");
  for (const s of STAGES) {
    const prev = s.requires.length === 0 ? "(no prerequisites)" : "requires stage " + s.requires.join(" + ");
    console.log(`  ${s.n}. ${s.label.padEnd(22)} → ${s.output.padEnd(32)} ${prev}`);
  }
  console.log("\nStage skills:");
  for (const s of STAGES) {
    console.log(`  ${s.n}. /home/workspace/Skills/${s.skill}/SKILL.md`);
  }
}

function runStage(channelDir: string, stageN: number, arg: string | undefined) {
  const stage = STAGES.find(s => s.n === stageN);
  if (!stage) {
    console.error(`Unknown stage: ${stageN}. Use 1-5.`);
    process.exit(2);
  }

  const req = checkRequirements(channelDir, stage.requires);
  if (!req.ok) {
    console.error(`Stage ${stageN} requires the following files to exist in ${channelDir}:`);
    for (const m of req.missing) console.error(`  - ${m}`);
    console.error(`\nRun the missing stages first.`);
    process.exit(3);
  }

  if (stageN === 1 && !arg) {
    console.error(`Stage 1 requires a niche argument: bun run run.ts stage 1 "<NICHE>"`);
    process.exit(2);
  }
  if (stageN === 4 && !arg) {
    console.error(`Stage 4 requires a video slug: bun run run.ts stage 4 "<VIDEO-SLUG>"`);
    process.exit(2);
  }

  const outputFile = stage.output.replace("<SLUG>", arg || "");
  const skillPath = `/home/workspace/Skills/${stage.skill}/SKILL.md`;

  console.log(`Stage ${stageN}: ${stage.label}`);
  console.log(`  skill:  ${skillPath}`);
  console.log(`  output: ${join(channelDir, outputFile)}`);
  console.log(`  niche:  ${arg || "(from stage 1)"}`);
  console.log(`\nRead ${skillPath} and produce the output file at the path above.`);
  console.log(`The skill's SKILL.md contains the full output contract.`);
}

function checkDir(channelDir: string) {
  console.log(`Checking ${channelDir}\n`);
  let next = 0;
  for (const s of STAGES) {
    const ok = s.requires.every(r => {
      const req = STAGES.find(x => x.n === r);
      if (!req || req.output.includes("<SLUG>")) return true;
      return existsSync(join(channelDir, req.output));
    });
    if (ok) {
      console.log(`  ✓ Stage ${s.n} (${s.label}) can run`);
    } else {
      if (next === 0) next = s.n;
      console.log(`  ✗ Stage ${s.n} (${s.label}) — missing prerequisites: ${s.requires.join(", ")}`);
    }
  }
  if (next) console.log(`\nNext stage to run: ${next}`);
  else console.log(`\nAll stages complete.`);
}

const args = process.argv.slice(2);
const cmd = args[0];

if (!cmd || cmd === "--help" || cmd === "-h") {
  printUsage();
  process.exit(0);
}

const channelDir = resolve(findChannelDir());

if (cmd === "list") {
  printList();
} else if (cmd === "check") {
  checkDir(channelDir);
} else if (cmd === "stage") {
  const n = parseInt(args[1] || "", 10);
  if (isNaN(n)) {
    console.error("Stage number required: bun run run.ts stage <1-5> [ARG]");
    process.exit(2);
  }
  runStage(channelDir, n, args[2]);
} else {
  console.error(`Unknown command: ${cmd}`);
  printUsage();
  process.exit(2);
}
