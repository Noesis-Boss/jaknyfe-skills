# Agent Specification: [Name]

## 1. Purpose and scope

- Job: [one sentence]
- Users: [who uses it]
- Trigger: [what starts a run]
- Inputs: [data supplied]
- Outputs: [artifacts or actions]
- Success criteria: [observable measures]
- Boundaries: [out of scope]
- Approval points: [human approval required for]

## 2. System prompt

- Role: [identity and responsibility]
- Core instructions: [durable behavior]
- Guardrails: [safety, privacy, and authority limits]
- Tool rules: [when tools may be used]
- Error behavior: [how uncertainty and failures are handled]
- Completion contract: [what must be true before stopping]

## 3. Model

- Primary model: [model]
- Rationale: [quality, latency, context, privacy, and cost]
- Fallback: [model or `none`]

## 4. Tools and integrations

| Tool | Purpose | Permission | Input/output | Timeout/retry | Failure behavior |
|---|---|---|---|---|---|
| [name] | [why] | [read/write] | [schema] | [policy] | [user-visible result] |

## 5. Memory and data

- Conversation state: [current-task history]
- Working state: [temporary state]
- Durable stores: [files, SQL, vector, or other]
- Saved data: [what is retained]
- Retention and ownership: [policy]
- Corrections and conflicts: [resolution rule]
- Secrets and sensitive data: [prohibited or protected handling]

## 6. Orchestration

```text
[trigger] -> [step] -> [decision] -> [step] -> [visible completion]
```

- State transitions: [states]
- Handoffs: [if any]
- Idempotency: [replay behavior]
- Stop condition: [when execution ends]

## 7. Interface contract

- Interface: [chat, web, API, CLI, or channel]
- Authentication: [method]
- Authorization: [roles and scopes]
- Validation: [accepted and rejected inputs]
- Progress: [streaming, status, or none]
- Errors: [presentation]
- Accessibility: [requirements]

## 8. Evaluation and definition of done

| Scenario | Expected result | Metric/threshold |
|---|---|---|
| Happy path | [result] | [threshold] |
| Edge case | [result] | [threshold] |
| Tool failure | [result] | [threshold] |
| Ambiguous request | [result] | [threshold] |
| Permission boundary | [result] | [threshold] |
| Adversarial input | [result] | [threshold] |

- Definition of done: [tests pass, interface verified, evidence preserved]
- Iteration loop: observe -> diagnose -> change one variable -> rerun
