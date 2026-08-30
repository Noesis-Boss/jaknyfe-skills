#!/usr/bin/env bun
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";

const HOME = homedir();
const WRAP = `${HOME}/.token-saver/scripts/wrap.py`;
const BIN = `${HOME}/.local/bin/token-saver`;
const env = { ...process.env, PATH: `${HOME}/.local/bin:${process.env.PATH ?? ""}` };

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(`Usage: bun run scripts/run.ts '<command>' | version | explain '<command>' | benchmark '<command>' | stats`);
  process.exit(1);
}

const mode = args[0];
if (mode === "version" || mode === "stats") {
  const cli = spawnSync(BIN, [mode], { encoding: "utf8", env });
  console.log(cli.stdout || cli.stderr);
  process.exit(cli.status ?? 1);
}

if (mode === "explain" || mode === "benchmark") {
  const cli = spawnSync(BIN, args, { encoding: "utf8", env });
  console.log(cli.stdout || cli.stderr);
  process.exit(cli.status ?? 1);
}

const command = args.join(" ");
const cli = spawnSync("python3", [WRAP, command], { encoding: "utf8" });
console.log(cli.stdout || cli.stderr);
process.exit(cli.status ?? 1);
