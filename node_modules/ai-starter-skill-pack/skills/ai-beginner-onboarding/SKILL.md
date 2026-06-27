---
name: ai-beginner-onboarding
description: Help an overwhelmed or uncertain beginner decide how to start using AI for life, work, school, a small business, or creative projects. Use for requests such as "I want to get into AI," "I do not know where to start," "which AI tools should I learn first," or "make me a beginner AI plan." Produce a tiny tool stack, a seven-day plan, one useful workflow, and one practice project. Do not use for advanced ML engineering, a single broken prompt, enterprise AI strategy, or a job-search-only request.
license: MIT
compatibility: Instruction-only Agent Skill; no network access or scripts required.
metadata:
  version: "1.0.0"
  category: ai-literacy
---

# AI Beginner Onboarding

Help the user take a useful first step without turning AI into a shopping list or giant curriculum.

## Route the request

Use this skill when the main problem is **starting**.

Route elsewhere when the main problem is:

- one prompt failing: use `prompt-debugger`;
- a sustained learning curriculum: use `personal-ai-tutor`;
- choosing something to build: use `ai-project-idea`;
- proving AI skills for work: use `no-bs-ai-career`;
- advanced model evaluation, ML engineering, or enterprise strategy: answer with a more appropriate specialist workflow.

## Beginner-safe defaults

Unless the user says otherwise:

- Recommend one general-purpose assistant they already have access to, plus an ordinary notes or document tool.
- Do not require an API, paid subscription, coding, agents, vector databases, or automation platforms.
- Plan for 20–30 minutes a day and include a 10-minute low-energy option.
- Begin with public, synthetic, or redacted information.
- Prefer one completed workflow over broad tool comparison.
- Treat device, disability, fatigue, budget, and inconsistent time as real design constraints.
- Do not claim that seven days creates mastery.

## Intake

Identify:

1. the user's real goal;
2. current experience;
3. available device and tools;
4. time and energy constraints;
5. the task they want AI to help with;
6. privacy or policy constraints.

Ask at most five bundled questions. When the user has already supplied enough context, do not repeat them. When details remain missing, state conservative assumptions and continue.

Never ask for passwords, private records, confidential work, or unredacted personal data.

## Procedure

1. Translate “learn AI” into one near-term outcome.
2. Summarize the user's starting position without judgment.
3. Choose the smallest tool stack that can support the outcome.
4. Explain why each tool is present and what is deliberately excluded.
5. Create a seven-day plan with one focused action per day.
6. Design one useful workflow using:
   - input;
   - AI task;
   - human check;
   - final use.
7. Define one practice project that can be completed with the available time and tools.
8. Include verification and privacy habits inside the work, not as an afterthought.
9. Name the most likely beginner mistakes.
10. End with one concrete check-in question or evidence request.

Use `references/onboarding-method.md` for selection rules and quality checks. Use `assets/onboarding-templates.md` when the user needs a worksheet or reusable plan.

## Output

Use this structure:

```markdown
# AI Beginner Onboarding

## Snapshot

## Best Starting Point

## Tiny Tool Stack

## 7-Day Starter Plan

## First Useful Workflow

## First Practice Project

## Mistakes to Avoid

## Next Check-In
```

### Output rules

- Keep the tiny tool stack to one to three items.
- Explain tools by function first; name current products only when useful and verify current availability when possible.
- Give actions, not course-topic labels.
- Make the first workflow useful to the user's actual life or work.
- Include a fallback for a low-energy day.
- Mark assumptions.
- Avoid hype, guilt, and employment promises.

## Quality gate

Before finalizing, check:

- Is there one clear first outcome?
- Can the user start with what they already have?
- Is every day small and observable?
- Does the workflow include a human verification step?
- Is the project finishable?
- Did the response avoid unnecessary tools?
- Did it protect sensitive data?
- Does the next check-in ask for evidence of use rather than motivation?
