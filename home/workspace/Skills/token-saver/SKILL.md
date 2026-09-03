---
name: token-saver
description: Content-aware CLI output compression for Zo. Wraps the token-saver Python package (32 specialized processors for git, docker, npm, cargo, pytest, eslint, kubectl, terraform, and more) to compress verbose command output and save tokens. Use when running commands that produce large output (git log, npm install, test suites, docker logs, build output) and you want to see only the important parts.
compatibility: Created for Zo Computer. Requires Python 3.10+ (pre-installed on Zo). Token-saver is installed at /root/.token-saver/ via its Claude Code installer.
metadata:
  author: jaknyfe.zo.computer
  source: https://github.com/ppgranger/token-saver
---

# Token-Saver Skill

Content-aware CLI output compression. Runs commands through token-saver's
specialized processors so you see only what matters — errors, summaries,
and key details — instead of raw verbose output.

## Prerequisites

Token-saver is installed at `/root/.token-saver/` (installed via its Claude Code
installer on 2026-07-31). Python 3 is pre-installed on Zo.

## Usage

### Run a command with compression (recommended)

```bash
bun run Skills/token-saver/scripts/run.ts '<command>'
```

Example:
```bash
bun run Skills/token-saver/scripts/run.ts 'git log --oneline -50 --stat'
```

The wrapper also supports the CLI subcommands:
```bash
bun run Skills/token-saver/scripts/run.ts version
bun run Skills/token-saver/scripts/run.ts explain '<command>'    # which processor handles it (dry run)
bun run Skills/token-saver/scripts/run.ts benchmark '<command>'  # show savings stats
bun run Skills/token-saver/scripts/run.ts stats                  # cumulative savings
```

### Direct Python (no wrapper)

```bash
python3 /root/.token-saver/scripts/wrap.py '<command>'
python3 /root/.token-saver/src/cli.py explain '<command>'
```

### Shell alias

Added to `~/.bashrc`:
```bash
alias ts='python3 /root/.token-saver/scripts/wrap.py'
```
Use: `ts git log --oneline -50`

### Zo-safe command helper

Use `/home/workspace/bin/zo-run COMMAND [ARGS...]` for routine commands. It
routes supported verbose command families through token-saver and leaves shell,
file-viewing, and interpreter commands direct. Use
`/home/workspace/bin/zo-command-audit COMMAND [ARGS...]` to inspect routing
without executing anything.

## Supported commands (processor routing)

| Command family | Processor |
|----------------|-----------|
| `git` (status, diff, log, show, push/pull, branch, blame, reflog, merge) | `git` |
| `npm`/`yarn`/`pnpm`/`bun` (install, build, run, audit, add, update) | `build` / `bun` |
| `pytest`, `jest`, `vitest`, `mocha`, `cargo test`, `go test`, `rspec` | `test` |
| `cargo` (build, check, doc, bench) | `cargo` |
| `eslint`, `ruff`, `flake8`, `pylint`, `mypy`, `prettier`, `shellcheck` | `lint` |
| `docker` (ps, images, logs, pull, push, inspect, stats, compose) | `docker` |
| `kubectl`/`oc` (get, describe, logs, top) | `kubectl` |
| `gh` (pr, issue, run, repo, api) | `gh` |
| `terraform` (plan, apply, init, output, state) | `terraform` |
| `helm`, `ansible`, `pulumi`, `cdktf`, `nix`, `mise`, `go`, `jq`/`yq` | various |
| `grep`/`rg`/`ag`/`fd`, `curl`/`wget`, `du`/`wc`/`df`, `env`/`printenv` | various |
| Any other command | `generic` (ANSI strip, dedup, truncation) |

## Known limitation

Zo does NOT process PreToolUse Bash hooks, so automatic hook-based compression
(the package's primary mechanism for Claude Code) does not work here. Invocation
is always explicit via the wrapper or alias. See
`file 'Skills/token-saver/EVALUATION.md'` for the full assessment.
