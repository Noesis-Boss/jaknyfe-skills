# Niche Wiki Methodology

## Objective

The wiki must let a solo builder understand: what the niche is, who the users/buyers are, painful workflows, existing tools, where the niche talks, available datasets/APIs, complaints, working business models, underserved opportunities, buildable projects, content that attracts the audience, and what to build, write, watch, or ignore.

## Sources (use ≥8 distinct types)

Official industry sources; government/regulatory sources; public datasets; APIs and developer docs; GitHub; tool directories and app marketplaces (Chrome Web Store, Shopify, WordPress, Zapier/Make/n8n); Reddit, forums, Discord; YouTube, podcasts, newsletters; job posts and freelance listings; review sites; Product Hunt; Hacker News; search autocomplete and trend tools; competitor sites, pricing pages, support docs, complaint threads; "alternatives to X" searches.

## Search patterns (adapt)

`[niche]` + tools / software / community / forum / subreddit / dataset / API / public data / directory / workflow / automation / compliance / regulations / spreadsheet / template / "how do I" / "looking for" / "pain points" / "software sucks" / "alternative" / "manual process" / "CSV" / "Zapier" / "n8n" / "GitHub" / "pricing" / "reviews" / "feature request" / "job description" / "freelance".

## Research discipline

For every major claim track: source, date accessed, why it matters, type (primary/secondary/community/commercial/anecdotal), confidence, potential bias/staleness. Separate confirmed facts / strong signals / weak signals / anecdotes / guesses / needs-validation.

## Wiki structure

```
wikis/<niche-slug>/
├── README.md                     # coverage, how to use, best opportunities & sources, next actions, limitations, update cadence
├── 00-source-log.md              # | Source | Type | Link | Date | Why it matters | Confidence | Notes |
├── 01-niche-overview.md          # what/why/who, recent changes, defining problems, vocabulary, beginner mental model, outsider misconceptions
├── 02-market-map.md              # segments, user/buyer groups, tool categories, channels, business models, adjacent + emerging subniches
├── 03-personas.md                # per persona: who, needs, current tools, annoyances, what they pay for, where to find them, attracting content, helpful product
├── 04-jobs-to-be-done.md         # | User | Situation | Job | Current workaround | Pain level | Opportunity |
├── 05-workflows-and-pain.md      # per workflow: who, trigger, process, tools, pain, frequency, automation potential, data needed, possible product, first validation question
├── 06-main-players.md            # | Player | Type | What they do | Audience | Pricing | Strength | Weakness | Link |
├── 07-tools-and-products.md      # per tool: category, user, promise, pricing, strengths, weaknesses, complaints, missing features, opportunity gap, link
├── 08-communities.md             # community table + recurring questions, complaints, beginner confusion, pain phrases
├── 09-data-sources.md            # | Source | Type | Access | Cost | Terms/Risk | Fields | Use cases | Link | — flag ToS/legal concerns
├── 10-regulations-and-risk.md    # legal/compliance/privacy/scraping/platform-dependency/liability; not legal advice; source everything
├── 11-keywords.md                # | Cluster | Example keywords | Intent | Content opportunity | Product opportunity | Difficulty guess |
├── 12-business-models.md         # | Model | Buyer | What they pay for | Price guess | Difficulty | Distribution | Risks |
├── 13-opportunity-map.md         # ranked, scored (rubric below), with verdicts
├── 14-project-ideas.md           # tiny tools, useful MVPs, ambitious projects, weird memorable machines (see record format)
├── 15-content-angles.md          # | Angle | Audience | Search intent | Why it works | Proof needed | CTA |
├── 16-learning-roadmap.md        # concepts, vocabulary, tools, communities, first 7/30/90 days, red flags
├── 17-watchlist.md               # | Thing to watch | Why | Signal to look for | Where to monitor |
└── 18-rejected-ideas.md          # why interesting, why rejected, what would change the decision
```

Merge or drop files that would be thin for this niche. Scale project-idea counts to evidence found; don't force quotas.

## Project idea record

```markdown
## [Project Name]
**User:** · **Problem:** · **MVP:** · **Input:** · **Output:**
**Data/API needs:** · **Stack suggestion:** · **Distribution path:** · **Monetization:**
**Why useful:** · **Why it might fail:** · **First build step:** · **7-day validation test:**
```

## Opportunity scoring (1–10 each, total = average)

Pain intensity · Evidence strength · Solo-buildability · Data availability · Distribution path · Monetization clarity · Competition gap · Frequency of use · Proof-of-value speed · Personal fit (from profile).

Verdicts: Build now / Research more / Watchlist / Ignore.

## Opportunity standards

Favor: useful before monetized; one-person buildable; visible pain; public data or accessible APIs; easy to explain and validate; specific audience; narrow enough to launch; weird enough to remember. Reject: generic AI wrappers; cold-start-less marketplaces; enterprise sludge; vague platforms; compliance-heavy without expertise; unavailable proprietary data; too expensive to validate; hype-only; indistinguishable from incumbents.
