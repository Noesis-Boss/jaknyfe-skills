---
name: ai-project-idea
description: Generate and rank small, realistic AI project ideas for a beginner, non-coder, self-taught developer, creator, job seeker, freelancer, worker, or small-business owner. Use for "what should I build with AI," "give me a weekend project," "I need a portfolio project," "small AI app ideas," or "something useful I can automate." Match ideas to interests, skills, tools, time, budget, and audience; recommend one MVP and a seven-day build plan. Do not use for unconstrained generic brainstorming, full startup market research, enterprise strategy, or career planning when a project is not the main need.
license: MIT
compatibility: Instruction-only Agent Skill; live product or market claims require current research.
metadata:
  version: "1.0.0"
  category: projects
---

# AI Project Ideas

Generate ideas the user can finish, explain, test, and demonstrate.

## Route the request

Use this skill when the main need is **choosing and scoping an AI project**.

Route elsewhere when:

- the user needs their first AI orientation: `ai-beginner-onboarding`;
- the user needs a sustained curriculum: `personal-ai-tutor`;
- one prompt is broken: `prompt-debugger`;
- the main goal is resume, job, freelance, or workplace strategy: `no-bs-ai-career`;
- the user requests full market validation, enterprise architecture, or startup financing.

Do not answer “give me ideas” with an unranked pile. Ask for constraints or state useful assumptions.

## Intake

Identify:

1. current skills;
2. interests or domain knowledge;
3. available tools and device;
4. time limit;
5. budget;
6. intended user or audience;
7. desired value: practice, personal usefulness, public demo, portfolio proof, freelance offer, or workplace improvement;
8. privacy, access, and maintenance constraints.

Ask at most five bundled questions. If the user gives little context, offer a small cross-section and label assumptions.

## Idea procedure

1. Convert interests and constraints into a project brief.
2. Generate ideas across applicable tiers:
   - tiny exercises;
   - weekend projects;
   - portfolio projects;
   - workflow automations;
   - weird useful internet machines;
   - career-proof projects.
3. Reject ideas that depend on unavailable data, unaffordable services, unauthorized access, or unsafe autonomous decisions.
4. Score the strongest ideas from 1–5 on:
   - usefulness;
   - beginner fit;
   - buildability;
   - learning value;
   - portfolio value;
   - originality;
   - demo potential;
   - maintenance burden, scored as **low burden = high score**.
5. Explain scores in plain language; do not imply scientific precision.
6. Rank the ideas and recommend one first build.
7. Scope the MVP to one user, one problem, one main input, one transformation, and one output.
8. Define acceptance checks and likely failure cases.
9. Define a proof-of-work artifact.
10. Create a seven-day build plan with a working slice early.
11. State what not to build yet.

Use `references/project-selection-method.md` for scoring and scope control. Use `assets/project-templates.md` for the scorecard, MVP brief, README, and proof checklist.

## Safe build defaults

- Use sample, public, or redacted data first.
- Keep a human approval step before consequential actions.
- Prefer a manual workflow prototype before automation.
- Do not recommend autonomous health, legal, benefits, employment, credit, housing, or safety decisions.
- Do not assume scraping, data reuse, or account access is permitted.
- Do not require a paid API unless the user accepts the cost.
- Include a no-AI or simpler baseline when it may solve the problem better.
- State current capability, pricing, and integration assumptions as unverified unless checked.

## Output

Use this structure:

```markdown
# AI Project Ideas

## User Fit

## Ranked Ideas

## Best First Project

## MVP Scope

## 7-Day Build Plan

## Proof-of-Work Artifact

## What Not To Build Yet
```

For ranked ideas, include the tier, intended user, one-sentence value, stack level, and score summary.

## Quality gate

Before finalizing, check:

- Are ideas grounded in the user's interests or constraints?
- Do the tiers offer meaningfully different sizes?
- Is the recommended project finishable?
- Does the MVP have a clear non-goal?
- Can the result be demonstrated with safe data?
- Is the AI step necessary rather than decorative?
- Does the plan produce a working slice before polish?
- Does the artifact reveal judgment, testing, and limitations?
- Is maintenance realistic?
