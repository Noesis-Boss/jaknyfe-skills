---
name: news-search
description: "Find and verify recent news coverage about a topic, organization, competitor, or event using Zo's web tools. Use for current news—not general research, journalist contact scraping, or publishing."
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# News Search

Return a small, dated, attributed set of coverage another person can verify. Separate what a source reports from your own interpretation.

## Workflow

1. **Set scope.** Identify the topic, geography, and time period. Ask one focused question only if a missing detail would materially change the search; otherwise proceed and state the scope.
2. **Search broadly but distinctly.** For current news, use `web_search` with the news topic and a suitable time range. Run two or three meaningfully different queries in parallel—for example, the named organization, the event plus its sector, and relevant primary or local sources. Do not repeat near-identical queries to inflate results.
3. **Verify the best sources.** Open relevant publisher or primary-source pages with `read_webpage` when the date, byline, original reporting, or a central claim matters. A result snippet is a lead, not confirmation. Prefer original reporting, official records, and direct statements.
4. **Deduplicate.** Collapse syndicated copies and articles that only repeat the same press release. Use `x_search` only when the user asks about social momentum or journalist discussion; label posts separately from published reporting.
5. **Report the limits.** State the date range and search scope, note inaccessible pages or unverified details, and never imply the search is exhaustive.

## Article record

For each useful item, include:

- Headline and direct URL.
- Outlet and author/byline only if the source shows them.
- Publisher-stated publication date; distinguish it from an update date. Use `date unverified` when unclear.
- One sentence on what the article establishes and why it is relevant.

Never invent a title, outlet, byline, date, quote, or canonical URL. Keep source claims distinct from interpretation.

## Output

Lead with the search scope. Return roughly 3–8 strong, deduplicated results, or fewer when coverage is limited. Support factual claims with direct sources and numeric footnote citations; define each citation once. Say plainly when the evidence came only from snippets or when little or no coverage was found. Absence of results is not proof that no coverage exists.

## Boundaries

- Use Zo's `web_search` and `read_webpage`; do not invoke the Newsjack CLI, Medialyst, or a paid search service.
- Do not scrape or infer journalist contact details. A byline can inform beat research; it is not permission to contact anyone.
- Do not send pitches, emails, posts, or alerts. Require human review before downstream outreach.
- Do not turn tragedy or human suffering into a promotional opportunity.

## Provenance

Zo-native adaptation of [Newsjack's `news-search`](https://github.com/elvisun/newsjack/blob/main/skills/news-search/SKILL.md). This skill uses Zo's web tools and does not require Newsjack or Medialyst credentials.
