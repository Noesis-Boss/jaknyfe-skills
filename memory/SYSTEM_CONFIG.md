# SYSTEM_CONFIG.md — Your Edit File

> **This is the file you own and edit.** All other files in the memory system are maintained by Zo.
> Use the "Your pending changes" section below to request changes — Zo reads this file and applies your requests at the start of every conversation.

---

## What This System Is

This is a **two-layer memory architecture** for Zo Computer:

1. **Clarion layer** (this system) — structured, taxonomy-based, file-based memory with automatic context loading at conversation start. Managed via rules.
2. **zobodhi-memory layer** — a lightweight JSON fact cache for fast substring queries. Complementary tool, not a replacement.

---

## File Inventory

| File / Folder | Who Owns | Purpose |
|---|---|---|
| `USER.md` | You | Your profile — name, role, preferences. Zo reads it every conversation. |
| `MEMORY.md` | Zo | Index of all memory entries. One line per memory file. |
| `memory/SYSTEM_CONFIG.md` | **You** | This file — your edit queue for requesting changes. |
| `memory/jaknyfe-profile.md` | Zo | Your user profile as a structured memory entry. |
| `memory/daily/` | Zo | Daily conversation notes, one file per day. |
| `memory/projects/` | Zo | Ongoing project context — one file per project. |
| `memory/feedback/` | Zo | Preferences, corrections, and feedback you've given Zo. |
| `memory/reference/` | Zo | Reference material and system documentation. |
| `scripts/memory-search.py` | Zo | Search tool — grep-based keyword search across all memory files. |
| `Skills/zobodhi-memory/` | Zo | Separate skill — fast-query JSON cache for quick fact lookups. |

---

## The Two Rules

### Rule 1 — Context Load at Conversation Start
Zo reads `USER.md` and `MEMORY.md` before every conversation. This gives Zo persistent context without you re-explaining yourself.

### Rule 2 — Active Capture + zobodhi-memory Sync
When you share a preference, correct an approach, describe a project, or reference an external system, Zo:
1. Creates or updates the appropriate `memory/feedback/` or `memory/projects/` file
2. Syncs the key fact to `Skills/zobodhi-memory/` as a parallel fast-query entry

Additionally: before a conversation ends or when you go quiet after significant work, Zo will ask: **"Want me to save a note on this?"**

---

## The Two-Layer Design

```
┌──────────────────────────────────────────────┐
│  Clarion Layer (this system)                │
│  • Structured file hierarchy                 │
│  • Taxonomy: daily / projects / feedback / ref│
│  • Auto context load via rules              │
│  • Full session summaries                    │
│  • Frontmatter metadata                     │
│  • Searchable via memory-search.py          │
└────────────────────┬─────────────────────────┘
                     │ sync on key facts
┌────────────────────▼─────────────────────────┐
│  zobodhi-memory Layer (Skills/zobodhi-memory/)│
│  • Flat JSON fact cache                      │
│  • Substring search — fast, no overhead     │
│  • Use for quick lookups and cross-project  │
│    fact retrieval                            │
│  • NOT the primary system — supplement only  │
└──────────────────────────────────────────────┘
```

**When to use which layer:**
- Need context at session start → Clarion (automatic, via rules)
- Want to remember a preference → Clarion + zobodhi-memory sync
- Quick fact lookup mid-session → `memory.ts --query "keyword"`
- Long-term project history → Clarion `memory/projects/`
- Structured session summary → Clarion `memory/daily/`
- Want to see everything remembered → `memory.ts --list`

---

## Your Pending Changes

<!-- Edit below this line. Write what you want changed in plain English. -->
<!-- Zo will read this section at the start of every conversation and apply your requests. -->

*No pending changes yet.*