---
name: memory-system-architecture
description: Clarion memory system layout, frontmatter schema, rules, and dual-layer design
type: reference
---

# Clarion Memory System — Architecture Reference

## System Overview

Two-layer architecture:
1. **Clarion** — primary structured layer (files, taxonomy, rules, auto context load)
2. **zobodhi-memory** — complementary fast-query layer (flat JSON, substring search)

## File Layout

```
/home/workspace/
├── USER.md                          ← User profile (owned by Don)
├── MEMORY.md                        ← Index (maintained by Zo)
├── memory/
│   ├── SYSTEM_CONFIG.md             ← Don's edit file (owned)
│   ├── jaknyfe-profile.md           ← User profile as memory entry
│   ├── daily/YYYY-MM-DD.md          ← Daily conversation notes
│   ├── projects/*.md                ← Project context
│   ├── feedback/*.md                ← Preferences, corrections
│   └── reference/*.md               ← Reference docs
└── scripts/
    └── memory-search.py             ← Grep keyword search
```

## Frontmatter Schema

Every memory file starts with:

```yaml
---
name: slug-identifier           # lowercase, no spaces
description: One clear sentence # what this memory covers
type: user|project|feedback|daily|reference
---
```

## Folder Types

| Folder | Type | Contents |
|--------|------|----------|
| `memory/daily/` | daily | Dated session summaries |
| `memory/projects/` | project | Ongoing project context |
| `memory/feedback/` | feedback | Preferences, corrections |
| `memory/reference/` | reference | System docs, references |

## Rules

### Rule 1 — Context Load (Conversation Start)
At the start of every conversation, Zo reads:
1. `USER.md` → Who is this person?
2. `MEMORY.md` → What do I already know?
3. Most recent `memory/daily/` file → What did we talk about recently?

### Rule 2 — Active Capture (During Conversation)
Zo saves automatically when you:
- Share a new preference
- Correct an approach
- Describe an ongoing project
- Reference an external system

Then: offer to save a session note if significant work happened: "Want me to save a note on this?"

On key facts: also sync to zobodhi-memory via `--add`.

## SYSTEM_CONFIG.md Usage

Don edits the "Your pending changes" section. Zo reads it at conversation start and applies changes. Plain English, no formatting required.

## Modifying the System

Add a new folder type → edit SYSTEM_CONFIG.md → "Your pending changes"
Change how Zo responds → edit SYSTEM_CONFIG.md → "Your pending changes"
Search past memories → ask Zo: "what did we discuss about [topic]?"
See all memories → ask Zo: "show me all my memory entries"

## Search

- Clarion: `scripts/memory-search.py <keywords>` — grep across all memory files
- zobodhi-memory: `memory.ts --query "keyword"` — substring match on flat JSON list
- Both are grep-based; Clarion covers structured files, zobodhi-memory covers quick facts

## Reference Sources

- Guide: https://www.clarionintelligencesystems.com/resources/memory-system-quick-start
- zobodhi-memory article: https://ai.gopubby.com/i-designed-an-ai-memory-system-using-2-500-year-old-buddhist-psychology-a3ded459262b
- Buddhist concept: Ālaya-vijñāna (storehouse consciousness)