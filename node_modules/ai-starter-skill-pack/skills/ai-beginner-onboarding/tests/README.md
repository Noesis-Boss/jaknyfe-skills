# AI Beginner Onboarding Trigger Evals

These cases test routing, not just whether the assistant can produce an onboarding plan after being told which skill to use.

## Manual method

1. Install the skill in a clean test runtime.
2. Start a fresh conversation for each case in `eval_queries.json`.
3. Submit the query without naming the skill.
4. Record:
   - whether the skill was invoked;
   - whether another skill was more appropriate;
   - whether the required headings appeared;
   - whether the response used a tiny stack and a realistic first workflow.
5. Repeat ambiguous cases three times because routing can be probabilistic.
6. Test explicit invocation separately if the runtime supports it.

## Pass criteria

A case passes when:

- `should_trigger: true` invokes this skill or clearly follows its procedure;
- `should_trigger: false` does not invoke it;
- anxious or vague requests do not receive a giant tool list;
- missing details produce a small intake or labeled assumptions;
- sensitive-data requests are minimized;
- the plan includes a low-energy path where relevant.

## Regression clues

- **False negatives:** add more natural trigger phrases to the frontmatter description.
- **Prompt-debugger false positives:** sharpen “starting” versus “repairing one prompt.”
- **Tutor false positives:** emphasize that onboarding is a first seven-day orientation, not a sustained curriculum.
- **Career false positives:** keep job-search-only language in the non-use boundary.
- **Verbose outputs:** move explanation into the local reference rather than expanding `SKILL.md`.
