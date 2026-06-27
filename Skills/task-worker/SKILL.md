---
name: task-worker
description: Executes running tasks in Syndicate by interpreting task descriptions with Hermes + /zo/ask and updating results. Polls all companies for running tasks.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Task Worker

Executes work assigned to Syndicate agents.

## How it works

1. Polls Syndicate every 10s for `running` tasks across all companies
2. For each running task, sends the task description to `/zo/ask` for interpretation + execution
3. Captures the result/error from the AI response
4. Updates the task via `PATCH /api/tasks/:id` with final status + result
5. Marks task `done` on success, `blocked` on failure

## Usage

```bash
bun run /home/workspace/Skills/task-worker/scripts/task-worker.ts
```

Runs indefinitely. Stop with Ctrl+C.

## Configuration

- `POLL_INTERVAL_MS`: Milliseconds between polls (default: 10000)
- `EXECUTION_TIMEOUT_MS`: Max time to wait for task execution (default: 60000)
- `MAX_RETRIES`: Max retries on transient failures (default: 3)
- Retries Zo execution on 429 contention and limits the worker to one in-flight task at a time to avoid concurrent `/zo/ask` overload.
