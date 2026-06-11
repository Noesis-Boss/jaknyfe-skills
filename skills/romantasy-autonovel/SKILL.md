---
name: romantasy-autonovel
description: Generate a Romantasy novel draft using the Enemies‑to‑Lovers + forced‑proximity outline stored in memory. Provides commands to create character sheets, chapter outlines, and full‑text scaffolding.
---

## Usage
- `npm run generate:characters` – pulls the character concept from memory and writes `characters.md`.
- `npm run generate:outline` – builds the three‑act outline (uses the saved outline.md) and writes `full-outline.md`.
- `npm run generate:draft` – combines characters and outline into a starter manuscript `draft.md`.

## Scripts
The skill ships a small TypeScript CLI (`scripts/main.ts`). Run it with `bun run scripts/main.ts <action>` where `<action>` is one of `characters`, `outline`, or `draft`.

## Dependencies
- `bun` (runtime already available).
- No external packages; uses Node’s `fs` and the Zobodhi memory tool via a shell command.

## Example
```bash
cd $(pwd)/Skills/romantasy-autonovel
bun run scripts/main.ts draft
# produces draft.md in the same folder
```

Feel free to extend the skill with more actions (e.g., scene‑by‑scene expansion, export to PDF, etc.).

## New Action: generate novel
- `bun run scripts/generate_novel.ts` – reads the full outline and expands each chapter into a PG‑13 romantic fantasy narrative (≈90 000 words). The output is written to `novel.md`.
