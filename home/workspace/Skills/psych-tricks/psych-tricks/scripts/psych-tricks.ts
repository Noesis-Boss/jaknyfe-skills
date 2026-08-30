#!/usr/bin/env bun
/**
 * psych-tricks.ts
 *
 * Reference tool: list all 49 tricks, search by keyword, or get details on specific items.
 *
 * Usage:
 *   bun psych-tricks.ts list              — list all titles
 *   bun psych-tricks.ts detail <N>        — show trick #N (concept + study + application)
 *   bun psych-tricks.ts search "<query>"  — search concept/application text for matching tricks
 *   bun psych-tricks.ts apply "<what you're writing>" — print the full reference for the AI to reason over
 */
import { readFileSync } from "node:fs";

const TRICKS_PATH = new URL("./tricks.json", import.meta.url).pathname;
const data: Array<{
  number: number;
  title: string;
  concept: string;
  study: string;
  technique: string;
  examples: string;
  application: string;
}> = JSON.parse(readFileSync(TRICKS_PATH, "utf8"));

const cmd = process.argv[2];
const arg = process.argv[3] || "";

if (cmd === "list") {
  for (const t of data) {
    const hasApp = t.application ? " ✓" : "";
    console.log(`${t.number.toString().padStart(2)}. ${t.title}${hasApp}`);
  }
} else if (cmd === "detail") {
  const n = parseInt(arg, 10);
  const t = data.find((x) => x.number === n);
  if (!t) {
    console.error(`No trick #${n}`);
    process.exit(1);
  }
  console.log(`#${t.number} — ${t.title}`);
  console.log(`\nConcept: ${t.concept}`);
  if (t.study) console.log(`\nStudy: ${t.study}`);
  if (t.technique) console.log(`\nTechnique: ${t.technique}`);
  if (t.examples) console.log(`\nExamples: ${t.examples}`);
  if (t.application) console.log(`\nApplication: ${t.application}`);
} else if (cmd === "search") {
  const q = arg.toLowerCase();
  const results = data.filter(
    (t) =>
      t.title.toLowerCase().includes(q) ||
      t.concept.toLowerCase().includes(q) ||
      t.application.toLowerCase().includes(q) ||
      (t.examples && t.examples.toLowerCase().includes(q)),
  );
  if (results.length === 0) {
    console.log("No matching tricks found.");
  } else {
    console.log(`Found ${results.length} matching trick(s):`);
    for (const t of results) {
      console.log(`  #${t.number} — ${t.title}`);
      console.log(`    ${t.application.slice(0, 120)}`);
    }
  }
} else if (cmd === "apply") {
  // Print the full reference — the AI will reason over which to use.
  console.log(
    "=== 49 Psychological Mind Tricks Reference ===\n" +
      "Below are all 49 tricks with concept and application.\n" +
      "Select 3-5 most relevant to the task and integrate them.\n\n",
  );
  for (const t of data) {
    console.log(`## ${t.number}. ${t.title}`);
    console.log(`Concept: ${t.concept}`);
    console.log(`Application: ${t.application || "(not provided in source)"}`);
    console.log();
  }
} else if (cmd === "summarize") {
  // Compact summary for prompt context
  for (const t of data) {
    console.log(
      `${t.number}. ${t.title}\n   ${t.concept.slice(0, 200)}\n   Apply: ${(t.application || "").slice(0, 200)}`,
    );
    console.log();
  }
} else {
  console.log(`Usage: bun psych-tricks.ts <command> [args]

Commands:
  list                    List all 49 trick titles
  detail <N>              Show full detail for trick #N
  search "<query>"        Search tricks matching query
  apply "<description>"   Print full reference for AI reasoning
  summarize               Compact summary of all 49 tricks`);
}
