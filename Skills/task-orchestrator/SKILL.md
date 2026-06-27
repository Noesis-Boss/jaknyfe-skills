---
name: task-orchestrator
description: Hermes‑based worker that watches Syndicate tasks, evaluates each new task with /zo/ask, claims appropriate ones, and performs the work locally. Use when you want a background agent that picks up tasks from the Syndicate board, decides if they can be automated, and runs them (e.g., calling BankBox APIs, running scripts, generating content). Works across all companies in the Syndicate tenant.
---

# Task Orchestrator

A lightweight worker that runs inside your Zo Computer as a Hermes agent. It:

1. **Polls Syndicate** for tasks that are in `backlog` (or newly created).  
2. **Calls `/zo/ask`** to decide whether the task can be automated and, if so, which tool to use.  
3. **Claims** the task for a designated Syndicate agent (you set the agent ID in the script).  
4. **Executes** the work locally (e.g., runs a command, calls an internal API, posts a tweet, etc.).  
5. **Marks** the task `done` (or `blocked` with an error) and writes an event.

The script is intentionally generic – the actual “work” is defined in the `executeTask` function. By default it logs the action; you can extend it to call BankBox endpoints, generate AI content, etc.

## Requirements

- **Bun** (or Node.js with `node-fetch`).  
- **ZO_API_TOKEN** in the environment – an access token you create in Settings → Access Tokens.  
- The Syndicate API URL (default `https://syndicate-jaknyfe.zocomputer.io`).  
- An existing Syndicate user (e.g., the admin you created) and an **agent ID** that will be used to claim tasks. You can create a dedicated “Task‑Bot” agent in the Syndicate UI.

## Files

- `scripts/task-orchestrator.ts` – the main loop.  
- `README.md` (optional) – additional notes.

## Usage

```bash
# Install dependencies (none required – uses built‑in fetch)
# Run locally with Hermes
hermes run /home/workspace/Skills/task-orchestrator/scripts/task-orchestrator.ts

# Or with Bun directly
bun run /home/workspace/Skills/task-orchestrator/scripts/task-orchestrator.ts
```

Set the `POLL_INTERVAL_MS` environment variable to change the poll frequency (default = 30 seconds).

## How it works (high‑level)

```
+------------------+      +---------------+      +------------------+
| Poll Syndicate   | ---> | /zo/ask eval  | ---> | Claim & Execute  |
| (every N sec)    |      | (AI decides)  |      | (local work)     |
+------------------+      +---------------+      +------------------+
```

## Customizing the work

Edit the `executeTask` function in the script. For example, to call a BankBox endpoint:

```ts
async function executeTask(task: Task) {
  const resp = await fetch("http://localhost:3001/api/goals", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: task.title }),
  });
  if (!resp.ok) throw new Error(`BankBox returned ${resp.status}`);
}
```

## Security

- The script runs with the same OS privileges as the calling process.  
- Keep `ZO_API_TOKEN` secret – store it in **Settings → Access Tokens** and read it from the environment.  
- Only allow trusted agents to claim tasks (set `ALLOWED_AGENT_ID` if needed).