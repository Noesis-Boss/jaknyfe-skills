# Prompt Debugger Templates

## Prompt diagnosis checklist

```markdown
### Environment
- Target model:
- Product/interface:
- Available tools:
- File or source access:
- Current information required? yes / no

### Behavior
- Original prompt:
- Desired result:
- Actual result:
- Reproducible every time?:
- One example failure:

### Diagnosis
- [ ] Vague goal
- [ ] Missing context
- [ ] Decorative or wrong role
- [ ] No output format
- [ ] Conflicting instructions
- [ ] Unrealistic request
- [ ] Examples needed
- [ ] Ambiguous or impossible constraints
- [ ] Wrong model/interface
- [ ] Missing data/tool/permission
- [ ] Hidden reasoning request
- [ ] Needs code, retrieval, or validation rather than more prompting

### Success test
A repaired prompt succeeds when:
1.
2.
3.
```

## Before/after prompt template

~~~~markdown
## Before

```text
[original prompt]
```

## Observed failure

[what happened, with one safe example]

## Diagnosis

| Problem | Evidence | Repair |
|---|---|---|
| | | |

## After

```text
Task:
[desired outcome]

Context:
[relevant facts and source material]

Requirements:
- [constraint]
- [constraint]

Use:
[allowed sources or tools]

Return:
[headings, fields, length, or schema]

Checks:
[visible checks, assumptions, or uncertainty]
```

## Why the rewrite should work

[connect each change to a failure]
~~~~

## Model-aware quick reference

| Situation | GPT-style default | Claude-style default | Gemini-style default |
|---|---|---|---|
| Ordinary task | Outcome first; concise constraints | Clear and direct | Clear and direct |
| Complex sections | Headings or delimiters | Headings or descriptive XML tags | Headings or delimiters |
| Long source material | Provide only relevant evidence | Source first, question later | Source first, question later |
| Consistency | Add relevant examples | Add relevant, diverse examples | Add relevant examples |
| Strict machine format | Native structured output when supported | Native structured output when supported | Native structured output when supported |
| Current/private facts | Use an approved tool or retrieval | Use an approved tool or retrieval | Use an approved tool or retrieval |

Always verify current product capabilities. The model family name alone does not reveal the tools present in a particular interface.

## Prompt test-case template

```markdown
| Test | Input | Expected behavior | Failure signal |
|---|---|---|---|
| Typical | | | |
| Minimal context | | | |
| Edge case | | | |
| Conflicting data | | | |
| Missing evidence | | | |
| Adversarial or malformed | | | |
```

### Test protocol

1. Run the original prompt on the same inputs.
2. Run the repaired prompt without changing other variables.
3. Compare against the stated success tests.
4. Change one variable at a time.
5. Save failures, not only successes.
6. Validate machine-readable output with a parser or schema.
7. Have a person inspect correctness, not only format.
