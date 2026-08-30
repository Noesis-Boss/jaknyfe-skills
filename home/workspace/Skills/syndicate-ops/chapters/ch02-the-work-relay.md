---
name: ch02-the-work-relay
description: "The Work Relay concept, seven-part task record, state machine, and human-in-the-loop model."
---

# Chapter 2 — The Work Relay & Seven-Part Task Record

## Core concept
Syndicate moves AI from **Prompt Mode** (asking for answers) to **Work Mode** (executing jobs with state and evidence). Instead of chat logs, the platform manages a **ledger of Tasks**, so work moving across AI agents, queues, and people never loses its source, limits, or status.

## The Seven-Part Task Record
Every unit of work follows a strict schema:
1. **Outcome** — the measurable goal
2. **Owner** — the current actor (Agent or Human)
3. **Source Material** — the grounding data (pitch decks, ICPs, transcripts)
4. **Context** — the reasoning chain and decisions made so far
5. **Allowed Actions** — strict boundaries on agent capabilities
6. **Stop Rules** — conditions that trigger a human gate (e.g., "Stop before sending")
7. **Receipt** — proof of completion and evidence

## State machine
Tasks move through a transparent lifecycle:
`ready → claimed → working → needs-input → review → done`

## Human-in-the-loop (HITL)
The platform enforces **Stop Rules**. When an agent reaches a critical milestone, the task moves to `review` status, pausing execution until a human partner approves the receipt.

## Technical architecture
- **Protocol** — defined in `AGENTS.md` (the System Operating Manual)
- **Persistence** — SQLite-backed task ledger for durable state
- **Orchestration** — `relay_engine.ts` manages handoffs and state transitions
- **Interface** — Boardroom view across companies; per-company boards for Projects, Agents, and Tasks
