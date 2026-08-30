# MANUAL-STEPS.md — the 4 UI steps the script can't do

Run `scripts/install-zorro.sh` first. Then these four steps, in order.
Each step is a Zo UI action — no shell needed.

> **Version note (2026-08-01):** The proxy is a **public** http service
> on :11435 and streams **real SSE**. Earlier versions of this doc said
> "private" and "forces stream:false" — both were wrong and caused the
> "streamed response ended without content" bug. See
> `Skills/ollama-proxy/SETUP.md` for the full story.

---

## Step 1 — Register the two services (~3 min)

Paste [`SERVICES-REQUEST.md`](./SERVICES-REQUEST.md) into a Zo chat and
let Zo create the services:

| Service | Mode | Purpose |
|---|---|---|
| `ollama-server` | process (no endpoint) | Runs Ollama on `127.0.0.1:11434` |
| `ollama-proxy` | **http, public**, :11435 | OpenAI-compatible bridge; streams real SSE when the client asks, buffered JSON otherwise |

**Smoke test** (from the Zo terminal, or ask Zo to run it):

```bash
curl -s http://localhost:11435/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3:14b","messages":[{"role":"user","content":"Say OK"}],"stream":false}'
```

Expect HTTP 200 with an `assistant` reply. Also verify the public URL
works — this is what Zo's cloud provider actually calls:

```bash
curl -s https://ollama-proxy-<your-handle>.zocomputer.io/v1/models
```

Expect a JSON model list. **The proxy MUST be public** — a private
service resolves `localhost` in Zo's cloud backend, not in your
container, and every chat then fails with a connection error.

## Step 2 — AstraDB secrets (free tier) (~5 min)

1. Create a **free** AstraDB account → database (e.g. `zorro-memory`,
   provider: Google Cloud / us-east1, Serverless) at
   https://astra.datastax.com
2. Database → **Connect** → **API Endpoint** → copy the endpoint URL
   (format `https://<db>-<id>.apps.astra.datastax.com`)
3. **Application Token** → Generate token → copy (starts with
   `AstraCS:...`)
4. In Zo: Settings → Advanced → **Secrets** → add:
   - `ASTRA_DB_ENDPOINT` = endpoint URL
   - `ASTRA_DB_APPLICATION_TOKEN` = token
5. First sync creates the `memories` collection automatically:

```bash
cd /home/workspace/Skills/astra-memory/scripts && bun run sync.ts sync
```

First run downloads the local embedding model (~270 MB) to
`/home/.z/hf-cache` — one-time, 1–3 min. Later syncs are fast.

## Step 3 — Add the free local AI provider (~3 min)

Settings → AI → Providers → **Bring Your Own Key** → OpenAI-compatible:

- Name: `ollama-local`
- Base URL: `https://ollama-proxy-<handle>.zocomputer.io/v1`
- API key: `ollama` (any non-empty string — the proxy doesn't check it)
- Model: `qwen3:14b` (primary) — `gemma3:1b` for a fast fallback

> **Never** use `http://localhost:11435/v1` or a container IP here. The
> provider layer is cloud-side; only the public `*.zocomputer.io` URL is
> reachable and stable (container IPs change on every restart).

This provider serves both chat and the persona (Step 4).

## Step 4 — Create the Zorro persona (~5 min)

Settings → AI → Personas → **New persona**:

- Name: `Zorro`
- Prompt: paste [`ZORRO-PERSONA-PROMPT.md`](./ZORRO-PERSONA-PROMPT.md)
- Model: `ollama-local` (or your paid model)
- Avatar: `https://static.z.computer/img/persona/c9271814-e180-47e4-b216-e1fed2b85461.jpg`
- Save, then switch to the Zorro persona from the persona picker.

---

## First-use check

Ask Zorro: *"what do you remember about me?"* — expect it to run
`zorro.ts memory "..."`, find the seeded memory tree, and answer from
your `USER.md`/`MEMORY.md`. Then `bun run skills/astra-memory/scripts/sync.ts sync`
should show a successful AstraDB sync.

## Troubleshooting

| Symptom | Fix |
|---|---|
| "model stream was interrupted" / "streamed response ended without content or tool calls" | Provider Base URL must be the **public** proxy URL (`https://ollama-proxy-<handle>.zocomputer.io/v1`), not `:11434` and not `localhost`. The proxy passes real SSE now — if it recurs, restart the `ollama-proxy` service (killing the process makes the supervisor relaunch it with the current `proxy.ts`). |
| Provider connection timeout | Stale container IP in Base URL. The public `*.zocomputer.io` URL never goes stale — use it. |
| `sync.ts` fails on first run | The embedding model download (HuggingFace) may be slow/blocked. Re-run; ensure `@xenova/transformers` exists (`ls /home/workspace/node_modules/@xenova/transformers`), else re-run installer with `SKIP_BUN_DEPS` unset. |
| Ollama not answering on 11434 | Check the `ollama-server` service is enabled and running (Services panel). It must bind `127.0.0.1:11434` only — the proxy reaches it from inside the container. |
| `ollama` binary missing after script | Run the tarball fallback manually: `curl -fsSL -o /tmp/ollama.tgz https://ollama.com/download/ollama-linux-amd64.tgz && tar -C /usr/local -xzf /tmp/ollama.tgz` |
| Memory feels empty | Seeding is optional: the installer writes `USER.md` + `MEMORY.md` stubs. Feed Zorro real facts via chat — `event=chatMessage` rules (see AGENTS.md) mirror them into memory automatically. |
