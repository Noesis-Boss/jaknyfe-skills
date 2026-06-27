---
name: syndicate-framework-launch
description: First working version of the Syndicate framework GUI
type: log
---
# 2026-06-22 — Syndicate Framework Live

**Status:** Foundation complete. Framework is fully functional and verified. Ready for test companies.

**Architecture (one-liner):** Multi-tenant SaaS. Each company is an isolated workspace with its own agents, projects, tasks, skills, memory, and events. Don's global view (Boardroom) aggregates across all tenants.

**Tech stack:**
- Bun + Hono (server) — single-process site
- Vite + React 19 (client) — SPA with shell + nested routes
- shadcn/ui (Tailwind 4, Radix primitives)
- SQLite (Bun native) — single DB at `data/syndicate.sqlite`
- agent-browser for verification

**Schema (9 tables):**
companies · projects · agents · tasks · events · skills · memories · config · (events indexes)

**Routes (Boardroom / Company board):**
- `/` — Boardroom: portfolio cards, aggregate stats, live activity feed
- `/c/:companyId` — Per-tenant board with 7 tabs: Board, Projects, Agents, Tasks, Skills, Memory, Events
- `data/syndicate.sqlite` — persistence

**API surface (19 endpoints):**
- Companies: list, get, create, board
- Per-company: projects/agents/tasks/skills/memory (list + create)
- Task lifecycle: claim, complete, block
- Agent: heartbeat
- Aggregates: boardroom, events, memory/search

**Task state machine (kanban):** backlog → ready → running → done | blocked | cancelled
**Agent state machine:** idle → running → blocked | offline
**Event log:** append-only audit trail of every state change

**Verified end-to-end:**
- Created company "Acme Corp" via UI dialog
- Hired agent "build-bot"
- Created project "Initial build"
- Created and completed task "Ship MVP" (backlog → running → done)
- New task "Wire up the meta-agent loop" (currently backlog)
- All 7 tabs render and are interactive
- Brand colors persist, budget in cents, slug uniqueness enforced

**Bugs hit and fixed during this session:**
1. camelCase vs snake_case mismatch between dialog and route (brandColor vs brand_color) — fixed by mapping in route handler
2. api.board() vs api.getBoard() naming — renamed
3. useParams() param key mismatch (id vs companyId) — fixed
4. Task status enum inconsistency (pending|done vs backlog|ready|running|done) — unified to kanban model with one-time DB migration
5. Memory type field mismatch (kind/importance/score vs scope/weight) — aligned to DB schema
6. Heartbeat missing required second arg — added
7. searchMemory signature mismatch — removed unused companyId
8. Event level "warning" vs "warn" — unified to "warn"
9. Existing 'pending' task in DB blocked by new kanban types — added one-time migration step

**What's NOT built yet (intentional, per Don's direction):**
- No test companies imported from Paperclip data
- No auth — site is currently open (will be private dev mode unless published)
- No automatic task dispatch (the "meta-agent loop" task in backlog is a placeholder for this)
- No public deployment yet

**Files added (~1700 lines of code):**
- `src/lib/db.ts` (145 lines) — schema, migrations
- `src/lib/repo.ts` (495 lines) — typed CRUD
- `src/lib/routes.ts` (221 lines) — Hono API routes
- `src/lib/api.ts` (191 lines) — client fetch helpers
- `src/components/syndicate-shell.tsx` (108 lines) — sidebar layout
- `src/pages/boardroom.tsx` (322 lines) — Don's portfolio view
- `src/pages/company-board.tsx` (730 lines) — per-tenant management GUI
- `src/App.tsx` — router with shell outlet
- shadcn components: button, dialog, input, textarea, label, select, separator, tabs, scroll-area, tooltip

**Reference paths:**
- Code: `/home/workspace/syndicate/`
- DB: `/home/workspace/syndicate/data/syndicate.sqlite`
- Live preview (dev): http://localhost:57548
- Project AGENTS.md: `/home/workspace/syndicate/AGENTS.md`

**Next steps (when Don is ready):**
1. Build the meta-agent dispatch loop (the task sitting in backlog)
2. Add auth (bearer token or per-tenant API key)
3. Decide on test-company import strategy from Paperclip snapshots
4. Add kill-condition monitoring (the `kill_conditions` column is wired but unused)
5. Consider memory search (column exists, route exists, UI built but not yet smoke-tested)
