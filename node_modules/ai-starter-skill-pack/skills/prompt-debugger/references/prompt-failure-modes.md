# Prompt Failure Modes

Use this reference to diagnose a prompt without falling into “more detail is always better.”

## Fast triage

Ask four questions:

1. **Did the model understand the task?**
2. **Did it have the information and capability required?**
3. **Did the prompt define a usable result?**
4. **Can success be tested?**

A “no” in a later layer cannot always be repaired in an earlier one.

## Diagnosis table

### Vague goal

**Signal:** The prompt uses words such as “better,” “professional,” “deep,” or “engaging” without defining the intended change.

**Repair:** Name audience, purpose, decision, and success criteria.

```text
Weak: Make this better.
Better: Rewrite this support reply for a frustrated customer. Keep every factual promise unchanged, acknowledge the delay in the first two sentences, and end with the next action.
```

### Missing context

**Signal:** The output guesses the audience, facts, scope, terminology, or history.

**Repair:** Add only context that changes the answer. Label unknowns.

Do not paste an entire private archive when three redacted facts are sufficient.

### Wrong or decorative role

**Signal:** “Act as a world-class genius” adds tone but not expertise, standards, or audience.

**Repair:** Replace status theater with task-relevant perspective.

```text
Review this as a maintainer who must support the code for two years. Focus on error handling, dependencies, and testability.
```

A role is optional. A concrete evaluation frame is useful.

### No output format

**Signal:** Correct content arrives in an unusable essay, wrong length, or inconsistent structure.

**Repair:** Define headings, fields, table columns, maximum length, or schema.

Do not demand a table when nested prose or long code will fit poorly.

### Conflicting instructions

**Signal:** The prompt says “be exhaustive” and “under 100 words,” or contains several incompatible personas and formats.

**Repair:**

1. delete duplicates;
2. rank the true constraints;
3. state which rule wins during a conflict.

```text
Priority order: factual accuracy, preservation of quoted text, then brevity.
```

### Unrealistic request

**Signal:** The model is asked to guarantee truth, predict an unknowable result, process missing content, or complete a task beyond available tools.

**Repair:** Narrow the outcome and add an evidence or human-review step.

### No examples

**Signal:** The task uses custom labels, unusual tone, or strict transformations and results vary despite clear instructions.

**Repair:** Add one to five short, correct, diverse examples. Include an edge case if boundaries matter.

Examples are not a substitute for rules. Examples with mistakes teach the mistakes.

### Bad constraints

**Signal:** Constraints are subjective, unverifiable, overly numerous, or impossible.

**Repair:** Convert them into observable checks.

| Weak constraint | Testable constraint |
|---|---|
| “Sound human” | “Use contractions, vary sentence length, and avoid sales claims.” |
| “Do not hallucinate” | “Use only the supplied sources; mark unsupported fields `unknown`.” |
| “Be comprehensive” | “Cover the five listed categories and identify missing evidence.” |

### Wrong model or interface

**Signal:** The task needs image understanding, a large file, code execution, strict schema output, or long-context behavior unavailable in the chosen interface.

**Repair:** Confirm current capabilities, then change model, interface, or workflow. Do not fabricate capability through instructions.

### Missing data or tool access

**Signal:** The prompt asks for today's prices, a private file, a calendar action, or exact calculations but the model lacks browsing, file access, account access, or a calculator.

**Repair:** Supply the approved data, enable the appropriate tool, or redesign the result as a research plan. A prompt cannot grant permission.

### Hidden reasoning request

**Signal:** The prompt demands private internal chain-of-thought or “every thought.”

**Repair:** Ask for inspectable work:

- assumptions;
- source citations;
- calculations;
- decision criteria;
- uncertainty;
- tests performed;
- a concise rationale.

### Prompting instead of engineering

**Signal:** Reliability requires deterministic behavior, repeated data processing, retries, state, validation, or external actions.

**Repair:** Move the reliable parts into code, schemas, tools, and checks. Use the prompt for judgment where flexibility is valuable.

Examples:

- parse with a schema, not a promise to “always output valid JSON”;
- calculate in code, not free-form prose;
- retrieve the current policy, not model memory;
- validate URLs and citations after generation;
- require approval before an external action.

## A layered repair order

Fix in this order:

1. **Access:** Is the data/tool/file available?
2. **Task:** Is the outcome clear and feasible?
3. **Evidence:** Is the relevant context present?
4. **Priority:** Are constraints compatible and ranked?
5. **Format:** Is the result usable?
6. **Examples:** Are boundaries still ambiguous?
7. **Model tuning:** Does the exact model need adaptation?

This prevents elaborate prompts around a missing capability.

## Before/after comparison

A repaired prompt should improve at least one measurable dimension:

- fewer unsupported claims;
- required fields present;
- correct length or format;
- stable labels across test inputs;
- fewer clarification loops;
- correct handling of edge cases;
- easier human verification.

Do not call a rewrite “better” merely because it is longer.

## Model variants: when they are justified

Create variants only when the target changes something material:

- source placement in long context;
- supported schema or tool mechanism;
- instruction organization;
- degree of proactivity;
- known interface limitation.

Avoid three cosmetic rewrites that differ only by model brand name.
