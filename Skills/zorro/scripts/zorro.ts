#!/usr/bin/env bun
/**
 * Zorro — self-improving orchestrator front-end.
 * Delegates memory recall/sync to Skills/astra-memory/scripts/sync.ts.
 *
 * Usage:
 *   bun run Skills/zorro/scripts/zorro.ts memory "<query>" [--limit=N] [--json]
 *   bun run Skills/zorro/scripts/zorro.ts autosync
 *   bun run Skills/zorro/scripts/zorro.ts plan "<task>"
 */
import { spawnSync } from "child_process";

const SYNC = "/home/workspace/Skills/astra-memory/scripts/sync.ts";
const LOGGER = "/home/workspace/Skills/agent-contracts/scripts/agent-contract.ts";

const [, , cmd, ...rest] = process.argv;

function runSync(args: string[]): number {
  const r = spawnSync("bun", ["run", SYNC, ...args], {
    stdio: "inherit",
    env: process.env,
  });
  if (r.error) {
    console.error(`zorro: failed to launch astra-memory sync.ts — ${r.error.message}`);
    return 1;
  }
  return r.status ?? 1;
}

function log(args: string[]): string {
  const r = spawnSync("bun", ["run", LOGGER, ...args], { encoding: "utf8", env: process.env });
  return r.status === 0 ? r.stdout.trim() : "";
}

function finish(runId: string, status: string, artifact?: string) {
  log(["finish", `--run=${runId}`, `--status=${status}`, ...(artifact ? [`--artifact=${artifact}`] : [])]);
}

switch (cmd) {
  case "memory": {
    const runId = log(["start", "--agent=zorro", "--surface=zorro"]);
    const q = rest.find((a) => !a.startsWith("--"));
    if (!q) {
      finish(runId, "error");
      console.error("Usage: zorro.ts memory \"<query>\" [--limit=N] [--json]");
      process.exit(1);
    }
    const args = ["query", q];
    const lim = rest.indexOf("--limit");
    if (lim !== -1 && rest[lim + 1]) args.push("--limit", rest[lim + 1]);
    else if (rest.includes("--limit=10") || rest.some((a) => a.startsWith("--limit=")))
      args.push(...rest.filter((a) => a.startsWith("--limit=")));
    if (rest.includes("--json")) args.push("--json");
    const status = runSync(args);
    finish(runId, status === 0 ? "ok" : "error");
    process.exit(status);
  }
  case "autosync": {
    const runId = log(["start", "--agent=zorro", "--surface=zorro"]);
    console.error("[zorro] autosync: syncing zobodhi + clarion → AstraDB…");
    const status = runSync(["sync"]);
    finish(runId, status === 0 ? "ok" : "error");
    process.exit(status);
  }
  case "plan": {
    const runId = log(["start", "--agent=zorro", "--surface=zorro"]);
    const task = rest.join(" ") || "(no task given)";
    console.log(`[zorro] plan for: ${task}`);
    console.log("1. RECALL  — bun run Skills/zorro/scripts/zorro.ts memory \"<keywords>\"");
    console.log("2. EXECUTE — smallest change that satisfies the task");
    console.log("3. VERIFY  — user-facing proof (screenshot / endpoint / log line)");
    console.log("4. AUTOSYNC — bun run Skills/zorro/scripts/zorro.ts autosync");
    finish(runId, "ok");
    process.exit(0);
  }
  default:
    console.error(
      "Usage: zorro.ts memory \"<query>\" | autosync | plan \"<task>\""
    );
    process.exit(1);
}
