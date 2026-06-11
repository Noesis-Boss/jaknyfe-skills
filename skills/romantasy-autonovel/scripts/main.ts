#!/usr/bin/env bun
import { execSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const ACTION = process.argv[2];
if (!ACTION) {
  console.error("Usage: bun run scripts/main.ts <characters|outline|draft>");
  process.exit(1);
}

// Helper to fetch a fact from Zobodhi memory (uses the CLI tool added earlier)
function getMemoryFact(tag: string): string {
  try {
    const out = execSync(`bun run /home/workspace/Skills/zodobhi-memory/scripts/memory.ts --get "${tag}"`, {
      encoding: "utf8",
    });
    return out.trim();
  } catch (e) {
    return "";
  }
}

function writeIfMissing(path: string, content: string) {
  const full = resolve(path);
  if (!existsSync(full)) writeFileSync(full, content);
}

switch (ACTION) {
  case "characters": {
    const fact = getMemoryFact("Character");
    const md = `# Characters\n\n${fact}\n`;
    writeFileSync(resolve("characters.md"), md);
    console.log("Wrote characters.md");
    break;
  }
  case "outline": {
    // copy the outline from the workspace if it exists
    const src = "/home/workspace/Stories/romantasy/EnemiesToLovers/outline.md";
    const dest = resolve("full-outline.md");
    if (existsSync(src)) {
      const data = readFileSync(src, "utf8");
      writeFileSync(dest, data);
      console.log("Copied outline to full-outline.md");
    } else {
      console.error("Outline not found at", src);
    }
    break;
  }
  case "draft": {
    const charsPath = resolve("characters.md");
    const outlinePath = resolve("full-outline.md");
    if (!existsSync(charsPath) || !existsSync(outlinePath)) {
      console.error("Run \"characters\" and \"outline\" first.");
      process.exit(1);
    }
    const draft = `# Draft – Enemies to Lovers Romantasy\n\n${readFileSync(charsPath, "utf8")}\n---\n${readFileSync(outlinePath, "utf8")}`;
    writeFileSync(resolve("draft.md"), draft);
    console.log("Created draft.md");
    break;
  }
  default:
    console.error("Unknown action", ACTION);
    process.exit(1);
}
