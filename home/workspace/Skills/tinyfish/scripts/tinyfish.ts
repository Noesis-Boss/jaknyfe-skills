#!/usr/bin/env bun
/**
 * Tinyfish wrapper for Zo Computer.
 *
 * Reads TINYFISH_API_KEY from environment (Zo Secrets, Settings > Advanced)
 * and forwards commands to the tinyfish CLI.
 *
 * Usage:
 *   bun run scripts/tinyfish.ts search query "hello world"
 *   bun run scripts/tinyfish.ts fetch content get "https://example.com"
 *   bun run scripts/tinyfish.ts agent run --sync "fill out the form" --url "https://example.com/form"
 */

import { execFileSync } from "node:child_process";
import process from "node:process";

const key = process.env.TINYFISH_API_KEY;
if (!key) {
  console.error("TINYFISH_API_KEY not set. Add it in Settings > Advanced.");
  process.exit(1);
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log("Usage: bun run scripts/tinyfish.ts <tinyfish-command> [args...]");
  console.log("  e.g. bun run scripts/tinyfish.ts search query \"hello world\"");
  process.exit(1);
}

try {
  const result = execFileSync("tinyfish", args, {
    env: { ...process.env, TINYFISH_API_KEY: key },
    encoding: "utf-8",
    stdio: "inherit",
  });
} catch (err: any) {
  if (err.status) {
    process.exit(err.status);
  }
  console.error("tinyfish error:", err.message);
  process.exit(1);
}