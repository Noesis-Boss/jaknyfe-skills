---
name: ch01-platform-overview-and-data-model
description: "Syndicate platform overview, stack, repo layout, data model, and API surface."
---

# Chapter 1 — Platform Overview & Data Model

## What it is
Multi-tenant agent orchestration platform. Replaces deprecated Paperclip. Each company is an isolated tenant with its own agents, projects, tasks, skills, and memory.

## Stack
- Bun + Hono backend
- React + Vite + Tailwind + shadcn/ui
- SQLite (single file at `data/syndicate.sqlite`)
- Single-process dev mode; production build via `bun run build`

## Run
- Dev: `bun run dev` (do not invoke manually; Zo manages the process)
- Prod: `bun run build` then `bun run prod`
- Type check: `bunx tsc --noEmit`

## Layout
| Path | Role |
|------|------|
| `server.ts` | Hono server + Vite middleware; mounts API routes from `src/lib/routes.ts` |
| `src/lib/db.ts` | SQLite schema + migration (includes Open Work Relay handoff fields) |
| `src/lib/repo.ts` | Typed repository functions (list/get/create/claim/complete/block/handoff) |
| `src/lib/routes.ts` | Hono API route handlers (incl. `/api/tasks/:id/handoff` endpoints) |
| `src/lib/api.ts` | Client-side fetch helpers |
| `src/components/syndicate-shell.tsx` | Sidebar + outlet layout |
| `src/pages/boardroom.tsx` | Global view: all companies + activity feed |
| `src/pages/company-board.tsx` | Single-company surface, 7 tabs |

## Data model
- **companies** — tenant boundary: slug, name, ticker, industry, brand_color, budget_cents
- **projects** — groups of work within a company
- **agents** — workers: role, status, schedule
- **tasks** — work units; kanban status: backlog/ready/running/blocked/done
- **tasks.handoff_state** — 'none' | 'pending' | 'in_progress' | 'completed' | 'failed'
- **tasks.receipts** — JSON array of HandoffReceipt[]
- **tasks.stop_rules** — JSON array of StopRule[] (human-in-the-loop gates)
- **tasks.next_handoff** — task_id to hand to when complete
- **events** — audit log; all actions emit one
- **skills** — company-specific capability definitions
- **memories** — stored notes/facts/decision/context (scoped + weighted)
- **config** — key-value store

Money is stored in cents everywhere; divide by 100 in the display layer.

## API surface
- `GET /api/health`
- `GET|POST /api/companies`, `GET /api/companies/:id`
- `GET /api/companies/:id/board` — full tenant snapshot
- `GET|POST /api/companies/:id/projects|agents|tasks|skills|memory`
- `POST /api/agents/:id/heartbeat`
- `POST /api/tasks/:id/claim|complete|block|handoff|acknowledge-handoff|reject-handoff`
- `PATCH /api/tasks/:id/handoff-state` — Open Work Relay
- `GET /api/memory/search?q=`
- `GET /api/boardroom` — aggregated view
- `GET /api/events?limit=`

## UI
- Boardroom (`/`) — multi-tenant overview with portfolio stats
- CompanyBoard (`/c/:companyId`) — 7 tabs: Board (kanban) / Projects / Agents / Tasks / Skills / Memory / Events
- Each company has a brand accent color reflected in the shell dot and dialog swatches
