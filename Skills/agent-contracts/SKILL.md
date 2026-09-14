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
bun run Skills/agent-contracts/scripts/agent-contract.ts list --limit=20
bun run Skills/agent-contracts/scripts/agent-contract.ts show RUN_ID
bun run Skills/agent-contracts/scripts/dashboard.ts
```

Required contract fields are `name`, `purpose`, `allowed_paths`, `allowed_tools`, and `forbidden_actions`. Every log record includes `run_id`, `agent`, `surface`, `type`, `status`, and an ISO timestamp.

`dashboard.ts` generates `runs/agent-contracts/dashboard.html`, a local read-only audit view with run filtering and event timelines. Zorro records tool events for memory queries, autosync, and plan emission.

Tool events are enforced against the active contract's `allowed_tools`; denied events fail before they are logged.

The Zo Space dashboard is `/agent-audit` and reads `AGENT_AUDIT_PASSWORD` from Zo Secrets. The page is private at the platform layer; the API also requires the same password before returning audit data.
