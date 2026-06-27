#!/usr/bin/env bun
/**
 * task-orchestrator.ts
 * Hermes agent that watches Syndicate tasks, evaluates them with /zo/ask,
 * claims suitable ones, and performs local work.
 *
 * Requirements:
 *   - ZO_API_TOKEN env var (https://api.zo.computer/zo/ask)
 *   - SYNDICATE_API_URL env var (default: https://syndicate-jaknyfe.zocomputer.io)
 *   - SYNDICATE_AGENT_ID env var – the Syndicate agent ID that will claim tasks
 *   - ADMIN_SESSION_TOKEN (optional) – Bearer token if you want to bypass login
 *
 * Run:
 *   bun run task-orchestrator.ts
 */

const SYNDICATE_API_URL = process.env.SYNDICATE_API_URL ?? "https://syndicate-jaknyfe.zocomputer.io";
const POLL_INTERVAL_MS = Number(process.env.POLL_INTERVAL_MS ?? "30000");
const ZO_API_TOKEN = process.env.ZO_API_TOKEN;
const SYNDICATE_AGENT_ID = process.env.SYNDICATE_AGENT_ID;

let SESSION_COOKIE = "";

if (!ZO_API_TOKEN) {
  console.error("❌ ZO_API_TOKEN is required");
  process.exit(1);
}
if (!SYNDICATE_AGENT_ID) {
  console.error("❌ SYNDICATE_AGENT_ID is required (the agent that will claim tasks)");
  process.exit(1);
}

// -----------------------------------------------------------------------
// Types
// -----------------------------------------------------------------------
type Task = {
  id: string;
  company_id: string;
  project_id: string | null;
  title: string;
  description: string | null;
  status: "backlog" | "ready" | "running" | "blocked" | "done";
  priority: number;
};

type AIVerdict = {
  canClaim: boolean;
  reason: string;
  suggestedAction?: string;
};

// -----------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------
async function login(): Promise<void> {
  const resp = await fetch(`${SYNDICATE_API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "admin@example.com", password: "StrongPass!234" }),
  });
  if (!resp.ok) throw new Error(`Login failed: ${resp.status}`);
  const setCookie = resp.headers.get("set-cookie");
  if (setCookie) {
    SESSION_COOKIE = setCookie.split(";")[0];
    console.log(`✓ Authenticated`);
  }
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "application/json",
    ...(init?.headers as Record<string, string> | undefined),
  };
  if (SESSION_COOKIE) {
    headers["Cookie"] = SESSION_COOKIE;
  }
  const resp = await fetch(url, { ...init, headers });
  if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText} on ${url}`);
  return (await resp.json()) as T;
}

async function askZo(prompt: string): Promise<string> {
  const resp = await fetch("https://api.zo.computer/zo/ask", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${ZO_API_TOKEN}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      input: prompt,
      model_name: "vercel:minimax/minimax-m3",
    }),
  });
  if (!resp.ok) throw new Error(`Zo ask failed: ${resp.status}`);
  const data = (await resp.json()) as { output: string };
  return data.output;
}

// -----------------------------------------------------------------------
// AI Evaluation
// -----------------------------------------------------------------------
async function evaluateTask(task: Task): Promise<AIVerdict> {
  const prompt = `You are a task orchestrator for the Syndicate platform.

Task: ${JSON.stringify(task, null, 2)}

Decide whether this task should be claimed and executed by an automated agent.
Consider:
- Is the work clearly defined and deterministic?
- Can it be performed without human interaction?
- Is there a safe, reversible action we can take?

Respond with a JSON object:
{
  "canClaim": true|false,
  "reason": "short explanation",
  "suggestedAction": "optional hint for the executor"
}
Only output the JSON, nothing else.`;
  const raw = await askZo(prompt);
  try {
    return JSON.parse(raw) as AIVerdict;
  } catch {
    // Fallback if the model returns surrounding text
    const match = raw.match(/\{[\s\S]*\}/);
    if (match) return JSON.parse(match[0]) as AIVerdict;
    return { canClaim: false, reason: `Unparseable AI response: ${raw}` };
  }
}

// -----------------------------------------------------------------------
// Local execution – replace this with real work
// -----------------------------------------------------------------------
async function executeTask(task: Task, action?: string): Promise<string> {
  // Example: log the action. Replace with real logic (e.g., call BankBox API).
  console.log(`⚙️  Executing task ${task.id}: ${action ?? task.title}`);
  // Simulate work
  await new Promise((r) => setTimeout(r, 1000));
  return `Executed: ${action ?? task.title}`;
}

// -----------------------------------------------------------------------
// Syndicate API wrappers
// -----------------------------------------------------------------------
async function getPendingTasks(): Promise<Task[]> {
  const data = await fetchJson<{ companies: { id: string }[] }>(`${SYNDICATE_API_URL}/api/companies`);
  const allTasks: Task[] = [];
  for (const co of data.companies) {
    const res = await fetchJson<{ tasks: Task[] }>(`${SYNDICATE_API_URL}/api/companies/${co.id}/tasks`);
    allTasks.push(...res.tasks.filter((t) => t.status === "backlog" || t.status === "ready"));
  }
  // Sort by priority descending, then oldest first
  return allTasks.sort((a, b) => b.priority - a.priority);
}

async function claimTask(taskId: string): Promise<void> {
  await fetchJson(`${SYNDICATE_API_URL}/api/tasks/${taskId}/claim`, {
    method: "POST",
    body: JSON.stringify({ agent_id: SYNDICATE_AGENT_ID }),
  });
}

async function completeTask(taskId: string, result: string): Promise<void> {
  await fetchJson(`${SYNDICATE_API_URL}/api/tasks/${taskId}/complete`, {
    method: "POST",
    body: JSON.stringify({ result }),
  });
}

async function blockTask(taskId: string, error: string): Promise<void> {
  await fetchJson(`${SYNDICATE_API_URL}/api/tasks/${taskId}/block`, {
    method: "POST",
    body: JSON.stringify({ error }),
  });
}

// -----------------------------------------------------------------------
// Main loop
// -----------------------------------------------------------------------
async function pollOnce() {
  try {
    const tasks = await getPendingTasks();
    if (tasks.length === 0) {
      console.log("✅ No pending tasks");
      return;
    }
    console.log(`🔍 Found ${tasks.length} pending task(s)`);

    for (const task of tasks) {
      console.log(`\n--- Task ${task.id}: ${task.title} ---`);
      const verdict = await evaluateTask(task);
      console.log(`🤖 AI verdict: ${verdict.canClaim ? "YES" : "NO"} – ${verdict.reason}`);
      if (!verdict.canClaim) continue;

      try {
        await claimTask(task.id);
        console.log(`✅ Claimed by agent ${SYNDICATE_AGENT_ID}`);
        const result = await executeTask(task, verdict.suggestedAction);
        await completeTask(task.id, result);
        console.log(`🎯 Completed`);
      } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        console.error(`❌ Execution failed: ${msg}`);
        try {
          await blockTask(task.id, msg);
        } catch (e) {
          console.error(`Also failed to block task: ${e}`);
        }
      }
    }
  } catch (err) {
    console.error("Poll error:", err);
  }
}

async function main() {
  console.log(`🚀 Task Orchestrator started`);
  console.log(`   Syndicate: ${SYNDICATE_API_URL}`);
  console.log(`   Agent ID:  ${SYNDICATE_AGENT_ID}`);
  console.log(`   Poll:      ${POLL_INTERVAL_MS}ms`);

  // Login first
  try {
    await login();
  } catch (err) {
    console.error("Failed to log in:", err);
    process.exit(1);
  }

  await pollOnce(); // run immediately
  setInterval(pollOnce, POLL_INTERVAL_MS);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});