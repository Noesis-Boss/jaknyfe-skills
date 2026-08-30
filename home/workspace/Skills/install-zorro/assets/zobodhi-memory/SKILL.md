---
name: zobodhi-memory
description: |
  A tiny skill that models the "Ālaya‑vijñāna" memory system from the article
  *I Designed an AI Memory System Using 2,500‑Year‑Old Buddhist Psychology.*  
  It stores the most important facts you feed it in a JSON database and lets you query the cache with natural‑language prompts.  
  The design is intentionally lightweight so you can drop it into any project that needs reasoning over a small, semantically‑typed memory.
compatibility: |
  This skill works on any environment that has Node.js (≥18) or Bun runtime.  
  It uses no external packages – just the built‑in `fs/promises` API.
allowed-tools: |
  Bash, ReadFile, CreateOrRewriteFile, EditFileLLM
metadata:
  author: "jaknyfe.zo.computer"
dependencies:
  node: "≥18"
  bun: "≥1.0"
usage: |
  1. **Training** – Add a fact to memory:
        bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --add "Your fact here"
    
  2. **Query** – Retrieve relevant facts:
        bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --query "your question"
    
  3. **List** – Show all stored facts:
        bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --list
    
  4. **Clear** – Reset the memory store:
        bun run /home/workspace/Skills/zobodhi-memory/scripts/memory.ts --clear
    
  The skill creates a file `memory.json` in the skill directory to persist data across chats.
references: |
  - Article: https://ai.gopubby.com/i-designed-an-ai-memory-system-using-2-500-year-old-buddhist-psychology-a3ded459262b
  - Buddhist concept: Ālaya‑vijñāna (storehouse consciousness)
---
