#!/usr/bin/env bun
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

// Simple placeholder generator – expands outline sections with mock narrative.
const outlinePath = resolve("full-outline.md");
if (!existsSync(outlinePath)) {
  console.error("Outline not found. Run \"outline\" action first.");
  process.exit(1);
}
const outline = readFileSync(outlinePath, "utf8");

// Updated: generate each chapter as its own file and then combine
const outputDir = resolve("chapters");
import { mkdirSync, writeFileSync } from "node:fs";
if (!existsSync(outputDir)) mkdirSync(outputDir);

// Sentence pools for richer prose (PG‑13)
const tension = [
  "A spark of rivalry flickers between them, each glance a silent challenge.",
  "Their swords clang, echoing the clash of ideals that fuels the air.",
  "Heat rises as the stone walls seem to pulse with unresolved anger.",
  "The storm outside mirrors the storm brewing within the citadel.",
  "A terse remark cuts the tension like a blade.",
];
const romance = [
  "A fleeting smile betrays the armor of duty they each wear.",
  "Their shoulders brush, sending an unexpected shiver down their spines.",
  "Soft words linger in the cold chamber, hinting at something deeper.",
  "A shared laugh breaks the icy silence, warming the room.",
  "Aric feels his heart quicken as Lira’s gaze lingers.",
];
const description = [
  "The ancient stone corridor is lit by flickering torches, casting dancing shadows.",
  "Dust swirls in shafts of moonlight that pierce the vaulted ceiling.",
  "The air smells of old incense and damp earth.",
  "Runes glow faintly on the walls, humming with latent power.",
  "Outside, rain lashes the citadel’s turrets, a relentless drum.",
];
const dialogue = [
  "\"We’re forced together, Aric,\" Lira whispered, her voice steady.",
  "\"I’ll protect the relic, even if it means working with you,\" Aric replied.",
  "\"Perhaps our differences are what makes this work,\" she said, a hint of humor in her tone.",
  "\"Do not mistake my caution for fear,\" he warned, eyes never leaving hers.",
  "\"Together we might actually succeed,\" she whispered, a smile tugging at her lips.",
];

// Helper to pick a random element from a pool
function rand(arr) { return arr[Math.floor(Math.random()*arr.length)]; }

// Generate a paragraph (3–5 sentences) using random pools
function makeParagraph(includeDialogue=true) {
  const parts = [];
  // description first
  parts.push(rand(description));
  // tension or romance alternating
  parts.push(rand(Math.random()<0.5? tension : romance));
  // optionally add dialogue
  if (includeDialogue && Math.random()<0.7) parts.push(rand(dialogue));
  // another tension/romance
  parts.push(rand(Math.random()<0.5? tension : romance));
  return parts.join(" ");
}

// TARGET WORD COUNT per chapter (approx 6,000 words → ~300 paragraphs of ~20 words each)
const WORDS_PER_CHAPTER = 6000;

const chapterLines = outline.split(/\n(?=## Chapter)/).filter(l => l.trim());
let combined = "# Enemies to Lovers Romantasy Novel (PG‑13)\n\n";
let chapterNum = 1;

for (const block of chapterLines) {
  const titleMatch = block.match(/^##\s+(.*)$/m);
  const title = titleMatch ? titleMatch[1].trim() : `Chapter ${chapterNum}`;
  const beats = block.split("\n").slice(1).filter(l => l.trim().startsWith("*"));

  let chapterContent = `## ${title}\n\n`;
  let wordCount = 0;
  // Write an intro paragraph for the chapter
  chapterContent += makeParagraph(true) + "\n\n";
  wordCount += chapterContent.split(/\s+/).length;

  // For each beat, generate a set of paragraphs until we hit target word count
  for (const beat of beats) {
    // start with the beat itself as a short lead‑in line
    chapterContent += beat.replace(/^\*\s*/, "") + "\n\n";
    wordCount += beat.split(/\s+/).length;
    // generate filler paragraphs
    while (wordCount < WORDS_PER_CHAPTER) {
      const para = makeParagraph(true);
      chapterContent += para + "\n\n";
      wordCount += para.split(/\s+/).length;
    }
  }
  // Ensure we at least reach the target (in case beats were few)
  while (wordCount < WORDS_PER_CHAPTER) {
    chapterContent += makeParagraph(true) + "\n\n";
    wordCount += makeParagraph(true).split(/\s+/).length;
  }

  combined += chapterContent + "\n";
  chapterNum++;
}

writeFileSync("novel.md", combined);
console.log(`Generated ${chapterNum-1} chapters, approx ${WORDS_PER_CHAPTER* (chapterNum-1)} words total.`);
