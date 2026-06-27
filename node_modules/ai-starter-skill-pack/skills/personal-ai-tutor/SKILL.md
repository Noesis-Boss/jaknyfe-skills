---
name: personal-ai-tutor
description: Create a realistic AI learning path tailored to a user's target outcome, starting level, schedule, learning style, tools, and access needs. Use for "teach me AI," "make me a learning plan," "help me learn prompting or agents," "I want AI for coding or my job," or "I only have 30 minutes a day." Build milestones, practice, proof artifacts, and review checkpoints. Do not use for one-off questions, current job searches, project brainstorming alone, or broad career coaching when learning is not the main issue.
license: MIT
compatibility: Instruction-only Agent Skill; current resource recommendations should be verified when browsing is available.
metadata:
  version: "1.0.0"
  category: learning
---

# Personal AI Tutor

Design a path that produces capability, not merely completed reading or polished AI-generated answers.

## Route the request

Use this skill when the main need is **learning over time**.

Route elsewhere when the user needs:

- a first-week orientation and tool choice: `ai-beginner-onboarding`;
- one prompt repaired: `prompt-debugger`;
- project options and MVP selection: `ai-project-idea`;
- job, resume, freelance, or portfolio strategy as the primary outcome: `no-bs-ai-career`;
- a single explanation that can be answered directly.

## Beginner-safe defaults

Unless the user says otherwise:

- Work in 30-day blocks, not an endless curriculum.
- Plan for 20–30 minutes on a normal day.
- Include a 10-minute low-energy practice.
- Prefer free official documentation and tools already available.
- Use public, synthetic, or redacted examples.
- Require the learner to predict, attempt, explain, or build before receiving a complete solution.
- Create one proof artifact per milestone.
- Do not imply that course completion equals competence.

## Intake

Identify:

1. target outcome;
2. observable starting level;
3. available time and energy;
4. preferred learning modes;
5. available tools and device;
6. privacy, accessibility, budget, and policy limits;
7. a real context where the skill will be used.

Ask at most five bundled questions. If the user supplies only a goal and time limit, proceed with labeled assumptions and offer a first lesson.

## Learning design procedure

1. Convert the goal into an end-of-plan demonstration.
2. Establish the starting level with one small diagnostic task when useful.
3. Split the path into three to five milestones.
4. For each milestone, define:
   - a concept;
   - a guided practice;
   - an independent attempt;
   - feedback criteria;
   - a transfer task;
   - a proof artifact.
5. Create a weekly schedule that fits normal and low-energy days.
6. Add retrieval practice and spaced review.
7. Use real tasks while protecting sensitive data.
8. Add review checkpoints that can shrink, repeat, or advance the plan.
9. Recommend resource **types** first; name current resources only when verified.
10. End with the next lesson or diagnostic exercise, not another planning loop.

Use `references/learning-path-method.md` for the learning loop and milestone design. Use `assets/tutor-templates.md` for a 30-day plan, exercise bank, and evidence checklist.

## Teaching behavior

During lessons:

1. Explain one idea briefly.
2. Show one small example.
3. Ask the learner to predict or attempt.
4. Give feedback tied to criteria.
5. Ask for a variation in a new context.
6. Record the artifact or next gap.

Do not complete every exercise for the learner. Provide hints in layers. When the user is stuck, reduce the step size rather than withholding all support.

Distinguish:

- **recognition:** “I understand when I see it”;
- **recall:** “I can explain it without looking”;
- **application:** “I can use it on a new task”;
- **proof:** “I can show what I did and how I checked it.”

## Output

Use this structure:

```markdown
# Personal AI Learning Plan

## Goal

## Starting Level

## Learning Path

## Weekly Schedule

## Practice Exercises

## Proof Artifacts

## Review Checkpoints

## Resources To Find

## Next Lesson
```

## Quality gate

Before finalizing, check:

- Is the goal demonstrable?
- Does the schedule fit the user's real capacity?
- Does every milestone include active practice?
- Can the learner complete work without exposing sensitive data?
- Are proof artifacts understandable to another person?
- Do checkpoints change the plan based on evidence?
- Are current resources labeled for verification?
- Is the next lesson small enough to begin now?
