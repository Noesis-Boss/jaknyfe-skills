# Review Protocol

## Verification hierarchy

Prefer evidence over self-report. In order: (1) artifacts in the workspace (new files, commits, wiki updates), (2) public artifacts (fetch profile links — new posts, repos, pages), (3) user's account. When only self-report is available, note it.

## Follow-through scoring

- Follow-through rate = done ÷ (done + expired + still-open-past-due) for items due since the last review.
- Track the trend across reviews. A falling rate with a growing commitment count means over-committing — recommend fewer, smaller commitments, and record that in the retro notes for the playbook.

## Stale-bet rules

- Open past due, no progress, no renewed reason → recommend kill by default; the user must argue to keep it.
- Kept items must get either a smaller scope or a nearer date — never an unchanged re-commit twice in a row.
- Watchlist items unchecked for 3+ reviews → retire or automate the check.

## Drift checks

1. **Goal drift** — does recent activity serve the profile's stated goals? Name the top mismatch.
2. **Positioning drift** — does new public output reinforce the known-for map, or blur it?
3. **Input/output balance** — research and ideas vs shipped proof. Flag when consumption/planning outpaces publishing for 2+ reviews.
4. **Constraint violations** — commitments exceeding stated hours/week or budget.

## Report format (`reviews/YYYY-MM-DD-review.md`)

```markdown
# Growth Review — YYYY-MM-DD

## Scoreboard
Follow-through: X% (prev: Y%) · Commitments open: N · Killed this review: N · Proof shipped since last: N

## What shipped
- item — evidence link/path

## Killed / expired
- item — why, lesson if any

## Pipelines
**Proof assets:** status summary + the single most important next ship
**Learning roadmap:** gaps closed / still blocking
**Watchlist:** triggers fired, items retired

## Drift warnings
- plain-language flags

## Next period commitments (max 3)
| Commitment | Due | Why this is highest-leverage |

## Notes for next retro
- observations about what advice/format worked or didn't
```

## Guardrails

- Max 3 new commitments per review. Fewer if follow-through is under 50%.
- Every commitment must trace to a profile goal.
- If the user seems discouraged, shrink the next commitment until it's un-failable — momentum beats ambition.
