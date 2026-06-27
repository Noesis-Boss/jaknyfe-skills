# Personal AI Tutor Trigger Evals

## Purpose

Test whether sustained learning requests invoke the tutor while one-off explanations, first-step onboarding, project ideation, and job search do not.

## Manual method

1. Run each query in a new conversation without naming the skill.
2. Record invocation.
3. For positive cases, check that the response includes:
   - an observable end demonstration;
   - starting-level evidence or a diagnostic;
   - three to five milestones;
   - active practice and transfer;
   - proof artifacts;
   - review checkpoints;
   - normal and low-energy scheduling when relevant;
   - a next lesson.
4. Repeat implicit and boundary cases three times.
5. Test explicit invocation separately.

## Pass criteria

The tutor should not behave like:

- a passive reading list;
- a giant catalog of AI topics;
- an automatic assignment-completion service;
- a certificate guarantee;
- a career plan with learning pasted on;
- a product recommendation list.

A positive output passes when the learner must do observable work and the plan can adapt from evidence.

## Regression clues

- False trigger on a single explanation: emphasize “learning over time” and “path.”
- False trigger on onboarding: distinguish first tool/first week from a sustained plan.
- False trigger on career: keep the target outcome educational rather than application-oriented.
- Weak outputs: ensure every milestone includes an independent attempt and proof artifact.
