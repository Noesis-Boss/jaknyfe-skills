# Growth Engine State Schema

All state lives in `growth-engine/` at the workspace root. Plain markdown. Every skill: (1) reads `playbook.md` and `profile.md` before acting, (2) writes results back, (3) appends verdicts/commitments to `decision-log.md`.

## profile.md

```markdown
# Builder Profile
Last updated: YYYY-MM-DD

## Identity
Name, one-line self-description, location/timezone if relevant.

## Skills & stack
Languages, frameworks, tools, platforms. Mark strongest.

## Projects
| Project | What it is | Status | Link | Proof value |

## Public presence
| Platform | Handle/URL | Audience size | Notes |

## Goals
- Career: ...
- Monetization: ...
- Audience: ...
(each with target + timeframe when known)

## Constraints
Time/week, budget, energy, work status, hard limits.

## Target audience
Who the work should attract.

## Tone & voice
Preferred tone; phrases that fit; phrases to avoid.

## Anti-positioning
What the user refuses to become. Treat as hard constraints.

## Confidence notes
Items marked (inferred) need user confirmation.
```

## playbook.md

The self-improvement memory. Skills MUST read and obey it.

```markdown
# Playbook
Last retro: YYYY-MM-DD

## Directives (obey these)
- Numbered, imperative rules learned from retros.

## What works
- Pattern — evidence — since when

## What doesn't work
- Pattern — evidence — decided when

## Open experiments
| Experiment | Hypothesis | Started | Check by | Result |
```

## watchlist.md

```markdown
| Item | Why it matters | Trigger signal | Where to monitor | Added | Last checked | Status |
```

Status: watching / triggered / retired.

## decision-log.md

Append-only. Never rewrite history; update Status in place only.

```markdown
| Date | Skill | Decision/Commitment | Due by | Status | Outcome notes |
```

Status: open / done / killed / expired.

## proof-assets.md

```markdown
| Proof asset | Purpose (what claim it supports) | Format | Status | Next step | Impact 1-5 | Link |
```

Status: idea / in progress / published / retired.

## learning-roadmap.md

```markdown
| Skill gap | Blocks which opportunity/goal | Learning resource/plan | Status | Evidence of progress |
```

## positioning.md

Current positioning statement, one-liners, bio variants, content pillars, known-for map, anti-positioning, and the latest 10-dimension score with date. Keep prior scores in a history table at the bottom.

## reviews/YYYY-MM-DD-review.md

Output of each growth-review run (see growth-review skill).

## wikis/<niche-slug>/

One folder per niche researched by niche-wiki.
