---
name: local-business-ai-setup
description: "Generate an AI adoption plan for a local business: the 5 highest-value AI tasks, concrete setup steps, pricing (what tools cost + what to charge if selling the service), and a plain-language owner pitch. Use when the user says 'set up AI for a [type of local business]', 'AI plan for a business owner', or gives a business type and wants tasks/pricing/pitch. Ends with a one-question-at-a-time interview to tailor the plan."
compatibility: "Created for Zo Computer"
metadata:
  author: "jaknyfe.zo.computer"
---

# Local Business AI Setup

Origin prompt (extracted from sticker image, 2026-09-07):

> "I want to set up Claude for a local [BUSINESS TYPE]. Build the 5 highest-value tasks, setup steps, pricing, and a plain-language owner pitch. Then interview me one question at a time until you have enough context."

## When to Use

- User names a business type (e.g. "landscaping company", "dental office", "auto repair shop") and wants an AI setup plan.
- User wants to pitch AI services to a local business owner.
- User asks for "highest-value AI tasks" for a small/medium local business.

## Workflow

1. **Get the business type.** If not stated, ask one question: "What type of business?" Do not proceed on a guess.
2. **Ask follow-ups one at a time** — only until you have enough context. Required minimum: business type, approximate size (solo/2-10/10+ staff), and the owner's tech comfort level. Optional, ask only if it changes the plan: budget, whether the user is the owner or selling to them, current tools in use. Never ask more than 5 questions total.
3. **Build the deliverable** — a single markdown document with exactly these sections:
   - **5 Highest-Value Tasks** — ranked, each with: what it is, time saved per week (estimate with stated assumption), and the specific tool(s) to use. Prefer free/cheap tiers. No speculative tasks.
   - **Setup Steps** — numbered, plain-language, one step per action, in the order the owner should actually do them. Include realistic time per step.
   - **Pricing** — two views: (a) what the tools cost the business per month, (b) if the user is selling this as a service, a suggested one-time setup fee + monthly retainer range. Label both.
   - **Plain-Language Owner Pitch** — 150 words max, no jargon, no AI hype. Lead with the money/time outcome, not the technology.
4. **Deliver the interview questions one at a time in chat** before finalizing if context is missing; the document is written after the interview, not before.
5. **Save output** to `local-business/<business-slug>/AI-SETUP.md` in the workspace (create the folder if needed) and give the user the path.

## Rules

- Plain language throughout — the reader is a business owner, not a technologist.
- Estimates must carry a one-line assumption (e.g. "assumes 30 inbound calls/week").
- Recommend at most one paid tool per task unless the free tier genuinely can't do the job.
- If the business type is regulated (medical, legal, financial), add a short compliance caution line in the relevant task entry.
- Never invent local market data; label any local-pricing assumption as an assumption.
