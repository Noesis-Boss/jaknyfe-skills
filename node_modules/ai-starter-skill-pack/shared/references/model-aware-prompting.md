# Model-Aware Prompting

**Last reviewed:** 2026-06-23

Use this reference to adapt a prompt without turning model folklore into rigid law.

## A durable prompt pattern

Most useful prompts need five things:

1. **Outcome:** What should be accomplished?
2. **Context and evidence:** What background, source material, or data should the model use?
3. **Constraints:** What must be included, excluded, preserved, or verified?
4. **Output contract:** What shape, length, audience, or schema should the result follow?
5. **Tools and checks:** Does the task require browsing, files, code execution, calculation, retrieval, or human approval?

A compact template:

```text
Task: [the outcome]

Context:
[only the information needed]

Requirements:
- [important constraint]
- [important constraint]

Use:
[source material, file, data, or tool]

Return:
[format, audience, length, fields]

Before finalizing:
[checks the model can actually perform]
```

Do not add a role merely for decoration. “Act as a genius” is weak context. “Write for a first-year nursing student who has not studied pharmacology” changes the work.

## GPT-style prompting

Current OpenAI guidance for GPT-5.5 emphasizes short, outcome-first prompts over inherited stacks of process instructions.

Useful defaults:

- Lead with the desired result.
- State constraints and evidence clearly.
- Define the final answer, not a theatrical internal process.
- Ask for a concise rationale, assumptions, or verification notes when useful.
- Remove legacy instructions that repeat the same goal in several ways.
- Use tools or retrieval when the model needs current or private information.

Avoid requesting hidden chain-of-thought. Ask for useful visible work instead:

```text
State your assumptions, show the calculation, list the checks performed, and give a concise explanation of the conclusion.
```

## Claude-style prompting

Clear and direct instructions are the baseline.

For a complex prompt, separate parts with descriptive tags:

```xml
<task>...</task>
<context>...</context>
<constraints>...</constraints>
<examples>...</examples>
<input>...</input>
<output_format>...</output_format>
```

Useful defaults:

- Put long documents or source material before the final question.
- Use a few relevant, diverse examples when consistency matters.
- Make tool rules precise. Current models can be proactive, so blanket rules such as “use every tool whenever possible” can create unnecessary actions.
- State what to do when evidence is missing.
- Use the product's structured-output feature when machine-valid schema adherence is required.

Tags organize a prompt; they do not make an unclear task clear.

## Gemini-style prompting

Current Gemini guidance also favors direct, specific instructions and iteration.

Useful defaults:

- State the task and success criteria plainly.
- For long context, put the documents or dataset first and the specific question near the end.
- Use examples for format consistency or edge cases.
- Use supported structured-output features for machine-consumed JSON or schemas.
- Verify current model and API settings in official documentation. Preview models and recommended parameters change.

Do not copy API tuning advice into a chat prompt. Prompt design, model selection, tool configuration, and generation parameters are different layers.

## When examples help

Use examples when:

- the requested format is unusual;
- tone is hard to describe;
- labels or categories are ambiguous;
- edge cases matter;
- the model is inconsistent after a clear zero-shot request.

Good examples are:

- close to the real task;
- diverse enough to show boundaries;
- short enough not to drown the instruction;
- correctly labeled;
- free of accidental patterns the model should not copy.

Do not add examples to compensate for a missing goal or missing source data.

## When structured output helps

Use a structured-output or schema feature when another program will consume the result.

Good uses:

- extracting fixed fields;
- producing records for a database;
- validating allowed categories;
- passing arguments to a tool;
- returning predictable nested data.

A prompt that says “return valid JSON” may still produce invalid or semantically wrong JSON. Prefer the runtime's native schema enforcement when available, then validate the values after parsing.

For human readers, a Markdown heading structure is often easier and more forgiving.

## When tools beat prompting

Use a tool, retrieval system, or external process when the task needs:

- current facts, prices, schedules, laws, or job listings;
- exact calculations;
- content from a private file or account;
- actions in another system;
- large-scale search or comparison;
- deterministic validation;
- access the model does not have.

A better prompt cannot reveal a file that was never provided, browse without browsing access, or make a guessed fact current.

## Common beginner mistakes

| Mistake | Better move |
|---|---|
| “Make it better” | Name the audience, purpose, and desired change |
| Huge persona, tiny task | Put task and evidence first |
| Ten conflicting rules | Rank constraints and delete duplicates |
| No output format | Show the headings, fields, or example |
| Asking for certainty | Ask for uncertainty, sources, and checks |
| Asking for hidden reasoning | Ask for assumptions, calculations, and a concise rationale |
| Adding more words after every failure | Diagnose whether context, data, tools, or model choice is missing |
| Treating one model as universal | Test the exact model and interface |
| Pasting confidential data | Redact or use synthetic data |
| Trusting fluent output | Verify important claims against primary sources |

## Source links

- OpenAI GPT-5.5 prompt guidance: https://developers.openai.com/api/docs/guides/prompt-guidance
- OpenAI prompt engineering: https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI Academy prompting: https://openai.com/academy/prompting/
- Anthropic prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Google Gemini prompt design: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Google Gemini 3 developer guide: https://ai.google.dev/gemini-api/docs/gemini-3
- OpenAI accuracy guidance: https://help.openai.com/en/articles/8313428-does-chatgpt-tell-the-truth
- Anthropic hallucination guidance: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Google Gemini safety guidance: https://ai.google.dev/gemini-api/docs/safety-guidance
