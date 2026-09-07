---
name: token-saver
description: Content-compresses verbose CLI output (git, npm/bun, cargo, pytest, docker, kubectl, terraform, curl -v, ls -la, grep -r, make) to save tokens. Run verbose commands via `bun run /home/workspace/Skills/token-saver/scripts/run.ts <command>`. Non-compressible commands pass through untouched with stderr and exit codes preserved. Full install lives at /root/.token-saver.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  version: 2.6.3
---

# token-saver

Re-registered 2026-09-07 after the Skills/token-saver directory was lost. The full install (scripts, hooks, savings.db, installers) remains intact at `/root/.token-saver`; this skill directory only carries the Zo-facing wrapper docs.

## Usage

Wrap any command that may produce verbose output:

```bash
bun run /home/workspace/Skills/token-saver/scripts/run.ts <command>
```

- Auto-passes-through non-compressible commands (ssh, python3 generic, interactive).
- Preserves stderr and exit codes.
- Output threshold: wrap anything likely >~500 chars; skip trivial commands.

## Diagnostics

```bash
bun run /home/workspace/Skills/token-saver/scripts/run.ts explain '<command>'   # show routing
bun run /home/workspace/Skills/token-saver/scripts/run.ts benchmark '<cmd>' --show-removed
```

When output was compressed, do NOT fabricate removed detail — note "output compressed by token-saver" and point to the full output if needed.
