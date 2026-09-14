#!/usr/bin/env bun
import { appendFile, mkdir, readFile, readdir } from "node:fs/promises";
import { dirname, join } from "node:path";

const root = "/home/workspace";
const runsDir = join(root, "runs/agent-contracts");
const required = ["name", "purpose", "allowed_paths", "allowed_tools", "forbidden_actions"];

function arg(name: string) {
  const prefix = `--${name}=`;
  const found = Bun.argv.find(value => value.startsWith(prefix));
  return found?.slice(prefix.length);
}

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

async function log(record: Record<string, unknown>) {
  await mkdir(runsDir, { recursive: true });
  const runId = String(record.run_id);
  await appendFile(join(runsDir, `${runId}.jsonl`), `${JSON.stringify({ timestamp: new Date().toISOString(), ...record })}\n`);
}

function safeValue(value: string | undefined) {
  return value?.slice(0, 500);
}

async function allowedTools(agent: string, surface: string) {
  const file = join(root, "Skills/agent-contracts/config/agents", `${agent}.md`);
  const text = await readFile(file, "utf8").catch(() => "");
  if (!text) fail(`Missing contract for agent: ${agent}`);
  const section = text.match(/^allowed_tools:\n([\s\S]*?)(?=^forbidden_actions:|^---)/m)?.[1] ?? "";
  const tools = section.split("\n").map((line) => line.trim()).filter((line) => line.startsWith("- ")).map((line) => line.slice(2).trim());
  if (surface === "zorro" && !tools.includes("memory")) fail(`Contract does not allow memory: ${agent}`);
  return tools;
}

const [, , command, ...rest] = Bun.argv;
if (!command) fail("Usage: validate|start|event|finish|list|show");

if (command === "validate") {
  const file = rest[0];
  if (!file) fail("Missing contract file");
  const text = await readFile(file, "utf8");
  const frontmatter = text.match(/^---\n([\s\S]*?)\n---/m)?.[1] ?? "";
  const missing = required.filter(field => !new RegExp(`^${field}:\\s*`, "m").test(frontmatter));
  if (missing.length) fail(`Invalid contract. Missing: ${missing.join(", ")}`);
  console.log(JSON.stringify({ valid: true, file }));
} else if (command === "start") {
  const agent = arg("agent");
  const surface = arg("surface");
  if (!agent || !surface) fail("Required: --agent=NAME --surface=zorro|skill|automation");
  await allowedTools(agent, surface);
  const runId = `${agent}-${Date.now()}`;
  await log({ run_id: runId, agent, surface, type: "start", status: "running" });
  console.log(runId);
} else if (command === "event") {
  const runId = arg("run");
  const type = arg("type");
  if (!runId || !type) fail("Required: --run=RUN_ID --type=TYPE");
  if (type === "tool") {
    const files = (await readdir(runsDir).catch(() => [])).filter((file) => file === `${runId}.jsonl`);
    if (!files.length) fail(`Unknown run: ${runId}`);
    const records = (await readFile(join(runsDir, files[0]), "utf8")).trim().split("\n").filter(Boolean).map((line) => JSON.parse(line));
    const tools = await allowedTools(records[0].agent, records[0].surface);
    const name = arg("name") ?? "";
    const permitted = tools.some((tool) => name === tool || name.startsWith(`${tool}.`));
    if (!permitted) fail(`Contract denied tool: ${name}`);
  }
  await log({ run_id: runId, type, name: safeValue(arg("name")), status: arg("status") ?? "ok", path: safeValue(arg("path")) });
  console.log(runId);
} else if (command === "finish") {
  const runId = arg("run");
  if (!runId) fail("Required: --run=RUN_ID");
  await log({ run_id: runId, type: "finish", status: arg("status") ?? "ok", artifact: arg("artifact") });
  console.log(runId);
} else if (command === "list") {
  const limit = Number(arg("limit") ?? 20);
  const files = (await readdir(runsDir).catch(() => []))
    .filter(file => file.endsWith(".jsonl"))
    .sort()
    .reverse()
    .slice(0, limit);
  for (const file of files) {
    const records = (await readFile(join(runsDir, file), "utf8"))
      .trim().split("\n").filter(Boolean).map(line => JSON.parse(line));
    const first = records[0];
    const last = records.at(-1);
    console.log(JSON.stringify({ run_id: first?.run_id, agent: first?.agent, surface: first?.surface, started: first?.timestamp, status: last?.status, records: records.length }));
  }
} else if (command === "show") {
  const runId = rest[0] ?? arg("run");
  if (!runId) fail("Required: show RUN_ID");
  const file = join(runsDir, `${runId}.jsonl`);
  console.log(await readFile(file, "utf8"));
} else {
  fail(`Unknown command: ${command}`);
}
