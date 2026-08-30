#!/usr/bin/env bun
/**
 * ViroScope viral idea generator.
 * Wraps the ViroScope AI endpoint (https://www.viroscopeai.com/generate).
 *
 * Usage:
 *   bun run viroscope.ts generate "<topic>" [--limit N] [--min-score N] [--json] [--uid <uid>]
 *   bun run viroscope.ts --help
 */
const ENDPOINT = "https://www.viroscopeai.com/api/generate-ideas";

const args = process.argv.slice(2);

function usage(): void {
  console.log(`ViroScope AI — viral YouTube idea generator

Usage:
  bun run viroscope.ts generate "<topic>" [options]

Options:
  --limit N       Show at most N ideas (default: all)
  --min-score N   Only show ideas with viralityScore >= N (default: 0)
  --json          Print raw JSON response
  --uid <uid>     User id sent to the API (default: env VIROSCOPE_UID or "zo-viroscope-user")
  --help          Show this help
`);
}

function badge(score: number): string {
  if (score >= 90) return "🟢 VIRAL HIT";
  if (score >= 82) return "🟠 HIGH POTENTIAL";
  return "🟣 STRONG IDEA";
}

function parseFlag(name: string, def: string): string {
  const i = args.indexOf(name);
  return i >= 0 && args[i + 1] ? args[i + 1] : def;
}

async function main(): Promise<void> {
  if (args.includes("--help") || args.length === 0) {
    usage();
    process.exit(args.length === 0 ? 1 : 0);
  }

  const cmd = args[0];
  if (cmd !== "generate") {
    console.error(`Unknown command: ${cmd}`);
    usage();
    process.exit(1);
  }

  const topic = args[1];
  if (!topic) {
    console.error("Error: topic is required. Example: bun run viroscope.ts generate \"funny cat videos\"");
    process.exit(1);
  }

  const json = args.includes("--json");
  const limit = parseInt(parseFlag("--limit", "0"), 10) || 0;
  const minScore = parseInt(parseFlag("--min-score", "0"), 10) || 0;
  const uid = parseFlag("--uid", process.env.VIROSCOPE_UID || "zo-viroscope-user");

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic, _uid: uid, _email: process.env.VIROSCOPE_EMAIL || null }),
  });

  const data = await res.json();

  if (!res.ok || data.error) {
    console.error(`ViroScope error: ${data.error || res.status}`);
    if (data.usage) {
      console.error(
        `Usage: ${data.usage.dailyUsed}/${data.usage.dailyLimit} today, ${data.usage.monthlyUsed}/${data.usage.monthlyLimit} this month`,
      );
    }
    process.exit(1);
  }

  if (json) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  const ideas = (data.ideas || [])
    .filter((i: { viralityScore: number }) => i.viralityScore >= minScore)
    .slice(0, limit || undefined);

  if (ideas.length === 0) {
    console.log(`No ideas met the filter (min-score ${minScore}).`);
    process.exit(0);
  }

  console.log(`\n🎯 Viral ideas for: "${topic}"\n`);
  ideas.forEach((idea: { title: string; description: string; viralityScore: number; outlierReason?: string; satisfactionPromise?: string }, idx: number) => {
    console.log(`${idx + 1}. ${idea.title}`);
    console.log(`   ${badge(idea.viralityScore)} — Score ${idea.viralityScore}/100`);
    console.log(`   ${idea.description}`);
    if (idea.outlierReason) console.log(`   Why it pops: ${idea.outlierReason}`);
    if (idea.satisfactionPromise) console.log(`   Promise: ${idea.satisfactionPromise}`);
    console.log("");
  });

  const u = data.usage;
  if (u) {
    console.log(`Usage: ${u.dailyUsed}/${u.dailyLimit} today · ${u.monthlyUsed}/${u.monthlyLimit} this month`);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
