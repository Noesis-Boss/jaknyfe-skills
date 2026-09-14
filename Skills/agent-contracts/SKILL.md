---
name: agent-contracts
description: Define scoped agent contracts and append structured run logs for Zorro sessions, skills, and automations.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Agent contracts and run logs

Use this skill when an agent, skill, or automation needs an explicit scope and a durable audit trail.

Contracts are Markdown files with YAML frontmatter under `config/agents/`. Run logs are JSONL files under `runs/`. The logger never records secrets or full prompt content; record identifiers, paths, tools, status, and artifact paths.

Run:

```bash
bun run Skills/agent-contracts/scripts/agent-contract.ts validate config/agents/example.md
bun run Skills/agent-contracts/scripts/agent-contract.ts start --agent example --surface skill
bun run Skills/agent-contracts/scripts/agent-contract.ts event --run RUN_ID --type tool --name read_file --status ok
bun run Skills/agent-contracts/scripts/agent-contract.ts finish --run RUN_ID --status ok --artifact output/result.md
```

Required contract fields are `name`, `purpose`, `allowed_paths`, `allowed_tools`, and `forbidden_actions`. Every log record includes `run_id`, `agent`, `surface`, `type`, `status`, and an ISO timestamp.
