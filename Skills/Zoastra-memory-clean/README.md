# astra-memory

A hybrid semantic + lexical memory layer for AI agents, backed by **DataStax Astra DB Serverless** with **local** [`nomic-embed-text-v1.5`](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) embeddings.

No external embedding API. No vector-database托管费. Everything runs on your own machine; only storage and queries hit Astra.

## What it does

- **Mirror your memory files** (markdown tree + JSON fact store) into a single Astra collection
- **Generate embeddings locally** via ONNX Runtime + transformers.js — no API costs
- **Search via hybrid RRF** — semantic (vector ANN) + lexical (substring) fused with reciprocal rank fusion
- **Recover from misspellings & natural-language queries** that pure substring search can't

## Quick start

```bash
# Install Bun if you don't have it: https://bun.sh
curl -fsSL https://bun.sh/install | bash

# Install deps
bun install

# Set Astra creds (don't commit these!)
export ASTRA_DB_ENDPOINT="https://<dbid>-<region>.apps.astra.datastax.com"
export ASTRA_DB_APPLICATION_TOKEN="<your-token>"

# Optional — point at your own memory location
export ZOBODHI_JSON="memory/zobodhi.json"   # default
export CLARION_ROOT="memory"                 # default

# Create collection (768-dim, cosine) — idempotent
bun run scripts/setup.ts

# Ingest sources
bun run scripts/sync.ts sync

# Query
bun run scripts/sync.ts query "what did we decide about pricing"
bun run scripts/sync.ts query "scottsh rite" --limit=5   # typo absorbed semantically
bun run scripts/sync.ts query "deploy" --source=project --json
```

## Architecture

```
┌─────────────┐      ┌──────────────┐
│ memory/    │──────▶│  sync.ts     │── embed locally ──┐
│ (markdown) │       │              │                    │
└─────────────┘       │              │                    ▼
┌─────────────┐       │              │          ┌────────────────────┐
│ memory.json │──────▶│              │─────────▶│ Astra collection  │
│ (zobodhi)   │       └──────┬───────┘          │ `memories`        │
└─────────────┘              │                  │ - 768-dim vectors  │
                             ▼                  │ - cosine ANN      │
                      ┌──────────────┐          │ - hybrid RRF query │
                      │ embed.ts     │          └─────────┬──────────┘
                      │ (nomic v1.5) │                    │
                      └──────────────┘                    │
                                                        ▼
                                              query "what was X?"
```

### Retrieval

Each query runs two ranked lists, fused via Reciprocal Rank Fusion (k=60):

| Signal | Method | Strengths |
|---|---|---|
| **Semantic** | nomic-embed-text-v1.5 + Astra `$vector` ANN | Misspellings, paraphrase, natural language |
| **Lexical** | substring match with title boost | Exact terms, IDs, code symbols |

A doc only needs to win one signal to surface.

## Source format

### Markdown tree (Clarion-style)

```
memory/
├── projects/
│   └── my-project.md      # source: clarion_project, project: my-project
├── daily/
│   └── 2026-06-27.md       # source: clarion_daily,    project: daily
├── feedback/
│   └── rule-correction.md  # source: clarion_feedback
└── reference/
    └── schema.md           # source: clarion_reference
```

Each file can have frontmatter:

```yaml
---
name: my-doc-name
type: project | daily | feedback | reference
project: my-project
date: 2026-06-27
tags: [deploy, ops]
---
```

### JSON fact store (zobodhi-style)

```json
{
  "memories": [
    {
      "id": 1748000000000,
      "text": "Don is the founder of Project X",
      "addedAt": "2026-06-27T03:00:00.000Z",
      "tags": ["user", "context"]
    }
  ]
}
```

## CLI reference

```
sync.ts sync [--source=zobodhi|clarion]
sync.ts status
sync.ts query <text> [--source=...] [--limit=N] [--json]
sync.ts add <fact>
sync.ts tail [N]

embed.ts info
embed.ts embed-query <text>
embed.ts embed-doc <text>

setup.ts [--recreate]
```

## Configuration

| Env var | Default | Notes |
|---|---|---|
| `ASTRA_DB_ENDPOINT` | — required | `https://<dbid>-<region>.apps.astra.datastax.com` |
| `ASTRA_DB_APPLICATION_TOKEN` | — required | Database read/write token |
| `ASTRA_DB_KEYSPACE` | `default_keyspace` | |
| `ASTRA_VECTOR_DIM` | `768` | Full Nomic output (matryoshka) |
| `ASTRA_VECTOR_SIM` | `cosine` | `cosine` \| `dot_product` \| `euclidean` |
| `MATRYOSHKA_DIM` | `768` | Truncate embeddings to this before L2-norm (64/128/256/512/768) |
| `HF_HOME` | `.cache/huggingface` | Model cache dir |
| `ZOBODHI_JSON` | `memory/zobodhi.json` | Path to zobodhi-style JSON file |
| `CLARION_ROOT` | `memory` | Root of markdown tree |

## Why local embeddings?

- **No per-query API cost.** Nomic is ~270MB quantized, runs in <1s on CPU.
- **Privacy.** Memory never leaves your machine for embedding.
- **Offline-capable.** Only Astra calls hit the network.
- **Free-tier friendly.** Astra's 80GB serverless free tier fits tens of millions of vectors.

## Embedding model

`nomic-embed-text-v1.5` — 768-dim, trained with Matryoshka Representation Learning (works at 64/128/256/512/768). Layer-norm + L2-normalized. Required prefixes:

- Queries: `search_query: <text>`
- Documents: `search_document: <text>`

Both added automatically. Don't strip them or quality degrades significantly.

## License

MIT. See `LICENSE`.