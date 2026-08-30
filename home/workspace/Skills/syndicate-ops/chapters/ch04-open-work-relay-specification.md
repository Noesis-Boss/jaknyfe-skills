---
name: ch04-open-work-relay-specification
description: "Formal Open Work Relay spec: task schema extension, state machine, implementation checklist."
---

# Chapter 4 — Open Work Relay Specification

## Purpose
Formalize handoffs between agents/tasks to:
- eliminate manual data copying
- establish audit trails via receipts
- ensure queue agnosticism across tools
- implement Stop Rules for human-in-the-loop gates

## Task schema extensions
- `handoff_state`: 'none' | 'pending' | 'in_progress' | 'completed' | 'failed'
- `receipts`: JSON array of HandoffReceipt[]
- `stop_rules`: JSON array of StopRule[]
- `next_handoff`: string | null (task_id to hand to when complete)

## HandoffReceipt
```ts
interface HandoffReceipt {
  handoff_id: string;
  from_task: string;
  to_task: string;
  timestamp: string;
  data_payload: Record<string, unknown>;
  acknowledgment: boolean;
  status: 'pending' | 'accepted' | 'rejected';
}
```

## State machine
```
backlog → ready → running → blocked → done
                   ↘ handoff_pending → handoff_in_progress → done
                   ↘ handoff_failed → blocked
```

## Implementation checklist
- [x] Add `handoff_state`, `receipts`, `stop_rules`, `next_handoff` columns to tasks table
- [x] Create API endpoints: `/api/tasks/:id/handoff`, `/api/tasks/:id/receipts`
- [ ] Add handoff UI in CompanyBoard Tasks tab
- [x] Create receipt verification middleware (in acknowledgeHandoff function)
- [x] Add Stop Rules validator script runner (`scripts/stop-rules-validator.ts`)

The one open item is the handoff UI in the CompanyBoard Tasks tab.
