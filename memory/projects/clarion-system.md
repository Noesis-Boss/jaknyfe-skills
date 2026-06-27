---
name: clarion-system-project
description: Clarion Intelligence System — full memory architecture installed 2026-05-21
type: project
---

# Clarion Intelligence System

## Overview
Full Clarion Intelligence Systems memory architecture installed 2026-05-21. Dual-layer design with `zobodhi-memory` as complementary fast-query layer.

## Architecture
- **Clarion layer** — structured file hierarchy, taxonomy (daily/projects/feedback/reference), auto context load via Zo rules
- **zobodhi-memory layer** — flat JSON fact cache, fast substring search, synced on key facts from Clarion

## File Structure
```
/home/workspace/
├── USER.md                          ← User profile
├── MEMORY.md                        ← Index of all memory entries
├── memory/
│   ├── SYSTEM_CONFIG.md             ← Don's edit file (owned)
│   ├── daily/YYYY-MM-DD.md          ← Daily conversation notes
│   ├── projects/*.md                ← Project context files
│   ├── feedback/*.md                ← Preferences and corrections
│   └── reference/*.md               ← Reference and system docs
├── scripts/
│   └── memory-search.py             ← Grep-based keyword search
└── Skills/zobodhi-memory/          ← Fast-query JSON cache (complementary)
```

## Two Rules Registered
1. **Context load at conversation start** — read USER.md, MEMORY.md, recent daily file
2. **Active capture + zobodhi-memory sync** — save preferences/projects + sync key facts to zobodhi-memory

## Reference
- Clarion guide: https://www.clarionintelligencesystems.com/resources/memory-system-quick-start
- Article inspiration (zobodhi-memory): https://ai.gopubby.com/i-designed-an-ai-memory-system-using-2-500-year-old-buddhist-psychology-a3ded459262b
- Buddhist concept: Ālaya-vijñāna (storehouse consciousness)

## Status
Active. Next: populate project entries, seed zobodhi-memory with key facts, review pending changes in SYSTEM_CONFIG.md.