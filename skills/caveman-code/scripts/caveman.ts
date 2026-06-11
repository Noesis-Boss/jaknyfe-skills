#!/usr/bin/env bun
/**
 * caveman-code wrapper.
 * Forwards argv to the `caveman` binary, installing it globally via npm if missing.
 *
 * Defaults: OpenRouter with openrouter/owl-alpha (overridable via flags).
 *
 * Usage:
 *   bun run caveman.ts --help
 *   bun run caveman.ts -p "summarize this file"
 *   bun run caveman.ts --provider google -p "list files in /tmp"
 */

import { spawnSync } from "node:child_process";

const PACKAGE = "@juliusbrussee/caveman-code";
const BINARY = "caveman";
const DEFAULT_PROVIDER = "openrouter";
const DEFAULT_MODEL = "openrouter/owl-alpha";

function binaryExists(): boolean {
  const r = spawnSync("which", [BINARY], { encoding: "utf8" });
  return r.status === 0 && r.stdout.trim().length > 0;
}

function installGlobal(): void {
  console.error(`[caveman] ${BINARY} not found on PATH; installing ${PACKAGE} globally...`);
  const r = spawnSync("npm", ["install", "-g", "--yes", PACKAGE], {
    stdio: "inherit",
    encoding: "utf8",
  });
  if (r.status !== 0) {
    console.error(`[caveman] global install failed (exit ${r.status})`);
    process.exit(r.status ?? 1);
  }
}

if (!binaryExists()) {
  installGlobal();
  if (!binaryExists()) {
    console.error(`[caveman] ${BINARY} still not on PATH after install. Check npm global bin directory.`);
    process.exit(1);
  }
}

// env: caveman expects GEMINI_API_KEY, but the workspace exposes GOOGLE_GENERATIVE_AI_KEY
if (!process.env.GEMINI_API_KEY && process.env.GOOGLE_GENERATIVE_AI_KEY) {
  process.env.GEMINI_API_KEY = process.env.GOOGLE_GENERATIVE_AI_KEY;
}

const userArgs = process.argv.slice(2);
const args = [...userArgs];
const hasProvider = userArgs.includes("--provider") || userArgs.includes("-P");
const hasModel = userArgs.includes("--model") || userArgs.includes("-m");
if (!hasProvider) args.push("--provider", DEFAULT_PROVIDER);
if (!hasModel) args.push("--model", DEFAULT_MODEL);

const r = spawnSync(BINARY, args, { stdio: "inherit", encoding: "utf8" });
process.exit(r.status ?? 0);
