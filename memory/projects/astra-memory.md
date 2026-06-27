---
name: astra-memory-project
description: AstraDB unified memory mirror — syncs zobodhi JSON + Clarion markdown into a single Astra collection for cross-source query
type: project
---
# Astra Memory

Unified memory layer backed by DataStax AstraDB.

- **Skill:** `Skills/astra-memory/`
- **CLI:** `bun run Skills/astra-memory/scripts/sync.ts {sync,query,add,status,tail}`
- **Astra collection:** `memories` in keyspace `default_keyspace`
- **Endpoint:** `https://c3904ca0-570a-4b2e-b292-0ca1ffab597a-us-east-2.apps.astra.datastax.com`

## Required env vars (in Settings > Advanced)
- `ASTRA_DB_ENDPOINT`
- `ASTRA_DB_APPLICATION_TOKEN`

## What it does
- Mirrors zobodhi `memory.json` facts → `source=zobodhi, layer=fact`
- Mirrors Clarion `memory/**/*.md` → `source=clarion_*, layer=fact|session|semantic`
- Cross-source lexical search (词 score = occurrences in text)
- Idempotent upsert keyed on `source + text[:200]`

## Token rotation rule
Application tokens MUST stay in env vars only. If Don ever pastes a token in chat, scrub the conversation, revoke the token in Astra portal, generate a new one, and update Settings > Advanced.
