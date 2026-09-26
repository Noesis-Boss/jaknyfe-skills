---
name: newsworthiness-check
description: "Assess whether a current event or an organization's announcement merits earned-media attention. Use when asked if a story is newsworthy, worth pitching, or worth commenting on."
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Newsworthiness Check

Give an honest editorial assessment, not promotional reassurance. Separate whether the event matters from whether this organization has a credible reason to speak about it.

## Choose the mode

- **Event commentary:** Is a public event worth commenting on for this user or organization?
- **Organization announcement:** Is the user's launch, result, research, milestone, or proposed angle genuinely useful to a defined audience or journalist?

If the prompt includes both a news event and an attached brand angle, assess the event first and the proposed angle second.

## Evidence workflow

1. Extract the claim, date, source links, intended audience, the user's connection or expertise, and any proof supplied. Mark missing facts; do not fill them in.
2. For current or time-sensitive claims, call `news-search` to check publication dates, pickup, framing, and whether coverage is saturated or stale. Prefer primary sources and reporting with visible dates. If search or evidence is unavailable, lower confidence and name the limitation.
3. Give two separate 1–10 scores: **story significance** (how much the event or announcement matters to its audience) and **pitch fit** (the user's credible standing, audience relevance, and useful contribution). Do not let a major story inflate a weak personal fit.
4. Apply the caps and hard stops. Explain the closest score anchors and why each score is not higher or lower.
5. Recommend one next move. Do not send a pitch or publish commentary.

## Story-significance score anchors

| Score | Meaning | Typical anchor |
|---|---|---|
| 9–10 | Historic or exceptional; broad, lasting public impact | Major constitutional rupture or a globally consequential event |
| 7–8 | Major national or sector-wide development with substantial evidence | Systemic failure, major ruling, or category-changing launch |
| 5–6 | Significant to a defined industry or audience; credible pickup is plausible | Material policy shift, verified large-scale result, or notable departure |
| 3–4 | Routine but potentially useful to a narrow trade audience | Standard funding, ordinary partnership, or incremental launch |
| 1–2 | Mostly self-promotional or relevant only to the organization | Anniversary, routine update, or generic opinion |

Use the closest anchor, not the most flattering one. High scores should be unusual. Neither score predicts coverage probability.

## Score the pitch fit separately

Assess direct expertise or authority, relevance to the target audience, evidence the user can add, and whether the angle serves a public or editorial interest beyond self-promotion. State what is known and what is only an inference. Do not invent article counts, audience impact, timing, or likely placement.

## Caps and hard stops

Apply these after the initial assessment:

- No credible standing or meaningful audience fit: **pitch fit is at most 4/10**.
- A central announcement claim lacks evidence: **story significance is at most 4/10**.
- A stale event has no new development: **pitch fit is at most 5/10**.
- Only one uncorroborated source supports a central claim: confidence is low; do not call it verified.
- Purely promotional framing lowers story significance; do not disguise advertising as news.
- Active tragedy or human suffering used for brand attention: **AVOID**. Do not suggest a promotional angle. Only consider adjacent commentary when the user has direct expertise and a clear public-interest contribution.
- If an active incident, legal threat, safety issue, or regulated claim is involved, pause routine pitching and identify the need for qualified crisis, legal, or compliance review.

Fabricated quotes, credentials, statistics, sources, or personal connections are never acceptable.

## Verdicts

- **Event:** `RIDE` (credible fit and open window), `WAIT` (important evidence or timing is unresolved), `SKIP` (weak fit, low significance, or saturated), or `AVOID` (a hard stop applies).
- **Announcement:** `PITCH` (merits preparing a tailored pitch, not sending it), `REVISE` (a credible story may exist after specific evidence or framing changes), or `HOLD` (not ready or not news).

A `PITCH` verdict is not permission to send. A human must review the final message and each proposed recipient.

## Output

Return concise Markdown:

1. **Scores and verdict:** mode, story-significance score, pitch-fit score, verdict, and confidence (`high`, `medium`, or `low`).
2. **Reasoning:** closest score anchors; story significance versus user fit; strongest supporting evidence; and why neither score is higher or lower.
3. **Evidence:** direct source links and dates, plus anything that remains unverified.
4. **Limits:** freshness, pickup, source-quality, standing, or proof gaps.
5. **Next move:** one concrete action, or a clear instruction to hold or avoid. Tie any suggested revision to a weak dimension.

Use `news-search` for linked current coverage. Cite direct sources; never cite a search snippet as if it were an opened source. Do not draft a pitch unless separately asked. If asked to create publishable copy, use `hook-generator` for a required opening line where applicable and require a `voxwerx` risk score below 20 before posting. This skill does not send or post.

## Provenance

Zo-native rewrite inspired by the assessment workflow in [Newsjack's `newsworthiness-check`](https://github.com/elvisun/newsjack/blob/main/skills/newsworthiness-check/SKILL.md). Newsjack is MIT-licensed. Search and evidence steps use Zo-native tools; the Newsjack CLI and Medialyst are not required.
