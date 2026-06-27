# AI Project Idea Trigger Evals

## Purpose

Test whether constrained project requests invoke the skill and whether generic brainstorming, full market research, onboarding, career strategy, and enterprise architecture stay outside it.

## Manual method

1. Start a new conversation per case.
2. Submit the query without naming the skill.
3. Record invocation and routing.
4. For positive cases, check:
   - user fit and assumptions;
   - multiple relevant tiers;
   - scored and explained ranking;
   - one recommended MVP;
   - acceptance checks and failure cases;
   - a seven-day sequence;
   - a proof artifact;
   - a “not yet” boundary.
5. Repeat implicit and generic-boundary cases three times.
6. Test explicit invocation separately.

## Pass criteria

A positive output fails when it:

- returns an unranked idea dump;
- ignores device, budget, time, or skill level;
- recommends a generic chatbot by default;
- uses private data without safeguards;
- treats autonomous high-stakes decisions as beginner projects;
- scores ideas without explaining tradeoffs;
- recommends an MVP that cannot be finished;
- omits maintenance and non-goals.

## Description tuning

Add real user language to the description when relevant project requests miss. Tighten “constraints, ranking, MVP” when generic brainstorming begins to over-trigger.
