# AI Project Templates

## Project idea scorecard

```markdown
# Project Candidate: [name]

**Tier:** tiny / weekend / portfolio / automation / weird useful / career-proof  
**User:**  
**Problem:**  
**Input:**  
**Output:**  
**Why AI:**  
**Available tools:**  
**Time limit:**  
**Budget:**  
**Sensitive data:**  
**Human check:**  

| Criterion | Score 1–5 | Reason |
|---|---:|---|
| Usefulness | | |
| Beginner fit | | |
| Buildability | | |
| Learning value | | |
| Portfolio value | | |
| Originality | | |
| Demo potential | | |
| Low maintenance | | |

**Gate failures:** permission / privacy / safety / cost / unavailable data / none  
**Recommendation:** build now / shrink / research / reject
```

## MVP scope template

```markdown
# MVP Brief

## One user

## One problem

## One main input

## One AI transformation

## One output

## Human review

## Acceptance checks

1.
2.
3.

## Test cases

- Typical:
- Edge:
- Missing or malformed:
- Unsafe or disallowed:
- No-AI baseline:

## Failure behavior

When the model or tool cannot complete the task:

> 

## Non-goals

- 
- 

## Cost and maintenance limits

- Maximum setup cost:
- Maximum monthly cost:
- Dependencies:
- Who maintains it:
```

## Seven-day build template

```markdown
| Day | Build target | Evidence | Stop rule |
|---|---|---|---|
| 1 | Problem, sample inputs, acceptance checks | Project brief | No building until the user and output are clear |
| 2 | Manual baseline | Worked example | Stop if AI adds no value |
| 3 | Core AI transformation | First working result | Ignore interface polish |
| 4 | Evaluation | Typical, edge, and failure tests | Fix the largest failure |
| 5 | Small interface or repeatable procedure | End-to-end slice | No new features |
| 6 | User test and accessibility/privacy pass | Notes and changes | Cut confusing steps |
| 7 | Documentation and demo | README, video/screenshot, case study | Publish limitations |
```

## Project README template

```markdown
# [Project Name]

[One sentence: user + problem + useful result.]

## Problem

## Intended user

## What it does

## What it does not do

## Demo

[Link, screenshot, recording, or reproducible example.]

## Workflow

1.
2.
3.

## AI's role

## Human checks

## Data and privacy

## Setup

## Example input

## Example output

## Evaluation

| Test | Expected | Result |
|---|---|---|
| Typical | | |
| Edge | | |
| Failure | | |

## Known limitations

## What I learned

## Next sensible improvement
```

## Proof-of-work checklist

- [ ] Problem and user are specific.
- [ ] The user's contribution is clear.
- [ ] AI use is disclosed.
- [ ] A no-AI baseline was considered.
- [ ] Sample data is safe to share.
- [ ] At least three tests are documented.
- [ ] One failure is shown honestly.
- [ ] Human review is visible.
- [ ] Cost and dependencies are stated.
- [ ] The project has a clear non-goal.
- [ ] A stranger can understand the value quickly.
- [ ] The demo can be reproduced or inspected.
- [ ] Accessibility issues are considered.
- [ ] Claims are measured or phrased conservatively.
- [ ] Confidential information is absent.

## Project-to-case-study outline

```markdown
### Situation
What recurring problem existed?

### Constraint
What made it difficult?

### Approach
What workflow did you design, and where did AI fit?

### Verification
How did you test and review it?

### Result
What changed? Use measured or plainly observable evidence.

### Limitation
What should not be inferred?

### Next step
What improvement is justified by evidence?
```
