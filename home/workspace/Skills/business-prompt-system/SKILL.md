---
name: business-prompt-system
description: Convert a rough business goal into a bounded sequence of prompts for discovery, validation, offer design, copy, acquisition, fulfillment, automation, and measurement. Use when the user wants to turn prompt ideas into an executable business workflow.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  category: business
---

# Business Prompt System

Turn a business goal into the smallest credible path from idea to evidence and delivery. Do not treat prompts as proof of demand or income.

## Required intake

Ask only for missing decisions that change the path: target buyer, painful job, relevant skill, available time, budget, buyer access, delivery format, income goal, deadline, and permission for external actions.

## Prompt pipeline

Run only the stages needed:

1. **Discover** — produce and pressure-test ideas with `find-moneymaking-biz`.
2. **Validate** — define the riskiest hypothesis, behavior-based test, evidence threshold, and stop rule with `customer-validation`.
3. **Package** — define one outcome, deliverables, exclusions, capacity, price, objections, and tiers with `low-ticket-offer-architect`.
4. **Present** — write truthful landing-page, lead-magnet, hook, and outreach assets with `copywriting`, `content-matrix`, `cold-outreach`, or `hook-generator` as needed.
5. **Deliver** — define intake, fulfillment, support, refunds, manual fallback, and capacity limits with `product-delivery-builder`.
6. **Automate** — automate only repeated, observable tasks after the manual path works; use `no-code-mvp-builder` when tools are needed.
7. **Measure** — track exposure, replies, qualified calls, commitments, revenue, delivery time, and capacity with `launch-metrics`.

## Stage contract

Every stage must state:

- Inputs and labeled assumptions
- Concrete output
- Evidence versus hypothesis
- Risks and exclusions
- Verification method
- Next smallest action

Use `PASS`, `HOLD`, or `FAIL` for stage status. Do not advance a `HOLD` or `FAIL` stage without an explicit user decision to accept the risk. Never send outreach, publish, charge money, or create external accounts without explicit approval.

## Quality rules

- Prefer one buyer, one painful job, one offer, and one channel.
- Replace vague goals such as “go viral” with measurable thresholds.
- Do not fabricate testimonials, demand, market size, profitability, or conversion rates.
- Keep the first test under the user's stated time and budget.
- Stop building when the evidence threshold is missed.

## Output

Return a compact Business Prompt Runbook containing the selected stages, prompts or actions, dependencies, stage gates, metrics, deferred work, and the next action. Do not generate all seven stages when a smaller path answers the request.
