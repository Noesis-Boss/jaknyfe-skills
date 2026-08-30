---
name: ch03-handoff-protocol-and-stop-rules
description: "Handoff protocol definition, stop rule types, state transitions, and receipt formats."
---

# Chapter 3 — Handoff Protocol & Stop Rules

## When to use
1. A task needs to hand off work to another agent
2. Data must flow between systems without manual copying
3. Human approval is required before proceeding
4. Audit trail needed for compliance/governance

## Handoff block
Add to any task description or AGENTS.md:

```yaml
handoff:
  target_agent: agent_id | external_system
  receipt_format: markdown | json | plain
  stop_rules:
    - condition: human_approval
      required_fields: [completed_at, output_artifact]
    - condition: validation_check
      script: validate_output.ts
  data_transfer:
    - field: output_artifact
      format: url | inline | reference
```

## Stop rule types
| Condition | Fields | Purpose |
|-----------|--------|---------|
| `human_approval` | `required_fields[]` | Wait for human review of specified task fields |
| `validation_check` | `script` | Run script before handoff completes |
| `time_delay` | `hours` | Minimum time between handoff states |

## State transitions (sequence)
1. User calls `POST /api/tasks/:id/handoff`
2. Task enters `handoff_pending` state
3. `initiateHandoff()` sets `next_handoff` and `stop_rules`
4. When task completes, check stop rules
5. Rules pass → `acknowledgeHandoff()` creates receipt
6. Rules fail → `rejectHandoff()` with reason
7. Receipt stored in `task.events`

## Receipt formats

### Markdown
```markdown
## Handoff Receipt: rcp_abc123

**From:** tsk_source
**To:** tsk_target
**When:** 2026-07-01T02:10:00Z
**Status:** accepted

### Data Payload
- result: Task completed successfully
- artifacts: [/reports/q3.pdf]
```

### JSON (programmatic consumers)
```json
{
  "handoff_id": "rcp_abc123",
  "from_task": "tsk_source",
  "to_task": "tsk_target",
  "timestamp": "2026-07-01T02:10:00Z",
  "data_payload": {"result": "...", "artifacts": [...]},
  "acknowledgment": true,
  "status": "accepted"
}
```

## Integration example
```ts
// Task worker checks handoff before completion
if (task.handoff_state !== "none") {
  const rules = JSON.parse(task.stop_rules || "[]");
  const passed = validateStopRules(task.id, rules);
  if (passed) {
    acknowledgeHandoff(task.id, { result: task.result });
  } else {
    rejectHandoff(task.id, "Stop rules validation failed");
  }
}
```
