# Prompt Debugger Trigger Evals

## What these evals measure

- Correct invocation for a specific failed or model-mismatched prompt.
- Rejection of general writing, factual, career, and architecture tasks.
- Ability to identify a missing tool or source rather than endlessly expanding the prompt.
- Useful model-specific adaptation without invented capability claims.

## Manual method

1. Use a fresh conversation for each case.
2. Submit the query without explicitly naming the skill.
3. Record invocation and routing.
4. For positive cases, inspect whether the answer:
   - states the intended task;
   - cites observable failure evidence;
   - provides one primary fixed prompt;
   - includes meaningful tests;
   - separates prompt, model, data, and tool problems.
5. Repeat model-boundary and vague cases three times.
6. Run explicit invocation tests separately if supported.

## Pass criteria

A positive case fails even when the skill invokes if it:

- replaces the prompt with a longer but equally vague prompt;
- invents missing source data;
- claims wording enables a tool;
- demands hidden chain-of-thought;
- adds model-branded variants with no material difference;
- omits test cases.

A negative case fails when prompt debugging hijacks a direct editing or factual task.

## Description tuning

When false positives occur, strengthen the words “specific prompt, prompt pattern, or observed model interaction.” When false negatives occur, add the user's natural failure language rather than abstract prompt-engineering terminology.
