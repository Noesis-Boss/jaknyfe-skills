---
name: zobodhi-memory-usage
description: How to use zobodhi-memory as the complementary fast-query layer
type: feedback
---

# zobodhi-memory Usage Guide

## Purpose
`zobodhi-memory` is a fast-query cache layered on top of the Clarion memory system. It is **not** a replacement for Clarion's structured approach. Use it for quick lookups that don't need full context.

## Commands

### Add a fact
```bash
bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --add "Your fact here"
```

### Query for a fact
```bash
bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --query "keyword"
```

### List all facts
```bash
bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --list
```

### Clear all facts
```bash
bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --clear
```

## When to Add Facts

- When Clarion captures a key preference or project fact, **also sync it to zobodhi-memory** via `--add`
- Use `--add` for any fact you want fast cross-session retrieval without navigating folder structure
- The `--query` command searches by substring match — no semantic understanding

## Sync Rules
When Rule 2 (active capture) fires, Zo should:
1. Write the memory file to the appropriate `memory/feedback/` or `memory/projects/` folder
2. Run `memory.ts --add` with the key fact text to keep the fast-query cache in sync

## Limitations
- Substring match only — not semantic search
- No metadata beyond `id`, `text`, `addedAt`, `tags`
- No update mechanism — only add and clear
- For structured project history, use Clarion's `memory/projects/` files instead

## Why
Fast. No folder navigation. Works in seconds. Good for quick cross-project lookups during active debugging sessions.