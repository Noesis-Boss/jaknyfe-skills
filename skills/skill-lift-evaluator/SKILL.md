---
name: skill-lift-evaluator
description: >-
  Design and run a controlled evaluation of whether an agent skill improves
  task outcomes compared with the same agent without that skill. Use when
  deciding whether to keep, revise, or retire a skill, or when measuring a
  skill revision's effect.
metadata:
  author: jaknyfe.zo.computer
---
# Skill Lift Evaluator

Evaluate a skill's incremental value on its intended tasks. This workflow is
method guidance; do not imply that a benchmark is statistically conclusive when
the sample is small or the evaluation lacks controls.

## 1. Define the decision

Record the skill path and version, intended task types, target users or agents,
the decision to inform (keep, revise, retire, or compare versions), and the
cost or risk of a wrong decision. Define success criteria before running cases.
Separate skill selection (whether the agent should invoke it) from skill
execution (whether using it improves the result).

## 2. Build a case set

Create cases from real representative requests where possible. Include routine
tasks, edge cases, relevant safety constraints, and near-miss tasks where the
skill should not be used. Write acceptance criteria or scoring rubrics before
seeing outputs. Keep a small held-out set for confirmation after revisions.
Avoid using only examples copied from the skill itself.

For each case, record: ID, prompt, expected behavior, verifier or rubric,
importance/weight, and whether skill invocation is appropriate. Prefer
deterministic checks for observable outcomes; use a blinded human or rubric
judge for subjective quality. Do not treat an LLM judge as ground truth.

## 3. Run a paired comparison

For every case, run both conditions:

- **Baseline:** same agent and task, with the candidate skill unavailable.
- **Skill:** same agent and task, with the candidate skill available and
  invoked according to the intended workflow.

Hold model, system instructions, tools, permissions, task wording, and starting
state constant. Randomize run order where practical. Repeat runs when outputs
are stochastic, and record model/version, harness, skill commit, tool versions,
run count, failures, and cost. Do not let either condition see the other's
output. Use isolated clean state for every run when tasks mutate files or data.

If the decision includes whether the skill is discoverable, run a separate
selection test with natural requests; do not conflate routing failures with
execution quality. Include near-miss cases to measure unnecessary invocation.

## 4. Score and compare

Apply the prewritten verifiers/rubrics to both outputs without revealing the
condition where feasible. Report per-case paired differences and aggregate:
success rate, quality dimensions, safety violations, unwanted side effects,
latency, and token/cost use when available. Keep safety failures visible as
hard gates; a quality average must not cancel a serious violation.

For small pilots, report counts and raw differences without claims of
significance. With enough independent paired cases, report an appropriate
uncertainty interval and method; do not infer population-wide usefulness from
repeated runs of only a few prompts. Identify evaluator disagreements and
missing evidence.

## 5. Decide and report

Use the thresholds set before the evaluation. If none were set, give a
provisional recommendation and state that thresholds need owner approval.
Recommend:

- **Keep** when the skill improves the targeted outcomes and passes safety and
  cost constraints across representative cases.
- **Revise** when gains are limited to certain cases, routing is unreliable, or
  the skill adds friction without enough benefit.
- **Retire** only when the no-skill condition meets the required criteria on
  representative and held-out cases, including relevant edge and safety cases.
- **Inconclusive** when controls, sample coverage, or scoring evidence cannot
  support a decision.

Deliver a concise report with scope, cases and exclusions, controls, results,
uncertainty, failures, recommendation, and next evaluation step. Preserve the
case set and score rubric so later skill versions can be compared fairly.

## Guardrails

- Do not edit, disable, delete, publish, or replace the evaluated skill as part
  of evaluation unless separately requested.
- Do not claim causality if model, prompt, tools, or task conditions differed.
- Do not hide failed runs, safety issues, or missing cases in averages.
- Do not present heuristic scores as objective truth.
- Respect task permissions and isolate side-effecting runs; use safe fixtures
  rather than live accounts or production data.
