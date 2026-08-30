#!/usr/bin/env bun
/**
 * Task Worker — polls Syndicate for running tasks, executes them via /zo/ask
 * 
 * Usage:
 *   bun run task-worker.ts              Run the worker
 *   bun run task-worker.ts --help       Show this help
 */


// Check for --help flag before initializing
if (process.argv.includes("--help") || process.argv.includes("-h")) {
  console.log(`
Task Worker — execute Syndicate tasks via /zo/ask

USAGE:
  bun run task-worker.ts [OPTIONS]

OPTIONS:
  -h, --help          Show this help message
  --once                Run single poll, then exit (for testing)

ENVIRONMENT VARIABLES:
  SYNDICATE_API_URL       Syndicate API base URL (default: https://syndicate-jaknyfe.zocomputer.io)
  POLL_INTERVAL_MS        Poll interval in milliseconds (default: 5000)
  ZO_CLIENT_IDENTITY_TOKEN  Zo API identity token (required)
  WORKER_EMAIL            Login email (default: worker@test.local)
  WORKER_PASSWORD         Login password (default: password123)

DESCRIPTION:
  Polls Syndicate for running tasks, claims them for suitable agents,
  executes via /zo/ask, and updates task status.

  Default: runs continuously until killed (Ctrl+C).
  --once: single poll cycle for testing.
`);
  process.exit(0);
}

const RUN_ONCE = process.argv.includes("--once");
const API_BASE = process.env.SYNDICATE_API_URL ?? "https://syndicate-jaknyfe.zocomputer.io";
const ZO_API = "https://api.zo.computer/zo/ask";
const POLL_INTERVAL_MS = parseInt(process.env.POLL_INTERVAL_MS || "5000", 10);
const MAX_WORKER_INFLIGHT = 1;
const ZO_RETRY_ATTEMPTS = 5;
const ZO_RETRY_BASE_DELAY_MS = 15000;

// Auth credentials
const WORKER_EMAIL = process.env.WORKER_EMAIL || "worker@test.local";
const WORKER_PASSWORD = process.env.WORKER_PASSWORD || "password123";
let sessionCookie: string | null = null;
let authToken: string | null = null;

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function authHeaders(): Record<string, string> {
  const headers: Record<string, string> = {};
  if (sessionCookie) headers["Cookie"] = sessionCookie;
  if (authToken) headers["Authorization"] = `Bearer ${authToken}`;
  return headers;
}

function zoApiAuthHeader(): string {
  const token = process.env.ZO_CLIENT_IDENTITY_TOKEN ?? process.env.ZO_ACCESS_TOKEN;
  if (!token) {
    throw new Error("ZO_CLIENT_IDENTITY_TOKEN is required");
  }
  return token;
}

async function ensureAuth(): Promise<void> {
  if (sessionCookie && authToken) return;
  console.log("Authenticating task worker...");
  const loginResp = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ email: WORKER_EMAIL, password: WORKER_PASSWORD }),
  });
  if (!loginResp.ok) throw new Error(`Login failed: ${await loginResp.text()}`);
  const data = await loginResp.json().catch(() => ({} as any));
  const setCookie = loginResp.headers.get("set-cookie");
  if (setCookie) sessionCookie = setCookie.split(";")[0];
  if (data?.token) authToken = data.token;
  console.log("Worker authenticated");
}

interface Task {
  id: string; company_id: string; title: string; description: string | null;
  status: string; priority: number; agent_id: string | null; project_id: string | null;
  handoff_state?: "none" | "pending" | "in_progress" | "completed" | "failed";
  next_handoff?: string | null;
  stop_rules?: string | null;
}

interface Agent {
  id: string; name: string; role: string; instructions: string | null; status: string;
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
    ...authHeaders(),
    ...(init?.headers as Record<string, string> | undefined),
  };
  const response = await fetch(url, { ...init, headers });
  const text = await response.text();
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${text.slice(0, 500)}`);
  if (!text.trim()) return {} as T;
  try {
    return JSON.parse(text) as T;
  } catch {
    throw new Error(`Invalid JSON from ${url}: ${text.slice(0, 500)}`);
  }
}

async function fetchReadyTasks(): Promise<Task[]> {
  const companies = await fetchJson<{ companies: { id: string }[] }>(`${API_BASE}/api/companies`);
  const allTasks: Task[] = [];
  for (const co of companies.companies || []) {
    const data = await fetchJson<{ tasks: Task[] }>(`${API_BASE}/api/companies/${co.id}/tasks?status=ready`);
    allTasks.push(...(data.tasks || []));
  }
  return allTasks;
}

async function fetchRunningTasks(): Promise<Task[]> {
  const companies = await fetchJson<{ companies: { id: string }[] }>(`${API_BASE}/api/companies`);
  const allTasks: Task[] = [];
  for (const co of companies.companies || []) {
    const data = await fetchJson<{ tasks: Task[] }>(`${API_BASE}/api/companies/${co.id}/tasks?status=running`);
    allTasks.push(...(data.tasks || []));
  }
  return allTasks;
}

async function fetchAgents(companyId: string): Promise<Agent[]> {
  const data = await fetchJson<{ agents: Agent[] }>(`${API_BASE}/api/companies/${companyId}/agents`);
  return data.agents || [];
}

async function claimTask(taskId: string, agentId: string): Promise<boolean> {
  const response = await fetch(`${API_BASE}/api/tasks/${taskId}/claim`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json", ...authHeaders() },
    body: JSON.stringify({ agent_id: agentId }),
  });
  return response.ok;
}

async function validateTaskForAgent(task: Task, agent: Agent): Promise<boolean> {
  const text = `${task.title} ${task.description || ""}`.toLowerCase();
  if (agent.role === "ceo") {
    if (text.includes("debug") || text.includes("code") || text.includes("deploy")) return false;
  }
  if (agent.role === "cto") {
    if (text.includes("marketing") || text.includes("sales") || text.includes("customer")) return false;
  }
  if (agent.role === "engineer") {
    if (text.includes("strategy") || text.includes("executive") || text.includes("board meeting")) return false;
  }
  return true;
}

async function executeTaskViaZo(task: Task, agent: Agent | null): Promise<string> {
  const instructions = agent?.instructions ? `\n\n**Agent Instructions:**\n${agent.instructions}` : "";
  const prompt = `Execute this task as a ${agent?.role || "worker"}:\n\n**Title:** ${task.title}\n**Description:** ${task.description || "No description"}\n**Priority:** ${task.priority}\n${instructions}\n\nReport what you did.`;

  const response = await fetch(ZO_API, {
    method: "POST",
    headers: { "Authorization": zoApiAuthHeader(), "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ input: prompt }),
  });
  const text = await response.text();
  if (!response.ok) throw new Error(`Zo ask failed (${response.status}): ${text.slice(0, 500)}`);
  try {
    const d = JSON.parse(text);
    return d.output || text || "No output";
  } catch {
    return text || "No output";
  }
}

async function executeTaskViaZoWithRetry(task: Task, agent: Agent | null): Promise<string> {
  let lastError: unknown;
  for (let attempt = 1; attempt <= ZO_RETRY_ATTEMPTS; attempt++) {
    try {
      return await executeTaskViaZo(task, agent);
    } catch (error) {
      lastError = error;
      const message = error instanceof Error ? error.message : String(error);
      const retryable = message.includes("429") || message.includes("Only 5 concurrent /zo/ask request(s) are allowed");
      if (!retryable || attempt === ZO_RETRY_ATTEMPTS) break;
      const delay = ZO_RETRY_BASE_DELAY_MS * attempt;
      console.warn(`[${task.id}] Zo busy, retrying in ${Math.round(delay / 1000)}s (attempt ${attempt + 1}/${ZO_RETRY_ATTEMPTS})`);
      await sleep(delay);
    }
  }
  throw lastError instanceof Error ? lastError : new Error(String(lastError ?? "Zo execution failed"));
}

async function fetchFullTask(taskId: string): Promise<Task | undefined> {
  const data = await fetchJson<{ task: Task }>(`${API_BASE}/api/tasks/${taskId}`).catch(() => ({}));
  return data.task;
}

async function acknowledgeHandoff(taskId: string, dataPayload?: Record<string, unknown>): Promise<void> {
  const response = await fetch(`${API_BASE}/api/tasks/${taskId}/acknowledge-handoff`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ data_payload: dataPayload || {} }),
  });
  if (!response.ok) console.error(`[${taskId}] Acknowledge handoff failed: ${await response.text()}`);
}

async function rejectHandoff(taskId: string, reason: string): Promise<void> {
  const response = await fetch(`${API_BASE}/api/tasks/${taskId}/reject-handoff`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ reason }),
  });
  if (!response.ok) console.error(`[${taskId}] Reject handoff failed: ${await response.text()}`);
}

async function completeTask(taskId: string, companyId: string, result: string, task?: Task): Promise<void> {
  const response = await fetch(`${API_BASE}/api/tasks/${taskId}/complete`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ result }),
  });
  if (!response.ok) {
    console.error(`[${taskId}] Complete failed: ${await response.text()}`);
    return;
  }
  // After completion, check if handoff is needed
  if (task?.handoff_state === "pending" && task?.next_handoff) {
    const stopRules = task.stop_rules ? JSON.parse(task.stop_rules) : [];
    // Only auto-acknowledge if no human_approval stop rules are present
    const hasHumanApproval = stopRules.some((rule: any) => rule.condition === "human_approval");
    if (!hasHumanApproval) {
      await acknowledgeHandoff(taskId, { result });
      console.log(`[${taskId}] Handoff acknowledged to ${task.next_handoff}`);
    } else {
      console.log(`[${taskId}] Handoff pending human approval, not auto-acknowledged`);
    }
  }
}

async function blockTask(taskId: string, companyId: string, error: string): Promise<void> {
  const response = await fetch(`${API_BASE}/api/tasks/${taskId}/block`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ error }),
  });
  if (!response.ok) console.error(`[${taskId}] Block failed: ${await response.text()}`);
}

const inFlight = new Map<string, Promise<string>>();

async function main(): Promise<void> {
  console.log(`Task Worker started`);
  console.log(`Poll interval: ${POLL_INTERVAL_MS}ms`);
  console.log(`Syndicate API: ${API_BASE}`);
  if (RUN_ONCE) console.log(`Mode: --once (will exit after single poll)`);
  
  await ensureAuth();

  while (true) {
    try {
      // Process in-flight tasks first (await their results)
      for (const [taskId, promise] of Array.from(inFlight.entries())) {
        try {
          const result = await promise;
          const fullTask = await fetchFullTask(taskId);
          await completeTask(taskId, "", result, fullTask);
          console.log(`[${taskId}] Completed`);
        } catch (err: any) {
          await blockTask(taskId, "", err.message);
          console.error(`[${taskId}] Blocked: ${err.message}`);
        }
        inFlight.delete(taskId);
      }

      if (inFlight.size < MAX_WORKER_INFLIGHT) {
        // Process running tasks (already claimed, waiting for execution)
        const runningTasks = await fetchRunningTasks();
        for (const task of runningTasks) {
          if (inFlight.size >= MAX_WORKER_INFLIGHT) break;
          if (inFlight.has(task.id)) continue;
          
          const agents = await fetchAgents(task.company_id);
          const agent = task.agent_id ? agents.find(a => a.id === task.agent_id) ?? null : null;
          
          if (!agent) {
            console.log(`[${task.id}] No agent found, skipping`);
            continue;
          }

          console.log(`[${task.id}] Executing: ${task.title} (${agent.role})`);
          inFlight.set(task.id, executeTaskViaZoWithRetry(task, agent));
        }

        // Claim ready tasks
        const readyTasks = await fetchReadyTasks();
        for (const task of readyTasks) {
          if (inFlight.size >= MAX_WORKER_INFLIGHT) break;
          const agents = await fetchAgents(task.company_id);
          const agent = agents.find(a => a.role === "engineer" || a.role === "cto") ?? null;
          
          if (!agent) {
            console.log(`[${task.id}] No engineer/cto found, skipping`);
            continue;
          }

          const valid = await validateTaskForAgent(task, agent);
          if (!valid) {
            console.log(`[${task.id}] Blocked: incompatible with ${agent.role}`);
            inFlight.set(task.id, Promise.reject(new Error(`Task blocked: incompatible with ${agent.role}`)));
            continue;
          }

          const claimed = await claimTask(task.id, agent.id);
          if (claimed) {
            console.log(`[${task.id}] Claimed by ${agent.role}`);
            inFlight.set(task.id, executeTaskViaZoWithRetry(task, agent));
          }
        }
      }
    } catch (err: any) {
      console.error("Worker error:", err.message);
    }
    
    // Exit after single poll if --once mode
    if (RUN_ONCE) {
      console.log("Single poll complete, exiting (--once mode)");
      return;
    }
    
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
  }
}

main().catch(err => {
  console.error("Fatal worker error:", err);
  process.exit(1);
});