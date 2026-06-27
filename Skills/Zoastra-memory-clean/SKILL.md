---
name: astra-memory
compatibility: Created for Zo Computer
description: Sync and query the unified memory layer backed by DataStax AstraDB. Mirrors facts from zobodhi-memory (Skills/zobodhi-memory/memory.json) and Clarion markdown tree (memory/**) into the AstraDB `memories` collection with local nomic-embed-text-v1.5 embeddings, then queries via hybrid semantic+lexical RRF. Use when the user wants to sync memory to AstraDB, query unified memories, check sync status, add a fact, or run semantic search. Requires ASTRA_DB_ENDPOINT and ASTRA_DB_APPLICATION_TOKEN in env (Settings > Advanced).
metadata:
  author: Noesis-Boss (aka Jaknyfe)
---
# AstraDB Memory

Unified memory layer that mirrors both the zobodhi JSON fact store and the Clarion markdown tree into a single AstraDB collection with local embeddings, then queries across both via hybrid semantic + lexical retrieval.

## Requirements

Set in [Settings > Advanced](/?t=settings&s=advanced) → Secrets:

- `ASTRA_DB_ENDPOINT` — e.g. `https://<dbid>-<region>.apps.astra.datastax.com`
- `ASTRA_DB_APPLICATION_TOKEN` — generated in Astra portal; needs Database read/write

`ASTRA_DB_KEYSPACE` is optional (defaults to `default_keyspace`).

Optional overrides:

- `ASTRA_VECTOR_DIM` — collection vector dimension (default `768`, matches nomic-embed-text-v1.5 full output)
- `ASTRA_VECTOR_SIM` — similarity metric (`cosine`, `dot_product`, `euclidean`; default `cosine`)
- `MATRYOSHKA_DIM` — truncate nomic embeddings to 64/128/256/512/768 before L2-norm (default `768` = full)
- `HF_HOME` — Hugging Face model cache (default `/home/.z/hf-cache`)

> **Token safety:** Application tokens are sensitive. Never paste them in chat. Store them as env vars in Settings > Advanced so they stay out of conversation history. Rotate quarterly and after any team-member change.

## First-time setup

```bash
cd scripts
bun run setup.ts                  # create collection (768-dim, cosine) — idempotent
bun run setup.ts --recreate       # drop + recreate (use after changing ASTRA_VECTOR_DIM)
bun run sync.ts sync              # ingest all sources with embeddings
```

## Usage

```bash
cd scripts

# Sync
bun run sync.ts sync                     # full sync (both sources)
bun run sync.ts sync --source=zobodhi    # one source only
bun run sync.ts sync --source=clarion

# Status / query
bun run sync.ts status                   # counts by source/layer + last sync
bun run sync.ts query <text>             # hybrid semantic+lexical RRF
bun run sync.ts query paperclip --source=clarion
bun run sync.ts query <text> --limit=20  # override result count

# Write
bun run sync.ts add "New fact to remember"
bun run sync.ts tail 10                  # most recent N

# Embedding tool (low-level)
bun run embed.ts info                    # show model/dim/warmup
bun run embed.ts embed-query "search text"
bun run embed.ts embed-doc "memory text"
```

## How search works

Hybrid retrieval fuses two signals via Reciprocal Rank Fusion (RRF, k=60):

1. **Semantic** — embed query with `search_query:` prefix, run Astra `$vector` ANN against the `memories` collection. Nomic-embed-text-v1.5 produces 768-dim L2-normalized vectors.
2. **Lexical** — substring scoring against `text` and `title` over the full corpus (title hits weight 10x).

Both ranked lists merge into a single RRF score. A doc only needs to win one signal to surface.

## Embedding model

`nomic-ai/nomic-embed-text-v1.5` runs locally via `@huggingface/transformers` v3 (ONNX Runtime WebAssembly). ~270MB quantized, cached at `/home/.z/hf-cache`. First-call warmup is ~1s; subsequent embeds are sub-second per chunk.

Required prefixes per the model spec:

- Queries: `search_query: <text>`
- Documents: `search_document: <text>`

These are added automatically by `embed.ts` and `sync.ts`. Don't strip them or the embedding quality degrades significantly.

## Schema (collection `memories`)

| field | type | notes |
| --- | --- | --- |
| `_id` | string | auto-generated UUID |
| `$vector` | number[] | 768-dim L2-normalized nomic embedding |
| `source` | string | `zobodhi` / `clarion_daily` / `clarion_project` / `clarion_feedback` / `clarion_reference` / `clarion_topics` / `clarion_bootstrap` |
| `layer` | string | `fact` / `session` / `semantic` (Clarion's 3-layer model) |
| `text` | string | full document text |
| `title` | string | short title (first heading or fact preview) |
| `path` | string | absolute path to source file |
| `timestamp` | string | ISO 8601 |
| `tags` | string[] | from frontmatter or `[]` |
| `project` | string | e.g. `scottish-rite`, `kilo-ui`, `paperclip`, `daily` |

## Sync behavior

- **Idempotent upserts** keyed on `source + first 200 chars of text`. Re-running sync adds nothing new.
- **File system is source of truth.** Astra is a mirror for unified search.
- **Local zobodhi writes are mirrored to Astra** automatically on `add`, with embedding.
- **No automatic sync on file edit** — run `bun run sync.ts sync` after editing markdown in `memory/**` to keep Astra in step.

## Hooking into chat

To auto-mirror incoming chat messages to Astra, add a custom rule in [Settings > AI > Rules](/?t=settings&s=ai&d=rules):

> When a chat message arrives, run `bun run scripts/sync.ts add "{{event.message.text}}"` if the message contains a fact, preference, decision, or non-trivial context.

## Rotation

If the application token is ever exposed (in chat, in a screenshot, in a public repo):

1. Go to Astra portal → Database → Connect → Application Tokens
2. Revoke the old token
3. Generate a new one
4. Update `ASTRA_DB_APPLICATION_TOKEN` in [Settings > Advanced](/?t=settings&s=advanced)
5. Re-run `bun run sync.ts status` to confirm connectivity

## Files

- `file scripts/sync.ts` — CLI for sync, query, add, tail, status
- `file scripts/embed.ts` — local nomic-embed-text-v1.5 wrapper (info / embed-query / embed-doc)
- `file scripts/setup.ts` — create / recreate collection at the right vector dim
- `file scripts/last-sync.json` — last sync timestamp + counts (regenerated on every sync)