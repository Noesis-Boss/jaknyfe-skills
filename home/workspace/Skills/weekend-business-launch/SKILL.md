---
name: weekend-business-launch
description: Orchestrate a lean weekend business launch from idea to first customers. Use whenever the user wants to pressure-test a business idea, create an offer, name or brand it, write a landing page, choose a no-code stack, find first customers, or plan launch day. Run the smallest gated path and stop building when evidence is insufficient.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  category: business
---

# Weekend Business Launch

Move one business idea through seven gated stages. The goal is a credible test and first customer conversations, not a polished business or guaranteed income.

## Operating rules

- Start with one idea, one audience, one painful job, and one offer.
- When the user supplies a collection of business prompts, use `business-prompt-system` to select and sequence only the stages needed.
- Separate facts, assumptions, hypotheses, and recommendations.
- Use the existing specialist skills when available: `find-moneymaking-biz`, `customer-validation`, `low-ticket-offer-architect`, `brand-builder`, `copywriting`, `no-code-mvp-builder`, `product-delivery-builder`, `growth-setup`, `launch-strategy`, `launch-metrics`, and `hook-generator`.
- Do not duplicate work already produced in the current conversation.
- Do not publish, send outreach, create payment products, or spend money unless the user explicitly requests that action.
- Reject fabricated proof, fake scarcity, guaranteed outcomes, spam, and unverified domain or platform claims.

## Intake

Ask only questions that materially change the plan: idea, target buyer, available time, budget, relevant experience, delivery format, launch deadline, and desired result. If the user gives enough context, proceed and label assumptions.

## Capability routing

Before running a stage, classify the work and activate only the needed specialists. Inspect the available skill descriptions first; read a specialist's full instructions only when its capability is required.

- **Unclear idea or offer:** `brainstorming`, then `customer-validation`.
- **Validated business and pricing:** `low-ticket-offer-architect`, `business-plan-builder` when financial modeling is needed.
- **Brand and customer-facing page:** `brand-builder`, `copywriting`, and `frontend-design` when a page must be designed or implemented.
- **Working MVP:** `no-code-mvp-builder`; add `product-delivery-builder` for onboarding, fulfillment, support, or refunds.
- **Admin, reporting, or customer portal:** add a dashboard-specific skill only when the requirement exists; otherwise do not create dashboard scope.
- **Acquisition and launch:** `growth-setup`, `launch-strategy`, `launch-metrics`, and `hook-generator` for feed-opening copy.

Record the selected skills, why each is needed, dependencies, and the skills deliberately skipped. Do not run a specialist merely because it is available.

## Seven gates

### 1. Pressure-test the idea

Identify the buyer, urgent pain, why now, current workaround, reachable channels, three failure reasons, and the leanest 48-hour test. Recommend one idea only when comparing several.

Use `customer-validation` to define the riskiest hypothesis and the evidence threshold before building. If the idea or audience is unclear, activate `brainstorming` first.

### 2. Lock the offer and price

Use `low-ticket-offer-architect`. Define one outcome, deliverables, exclusions, delivery burden, good/better/best tiers when justified, objections, and a paid validation threshold.

### 3. Name and brand it

Use `brand-builder` for the minimum credible message, visual kit, proof treatment, and CTA. Treat domain availability as unverified until checked live.

### 4. Write the landing page

Use `copywriting` when it is functional; otherwise produce a lean page with headline, audience/problem, outcome, proof or honest newness, offer, objections, CTA, refund/privacy notes, and no unsupported claims.

### 5. Choose the no-code MVP path

Use `no-code-mvp-builder`. Choose the fewest tools needed for landing page, payment or signup, email/contact, delivery, and measurement. Verify current availability and free-tier limits before asserting them. Give a numbered build order and a manual fallback.

Use `product-delivery-builder` to define onboarding, intake, fulfillment, support, refunds, capacity, and the purchase-to-outcome test.

### 6. Line up first customers

Use `growth-setup` when appropriate. Select up to three audience-owned channels, write useful non-spam outreach, define daily volume, response handling, qualification questions, and a stop rule. Do not send messages automatically without explicit permission.

### 7. Plan launch day

Use `launch-strategy` and `launch-metrics`. Include timezone, exact publishing order, channel-specific copy, one measurable goal, technical checks, capacity limit, funnel tracking, and an end-of-day review. Route feed-opening copy through `hook-generator` when required.

## Gate behavior

After each stage, report `PASS`, `HOLD`, or `FAIL`:

- `PASS`: enough evidence and a clear next action.
- `HOLD`: one missing decision or validation step.
- `FAIL`: the idea, offer, or path is not credible under stated constraints.

Do not advance past `HOLD` or `FAIL` unless the user explicitly chooses to accept the risk.

## Default output

# Weekend Business Launch Brief
## Inputs and assumptions
## Gate results
## Recommended business test
## Offer and pricing
## Minimum brand and landing page
## No-code build order
## First-customer plan
## Launch-day playbook
## Risks and deferred work
## Next smallest action

Success means the user has one testable offer, one working path to action, a truthful message, a measurable goal, and a bounded next step. It does not mean revenue has been proven.
