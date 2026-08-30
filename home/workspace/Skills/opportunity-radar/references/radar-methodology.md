# Radar Methodology

## Signal types to hunt

1. Platform changes · 2. New APIs · 3. New AI model capabilities · 4. New open-source tools · 5. Communities with repeated pain · 6. Search trends · 7. Regulatory/compliance changes · 8. Broken workflows · 9. New marketplaces · 10. Creator/business behavior shifts · 11. Expiring/abandoned tools · 12. Newly available public datasets · 13. Pricing changes or enshittification by incumbents · 14. New distribution channels · 15. Developer ecosystem shifts · 16. Niche communities asking for the same thing repeatedly.

## Sources (use ≥5 distinct types)

Official changelogs and developer docs; GitHub repos and issue trackers; Hacker News; Reddit; Discord/forums when accessible; Product Hunt and launch sites; app marketplaces (Chrome Web Store, VS Code Marketplace, Shopify, WordPress, Zapier/Pipedream/n8n); Google Trends or equivalents; keyword tools/search autocomplete; job posts and freelance listings; government/regulatory sources; public datasets; competitor sites, pricing pages, reviews, support forums; "alternatives to X" / "X is broken" / "X sucks" / "looking for X" / "how do I automate X" searches. Do not rely on social media hype alone.

## Search patterns (adapt to domain)

- `[new API/platform]` + changelog / use cases / limitations / examples / pricing / GitHub issues / Reddit / "how do I" / "alternative"
- `[industry]` + "spreadsheet" / "manual process" / "template" / "compliance" / "new rules" / "pain points" / "software sucks" / "looking for tool"
- `[workflow]` + "Zapier" / "n8n" / "Pipedream" / "API" / "CSV" / "scrape" / "OCR"
- `[tool]` + "pricing increase" / "shutting down" / "alternatives" / "reviews" / "feature request"

## Special focus: broken workflows

Actively hunt workflows still running on spreadsheets, screenshots, copy/paste, email chains, PDFs, manual reporting, CSV exports, messy Airtable/Notion bases, Zapier duct tape, Slack chaos, recurring checklists, inbox triage, human review queues, outdated portals, compliance paperwork, OCR-able documents, public records, repetitive research. These usually beat flashy AI demos.

## Special focus: platform/API changes

Ask: what was impossible or expensive before? What can now be automated? What new data became available? What workflow got 10x easier? What tools become obsolete? What small tool, template, directory, dashboard, or agent can ride the change? Which user group will discover the capability slowly and need help?

## Special focus: community pain

Look for repeated phrases: "Does anyone know a tool for…", "I hate doing…", "Is there a way to automate…", "We still use a spreadsheet for…", "This takes me hours…", "I built a hacky script…". Quote or paraphrase briefly and link to the source.

## Quality filter — reject:

Generic AI wrappers with no distribution advantage; problems big companies already solve well; enterprise-sales-dependent ideas (unless requested); ideas needing big teams, legal departments, or massive proprietary data; no identifiable buyer; interesting-but-not-urgent pain; scraping sites that prohibit it; trendy-but-unevidenced ideas; no plausible path to first users; too broad for a first product; ideas requiring model capabilities that don't reliably exist. Also reject anything violating the profile's constraints or anti-positioning.

## Scoring rubric (1–10 each, total = average)

1. Pain intensity · 2. Timing advantage (why now?) · 3. Evidence strength · 4. Solo-buildability · 5. Data availability · 6. Distribution path · 7. Monetization clarity · 8. Competition gap · 9. Workflow frequency · 10. Proof-of-value speed.

Add an 11th lens from state: **Personal fit** — does it use profile strengths and serve profile goals? Report it alongside the total but don't bury a great opportunity for fit alone; flag the mismatch.

Verdicts: **Build now / Research more / Watchlist / Ignore**.

## Opportunity record format

```markdown
## [Opportunity Name]
**Verdict:** … **Score:** X/10 **Opportunity type:** …
**Target user:** · **Pain:** · **Why now:** · **Evidence:** (links)
**What changed:** · **Current bad workaround:** · **Proposed product:**
**MVP scope:** · **Data/API needs:** · **Distribution path:** · **Monetization path:**
**Risks:** · **Why this might fail:** · **Fast validation test:** · **First build step:**
**One-sentence pitch:**
```

For each strong opportunity propose 3 buildable versions — tiny (weekend), useful MVP, ambitious — each with user, core feature, input, output, data source, tech/API requirement, why someone would use it, what to build first.

## Output order

1. **Research digest** — what changed, sources checked, strongest/weakest signals, uncertainties (with links)
2. **Signal map** — table: Signal | Source | What changed | Opportunity implication | Strength
3. **Ranked opportunities** — table: Rank | Opportunity | Score | Verdict | Target user | Why now | MVP
4. **Detailed records** (format above)
5. **Best 3 bets** — why better, what to validate first, what NOT to build yet, 7-day validation plan, MVP build plan, first public proof-of-work artifact
6. **Watchlist** — items + revisit triggers
7. **Rejected ideas** — and why
8. **Next research queries** — exact searches
9. **Builder action plan** — today / this week / this month
