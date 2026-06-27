---
name: memory
description: Durable memory management for AI agents using the four-layer memory model. Ensures instructions, decisions, and context survive compaction and session resets by persisting to files and using retrieval-based recall.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
allowed-tools: Bash
---
# Memory Skill: Durable Agent Memory

## Overview

This skill implements the memory management framework from the OpenClaw Memory Masterclass. It ensures your agent's instructions, preferences, and context survive compaction, pruning, and session resets.

## The Four-Layer Memory Model

| Layer | What it is | Durability |
| --- | --- | --- |
| Bootstrap files (SOUL.md, AGENTS.md, MEMORY.md) | Injected at every session start from disk | Permanent |
| Session transcript (JSONL on disk) | Conversation history rebuilt each turn | Semi-permanent |
| LLM context window | What the model actually sees right now | Temporary |
| Retrieval index (memory_search / QMD) | Searchable index over memory files | Permanent |

## Core Rules

### Rule 1: Persist decisions in files

Before switching tasks, giving complex instructions, or making important decisions, write them to MEMORY.md or a dedicated memory file.

### Rule 2: Check memory flush is enabled

Verify that pre-compaction memory flush is configured with enough buffer to trigger before overflow.

### Rule 3: Make retrieval mandatory

Add this rule to AGENTS.md:

```markdown
## Memory Protocol
- Before answering questions about past work: search memory first
- Before starting any new task: check memory/today's date for active context
- When you learn something important: write it to the appropriate file immediately
- When corrected on a mistake: add the correction as a rule to MEMORY.md
- When a session is ending or context is large: summarize to memory/YYYY-MM-DD.md
```

### Rule 4: Manual saves before major actions

Before task switches or complex instructions, tell the agent:

```markdown
Save this to MEMORY.md
```

## Configuration

### Compaction Settings (add to config)

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 40000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "systemPrompt": "Session nearing compaction. Store durable memories now.",
          "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

### Session Pruning

```json
{
  "contextPruning": {
    "mode": "cache-ttl",
    "ttl": "5m"
  }
}
```

### Hybrid Search

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "local",
        "query": {
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3
          }
        }
      }
    }
  }
}
```

## File Architecture

```markdown
workspace/
├── SOUL.md        # Identity, tone, ethics
├── AGENTS.md      # Workflow rules, tool conventions
├── USER.md        # Who you are, priorities, preferences
├── MEMORY.md      # Decisions, principles, corrections
└── memory/
    └── YYYY-MM-DD.md  # Daily working context
```

## Quick Diagnosis

Run `/context list` to check:

- Is MEMORY.md loading?
- Is anything TRUNCATED?
- Do injected chars equal raw chars?

## Slash Commands

| Command | Purpose |
| --- | --- |
| `/context list` | Shows loaded files, sizes, truncation |
| `/compact [focus]` | Manual compaction, optionally with focus guidance |
| `/new` | Fresh session, clean context |

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Agent forgets preferences | Write to MEMORY.md; check `/context list` |
| memory_search returns nothing | Verify memory files exist; check embedding model |
| Context overflow | `/compact` before adding instructions; raise `reserveTokensFloor` |

## Usage

```bash
# Check context
/openclaw context list

# Manual compaction before new task
/openclaw compact Focus on decisions and active tasks

# Save important decisions
# Tell agent: "Save this to MEMORY.md"
```