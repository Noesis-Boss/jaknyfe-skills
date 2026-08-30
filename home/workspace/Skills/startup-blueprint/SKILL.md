---
name: startup-blueprint
description: Ten-phase startup validation and blueprint system. Runs structured analysis across idea breakdown, demand validation, customer profiling, competitor analysis, positioning, offer creation, revenue modeling, go-to-market planning, risk analysis, and a complete startup blueprint. Each phase is a standalone prompt; the full sequence produces an investor-ready validation package. Use when the user says "validate my startup idea," "startup blueprint," "analyze my business idea," or references any of the 10 phases by name.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  version: 1.0.0
---

# Startup Blueprint Skill

A ten-phase system to validate, position, and plan a startup idea from first concept to investor-ready blueprint. Each phase runs as a standalone prompt; the full sequence produces a complete validation package.

## When to use

- The user has a business idea and wants structured validation
- The user asks for startup planning, market analysis, or competitive research
- The user says "validate my idea," "startup blueprint," "analyze this business"
- The user wants help with positioning, pricing, customer profiling, or go-to-market

## How to run

Replace `[IDEA]` with the user's actual idea in each prompt. Run phases in order for full validation, or run individual phases on demand.

If the user provides an idea but no specific phase, default to running Phase 1 (Idea Breakdown) first, then ask which phase they want next — or offer to run the full sequence.

---

## Phase 1: Idea Breakdown

**Prompt:**

```
I have a business idea: [IDEA]. Analyze it across the problem, target customer, value proposition, business model, required resources, competitive advantages, and key assumptions. Identify what I'm overlooking and the biggest risks I should validate first.
```

**Output:** Structured breakdown with risk flags.

---

## Phase 2: Demand Validation

**Prompt:**

```
Evaluate the real demand for [IDEA]. Identify who would pay, the problem they need solved, its urgency, current alternatives, and the strongest evidence that would prove willingness to pay. Challenge weak assumptions and be skeptical—not optimistic.
```

**Output:** Demand evidence map with willingness-to-pay indicators.

---

## Phase 3: Customer Profile

**Prompt:**

```
Create a detailed ideal customer profile for [IDEA]. Identify their goals, frustrations, buying triggers, objections, current solutions, willingness to pay, and the online platforms where they're easiest to reach.
```

**Output:** ICP document with platform targeting.

---

## Phase 4: Competitor Analysis

**Prompt:**

```
Analyze the competitive landscape for [IDEA]. Identify direct and indirect competitors, their positioning, pricing, strengths, weaknesses, target customers, and marketing strategies. Then uncover realistic market gaps and opportunities I could exploit.
```

**Output:** Competitive matrix with gap analysis.

---

## Phase 5: Unique Positioning

**Prompt:**

```
Based on the market and competitors for [IDEA], create 5 distinct positioning strategies. For each, define the target customer, core promise, differentiation, competitive advantage, and biggest risk. Recommend the strongest option and explain why.
```

**Output:** Five positioning options with recommendation.

---

## Phase 6: Offer Creation

**Prompt:**

```
Turn [IDEA] into an irresistible offer. Define what I'm selling, the customer transformation, key features, bonuses, pricing, guarantee options, and the strongest reason to buy now. Make the offer compelling, differentiated, and easy to understand.
```

**Output:** Offer sheet with pricing and guarantee structure.

---

## Phase 7: Revenue Model

**Prompt:**

```
Design 3 realistic revenue models for [IDEA]. Compare pricing, acquisition costs, margins, scalability, risks, and complexity. Recommend the best model for an early-stage business and explain why.
```

**Output:** Revenue model comparison with recommendation.

---

## Phase 8: Go-To-Market Strategy

**Prompt:**

```
Create a practical 30-day go-to-market plan for [IDEA]. Include the launch sequence, best marketing channels, content strategy, customer acquisition tactics, daily priorities, key metrics, and the fastest realistic path to the first 10 paying customers.
```

**Output:** 30-day launch plan with daily actions.

---

## Phase 9: Risk & Failure Analysis

**Prompt:**

```
Act as a brutally honest startup advisor. Try to prove why [IDEA] could fail. Identify the 10 biggest risks across demand, competition, pricing, acquisition, operations, and scalability. For each, give me a low-cost test to validate or disprove the risk before investing significant time or money.
```

**Output:** Top-10 risk table with validation tests.

---

## Phase 10: Complete Startup Blueprint

**Prompt:**

```
Using everything we've established about [IDEA], create a complete startup blueprint covering the problem, target customer, market opportunity, competitors, positioning, offer, pricing, revenue model, marketing, customer acquisition, launch roadmap, key metrics, and risks.

End with the 10 highest-impact actions I should take next. Prioritize execution, speed, validation, and measurable results over theory.
```

**Output:** Full startup blueprint with prioritized action list.

---

## Execution guidance

1. **Capture the idea first.** Before running any phase, restate the idea in one sentence and confirm it's accurate. Ambiguity here corrupts every downstream phase.

2. **Use web search liberally.** Phases 2, 4, 5, 7, and 8 especially benefit from real competitor pricing, market data, and TAM estimates. Run 2-3 targeted searches per phase where evidence matters.

3. **Build across phases.** When running the full sequence, feed outputs from earlier phases into later ones. Phase 10 should synthesize Phases 1-9 — not repeat them.

4. **Stay skeptical.** The user wants the truth, not encouragement. In Phases 2 and 9 especially, challenge weak assumptions and flag unfounded optimism.

5. **Make it actionable.** Every phase output should end with a concrete next step — not a concept, a thing the user can do today.

6. **Keep it tight.** Don't pad. If a phase produces 8 good points, 8 is enough. The user prefers dense signal over comprehensive filler.

## Output format

For each phase, structure output as:

- **Findings** — the core analysis, in plain prose or a table
- **Risks / Gaps** — what's weak, missing, or unvalidated
- **Recommendation** — the single most important takeaway (where applicable)
- **Next action** — one concrete step the user can take today

For the full blueprint (Phase 10), use a structured document with clear section headers matching the outline in the prompt.
