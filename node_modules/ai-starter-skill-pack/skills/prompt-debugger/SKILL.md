---
name: prompt-debugger
description: Diagnose and repair a prompt that produces vague, generic, incorrect, badly formatted, or model-mismatched results. Use for "fix this prompt," "why did the AI misunderstand me," "rewrite this for Claude/GPT/Gemini," "the model ignores my format," or "my prompt is not working." Identify whether the real problem is instructions, context, examples, output structure, model choice, missing data, or missing tools; then rewrite and test it. Do not use for general writing feedback, one-off factual questions, full automation architecture, or broad career coaching.
license: MIT
compatibility: Instruction-only Agent Skill; works best when the original prompt and observed output are available.
metadata:
  version: "1.0.0"
  category: prompting
---

# Prompt Debugger

Repair the smallest layer that is actually broken. Do not assume every failure is solved by adding prompt text.

## Route the request

Use this skill when the user has a specific prompt, prompt pattern, or model interaction to diagnose.

Do not use when:

- the user only wants a piece of writing improved and prompt behavior is not the issue;
- the user asks a factual question;
- the real task is end-to-end automation design;
- the user needs beginner onboarding, a learning curriculum, project ideation, or career planning;
- the failure is clearly an unavailable permission or external-system problem that requires technical support rather than prompting.

## Gather the minimum evidence

Identify:

1. target model and interface;
2. task type;
3. original prompt;
4. desired output;
5. actual output or failure;
6. available source data and tools;
7. hard constraints.

Ask for missing evidence only when it will change the diagnosis. Redact sensitive content. If no model is named, produce a model-neutral repair and label assumptions.

## Diagnose before rewriting

Check these failure modes:

- vague goal;
- missing context;
- decorative or wrong role;
- no output format;
- conflicting or unranked instructions;
- unrealistic request;
- no examples where examples are needed;
- weak, impossible, or ambiguous constraints;
- wrong model or interface for the task;
- missing data, retrieval, permissions, or tool access;
- request for hidden reasoning instead of useful visible evidence;
- trying to solve with prompting when code, browsing, calculation, validation, or another tool is required.

Name the few failure modes that materially explain the result. Do not produce a generic checklist disconnected from the prompt.

## Rewrite procedure

1. State what the prompt is trying to accomplish.
2. Identify the evidence for each diagnosed failure.
3. Separate task, context, constraints, sources, and output.
4. Remove duplicated, theatrical, or conflicting instructions.
5. Add examples only when they clarify format, labels, tone, or edge cases.
6. Add a structured output contract when the result will be parsed or compared.
7. Add tool and source instructions when the model needs external information.
8. Replace requests for hidden chain-of-thought with requests for assumptions, calculations, checks, citations, or concise rationale.
9. Write one primary fixed prompt.
10. Add model-specific variants only when they produce a real difference.
11. Create representative test inputs, including an edge case.
12. Explain the next variable to change if the repair still fails.

Use `references/prompt-failure-modes.md` for deeper diagnosis. Use `assets/prompt-debugger-templates.md` for reusable worksheets.

## Model-aware defaults

- **GPT-style:** lead with the outcome, evidence, constraints, and final form; avoid inherited process-heavy instruction stacks.
- **Claude-style:** be direct; use clear sections or XML-style tags for complex context; place long source material before the final task.
- **Gemini-style:** be direct; for long context, place material before the specific question; verify current API and preview-model settings.
- Do not claim a model supports a tool, schema mode, file type, or live-data source without current evidence.
- Native structured-output features are preferable when strict machine-readable schemas are required.

## Output

Use this structure:

```markdown
# Prompt Debug

## What The Prompt Is Trying To Do

## Why It Is Failing

## Fixed Prompt

## Model-Specific Notes

## Optional Variants

## Test Cases

## What To Change If It Still Fails
```

Put the fixed prompt in a fenced code block. Preserve user facts and legitimate constraints; do not silently invent missing content.

## Quality gate

Before finalizing, check:

- Does each diagnosis point to something observable?
- Is the fixed prompt shorter or clearer rather than merely longer?
- Does the output contract match the real use?
- Are tools, data, and permissions distinguished from instructions?
- Are examples necessary and correct?
- Are test cases representative and safe?
- Can the user identify the next variable to test?
