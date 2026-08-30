---
name: caveman-code
description: Run the @juliusbrussee/caveman-code CLI — a provider-agnostic terminal coding agent with token-saving "Caveman mode" compression, multi-provider auth (Anthropic, OpenAI, Google, xAI, etc.), interactive TUI, print mode for one-shots, and JSON/RPC mode for automation. Use when the user wants to run a coding task with the caveman/caveman-code CLI, install it, check its version, list supported providers, or invoke it with a prompt. Backed by the upstream npm package — keep this skill thin and let caveman do the work.
compatibility: Created for Zo Computer. Requires Node.js 20+ on the host.
metadata:
  author: jaknyfe.zo.computer
---

# caveman-code skill

Thin wrapper around the upstream `caveman` / `caveman-code` CLI (`@juliusbrussee/caveman-code`).

## Default provider

The wrapper defaults to **OpenRouter** with model **`openrouter/owl-alpha`** (a 1M-context, 262K-output coding model). To use a different provider/model, pass the flags explicitly — the wrapper only injects defaults when `--provider` and `--model` are absent.

## Install

The wrapper script installs the package globally via npm on first run if it isn't already present:

```bash
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts --help
```

If the global install is missing, you'll be prompted to install it. You can also install manually:

```bash
npm install -g @juliusbrussee/caveman-code
```

## Auth

caveman-code is provider-agnostic. Set one of the standard env vars before invoking:

- `ANTHROPIC_API_KEY` — Anthropic (Claude)
- `OPENAI_API_KEY` — OpenAI
- `GOOGLE_API_KEY` / `GEMINI_API_KEY` — Google
- `XAI_API_KEY` — xAI (Grok)
- `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `MISTRAL_API_KEY`, etc.

Or run `caveman` interactively and use `/login` for OAuth subscriptions (Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot, Gemini).

The Zo-side wrapper reads API keys from the same env vars. Add them in [Settings > Advanced](/?t=settings&s=advanced) as Secrets.

## Usage

### Wrapper CLI

```bash
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts <caveman-args...>
```

Examples:

```bash
# Print mode — one-shot prompt, prints response, exits
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts -p "summarize this file"

# JSON mode — structured output for automation
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts --mode json -p "list files in /tmp"

# Pick a provider/model
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts --provider openai --model gpt-4o -p "..."

# Continue most recent session
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts -c

# Browse sessions
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts -r

# Version
bun run /home/workspace/Skills/caveman-code/scripts/caveman.ts --version
```

The wrapper passes `--yes` to `npm install -g` if a global install is needed, and otherwise just forwards argv to the `caveman` binary on PATH.

### Interactive mode

For the full TUI, run the binary directly (the wrapper is meant for non-interactive scripted use):

```bash
caveman
```

This opens a full TUI with history, file picker, slash commands (`/login`, `/model`, `/compact`, `/settings`, …), and a status footer showing token/cache usage and cost.

## Caveats

- Requires Node.js 20+. Zo Computer ships with this; no extra setup.
- The package pulls in a non-trivial dep tree (`better-sqlite3`, native photon-node wasm, etc.). First-time install takes ~30s.
- This skill is a thin shim. Behavior, flags, and provider setup are owned upstream — see the package README at https://www.npmjs.com/package/@juliusbrussee/caveman-code.
- Don't run the interactive TUI from inside another tool call — use the host terminal directly via [Terminal](/?t=terminal).

## Provider notes

- **OpenRouter**: requires `OPENROUTER_API_KEY` in env. If the OpenRouter privacy data policy is set to "deny all", some models return 404 — relax at https://openrouter.ai/settings/privacy or pick a different model.
- **Google Gemini**: requires `GEMINI_API_KEY` in env. The wrapper auto-maps the workspace's `GOOGLE_GENERATIVE_AI_KEY` to `GEMINI_API_KEY` for convenience.
- **Anthropic / OpenAI / etc.**: pass `--api-key <key>` or set the appropriate env var.
