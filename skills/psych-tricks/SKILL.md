---
name: psych-tricks
description: Applies the 49 Psychological Mind Tricks framework to any requested output — sales copy, emails, landing pages, scripts, pitches, negotiations, presentations, or any persuasive communication. Takes the user's output goal, scans all 49 principles, and injects the most relevant persuasion techniques with specific phrasings. Use when the user asks to "apply psych tricks", "make this more persuasive", "infuse psychology into", or when writing any copy that needs persuasion optimization.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Psych Tricks

Applies concepts from the "49 Psychological Mind Tricks That Feel Illegal To Know" framework to any output.

## Quick start

```
bun scripts/psych-tricks.ts list        — all 49 titles
bun scripts/psych-tricks.ts detail 12   — full detail on #12
bun scripts/psych-tricks.ts search "negotiation" — search by keyword
bun scripts/psych-tricks.ts summarize   — compact summary
```

## How to use in chat

1. Read `scripts/tricks.json` for the full reference.
2. The user will describe the output they want (e.g., "write a sales email for a gym membership").
3. Scan all 49 tricks against the specific output goal.
4. Select the 3-5 most relevant principles for the output — prioritize tricks where the application field directly maps to the output type.
5. Inject each trick with a **concrete, non-obvious phrasing** — never just name the principle. Show it applied to the actual words.

Example: for a gym membership email, relevant picks might be:
- #4 (Scarcity) → "Only 3 spots left in the early-morning crew"
- #7 (Commitment/Consistency) → "Would you prefer M/W/F or T/Th/Sat?"
- #10 (Ben Franklin Effect) → "We'd love your honest feedback on our new equipment layout — just two quick questions?"
- #20 (Urgency) → countdown timer on the offer
- #3 (Social Proof) → "97 members just like you joined last month"

6. After applying the principles, explain **which tricks were used and how** as a brief wrap-up so the user can iterate.

## Reference

- `scripts/tricks.json` — full structured data for all 49 tricks (title, concept, study/examples, application)
- `scripts/psych-tricks.ts` — CLI lookup tool
- `scripts/parse-source.ts` — regenerates `tricks.json` from the source RTF
