# Project Selection Method

## Begin with a project brief

```text
For [specific user], solve [specific recurring problem]
using [available input] to produce [useful output]
within [time/budget/tool limits], while a human checks [risk].
```

Example:

```text
For a solo house cleaner, turn a redacted voice-note summary of a completed job into a customer follow-up draft and an internal supply checklist within one weekend, while the owner approves every message.
```

This is better than “build an AI app for small business.”

## Idea tiers

### Tiny exercises

Time: roughly 20 minutes to three hours.

Use for learning one mechanism:

- compare two prompt formats with test cases;
- extract a few fields from public text;
- classify a small dataset and inspect errors;
- create a source-grounded question-and-answer worksheet;
- build a command-line text transformation.

A tiny exercise may be worth sharing when the evaluation is thoughtful.

### Weekend projects

Time: one to three focused days.

Use for one complete workflow:

- input form → AI transformation → review screen → export;
- public document → key claims → cited brief;
- voice note → structured plan → human edits;
- code issue → reproducible test → suggested patch review.

Keep integrations optional.

### Portfolio projects

Time: one to four weeks.

Add:

- a real user or credible user test;
- clear documentation;
- test cases and failure analysis;
- a deployed demo or reproducible local setup;
- a case study;
- accessibility and privacy notes.

“Portfolio” means inspectable evidence, not maximum feature count.

### Workflow automations

Start manually. Automate only stable steps.

Good candidates:

- recurring classification;
- drafting from approved templates;
- routing low-risk records;
- generating a review queue;
- updating a non-sensitive internal summary.

Include logging, failure handling, permissions, and a human checkpoint.

### Weird useful internet machines

These combine a narrow odd input with an unexpectedly useful output.

Examples:

- **Abandoned-tab archaeologist:** groups exported browser tabs into “finish, save, or discard” with a human-reviewed rationale.
- **Promise lint:** scans public-facing draft copy for promises, dates, numbers, and claims that need evidence.
- **Friction diary synthesizer:** turns short notes about recurring annoyances into ranked automation candidates.
- **Reverse FAQ:** takes a confusing public page and generates the questions a first-time visitor is likely to ask, tied to quoted source sections.
- **Tiny bureaucracy translator:** converts one public form's instructions into a plain-language checklist without filling the form or giving legal advice.

Weirdness should improve memorability or usefulness, not hide a weak problem.

### Career-proof projects

Match a target role's real work:

- customer support: knowledge-grounded reply assistant with an error taxonomy;
- operations: exception-review queue with measured handling time;
- marketing: claim-checking content workflow;
- developer: test-first issue reproducer and patch-evaluation harness;
- analyst: source-to-brief pipeline with a claim-evidence table;
- educator: practice generator with rubric and learner-attempt loop.

Use current job descriptions to validate relevance when browsing is available.

## Scorecard

Score each criterion 1–5.

| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| Usefulness | novelty only | occasional value | solves a recurring problem |
| Beginner fit | requires many new layers | one or two new layers | mostly uses current skills |
| Buildability | blocked by access/dependencies | feasible with risk | obvious path with available tools |
| Learning value | copies a tutorial | requires adaptation | teaches transferable judgment |
| Portfolio value | output only | documented demo | problem, process, tests, result, explanation |
| Originality | generic clone | tailored combination | distinct problem framing or interaction |
| Demo potential | hard to show | understandable with setup | value visible in under two minutes |
| Low maintenance | fragile and costly | manageable | simple, cheap, few dependencies |

Scores support comparison. They do not replace judgment. A project with a lower total may be the right first build because it unlocks momentum or access.

### Optional weighting

Weight only when the user has a clear priority.

- Weekend: buildability ×2, low maintenance ×2.
- Learning: beginner fit ×2, learning value ×2.
- Portfolio: usefulness ×2, portfolio value ×2, demo potential ×2.
- Small business: usefulness ×2, low maintenance ×2, privacy risk as a separate gate.

Do not present decimal rankings as objective truth.

## MVP scope rule

Use **1–1–1–1–1**:

- one primary user;
- one problem;
- one main input;
- one AI transformation;
- one output.

Add:

- one human check;
- one failure state;
- one explicit non-goal.

Example:

```markdown
User: solo newsletter writer
Problem: identifying unsupported claims in a draft
Input: pasted draft plus approved source links
AI step: extract claims and map them to supplied evidence
Output: review table
Human check: writer verifies every source relationship
Failure state: unsupported or inaccessible source
Non-goal: automatic publication or fact certification
```

## Is AI actually needed?

Ask:

1. Is the input ambiguous, linguistic, visual, or variable?
2. Does a model add useful interpretation or generation?
3. Can the result be checked?
4. Would a form, filter, formula, template, or search query work better?
5. Does AI add privacy, cost, latency, or reliability problems larger than its value?

A non-AI solution is a successful recommendation when it better fits the problem.

## Seven-day build sequence

1. **Problem and sample:** define the user, input, output, and three safe examples.
2. **Manual baseline:** solve one example without automation.
3. **Core AI step:** make the narrow transformation work.
4. **Evaluation:** add typical, edge, and failure cases.
5. **Interface:** create the smallest usable input/review/output flow.
6. **User test and cleanup:** observe one person or simulate the exact workflow.
7. **Proof:** record demo, write README/case study, state limitations.

Build the risky assumption before the logo.

## What not to build yet

Common scope traps:

- a general-purpose chatbot;
- a platform for “everyone”;
- a multi-agent swarm without a validated manual workflow;
- a medical, legal, financial, hiring, or benefits decision maker;
- an app dependent on unapproved confidential data;
- broad web scraping without permission and maintenance planning;
- five integrations before the core transformation works;
- a clone whose only difference is a new model name;
- an automation with no logs, stop condition, or human approval;
- a project whose monthly cost is unknown.
