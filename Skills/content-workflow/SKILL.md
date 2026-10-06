---
name: content-workflow
description: "Coordinate end-to-end content creation across research, briefing, drafting, verification, review, repurposing, and measurement. Use when creating or improving external content or defining a reusable content workflow."
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Content Workflow

Run this workflow for articles, newsletters, social posts, video scripts, campaigns, and other external-facing content. Route work through existing skills; do not duplicate their procedures or create content just to fill a calendar.

## Intake and scope

Establish the deliverable, audience, purpose, channel, source material, desired reader action, deadline, voice, constraints, and success measure. Ask only for missing details that materially affect the result; otherwise state reasonable assumptions. Use the user's existing brand and writing samples when available. Check for related existing content before proposing a new piece.

Create a short brief with:

- Audience and the problem or question they have.
- One reader outcome and one primary message.
- Evidence available, evidence still needed, and claims to avoid.
- Format, channel, voice, length, call to action, and constraints.
- A measurable success signal and review date.

## Research and editorial decision

For current events, recent claims, or time-sensitive subjects, use `news-search`; distinguish source reporting from analysis, cite direct sources, and state search limits. Use `newsworthiness-check` when deciding whether a current event or announcement merits commentary or pitching. For other factual work, gather primary sources and reliable evidence appropriate to the topic. Do not invent facts, quotes, personal experience, credentials, statistics, or sources. If a central claim cannot be verified, remove it, qualify it, or mark it for human resolution.

Use `content-brief` for a substantial piece that needs an outline, SEO plan, or production specifications. For a small, clear request, proceed with the short brief above instead of adding ceremony.

## Draft

Use `content-engine` for the first draft and `social-content` when platform-native social structure is important. Make one piece the canonical source when producing multiple formats. Keep the content useful on its own, specific to the audience, and aligned with the stated goal. Use `hook-generator` for required opening lines on X posts and other applicable surfaces. Do not optimize for attention at the expense of accuracy or reader value.

## Verify and edit

Before a draft is considered review-ready:

1. Use `verify-claims` or direct source checks for material factual claims; maintain a compact claim-to-source list for substantive pieces.
2. Check audience fit, purpose, structure, readability, accessibility, CTA, platform limits, and required disclosures.
3. Use `voxwerx` on external-facing copy. Preserve the writer's voice and facts; make minimum effective edits. Its AI-pattern risk score must be below 20 before posting under the workspace publishing rule. The score is an editorial gate, not evidence of authorship or factual correctness.
4. Use `eval-content` only when its runner and required inputs are available and appropriate. Treat unavailable Claude-specific paths or brand-profile dependencies as unavailable; do not report their scores as if run. Perform the relevant checks directly and disclose that limitation.
5. Present unresolved claims, assumptions, and material tradeoffs for human judgment.

## Human approval and distribution

Return the final draft, sources or claim notes, the intended channel, and any open decisions. Do not publish, schedule, send, or pitch without explicit approval of that specific copy and destination. User approval to draft is not approval to distribute. For X, follow the workspace account rule and use the required username when the user has authorized a post. For Content360, prepare as a draft unless the user explicitly approved scheduling or publication. Never bypass a project-specific approval gate.

## Repurpose and measure

Use `content-repurpose` when adapting an approved canonical piece to other channels. Preserve its supported claims while changing structure for each channel; do not treat a derivative as approved merely because its source was. Set one primary measure and a review window suited to the channel. After publication, use actual available results (for example, clicks, qualified replies, saves, conversions, or completion) as evidence; separate measured results from interpretation. Record useful learning in the next brief or content plan. Do not invent benchmarks or imply causal impact from weak data.

## Lean path

For a simple one-off post: short brief → draft → hook if applicable → claim check → VoxWerx → human approval. Add research, a formal brief, evaluation, repurposing, or measurement only when the content's stakes or scope warrant it.
