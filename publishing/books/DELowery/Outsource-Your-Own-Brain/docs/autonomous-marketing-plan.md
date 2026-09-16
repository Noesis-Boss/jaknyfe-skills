# Autonomous Marketing Plan

**Product:** *Outsource Your Own Brain: How Solopreneurs Delegate Cognitive Labor and Keep the Thinking That Matters*

**Author:** D.E. Lowery, MBA

**Plan date:** 2026-09-16

## Decision

Build a post-publication marketing loop that runs without per-engagement human approval after one-time setup. The system should maximize qualified reach, not raw message volume. It may publish, test, optimize, and stop campaigns automatically inside fixed policy, rate, privacy, and budget limits.

The system must not send unsolicited bulk messages, fabricate endorsements, manipulate reviews, scrape personal contact data, impersonate the author, or distribute the Kindle book outside Amazon while KDP Select exclusivity applies.

## Live listing audit

Audited 2026-09-16 through the public Amazon.com product page and search results.

| Edition | ASIN | Price | Status |
|---|---|---:|---|
| Kindle | `B0HG9NB8PD` | `$6.99` | Live; Kindle Unlimited included |
| Paperback | `B0HG9JGW6D` | `$17.99` | Live; linked format |

The listing is categorized under business/computer science/artificial intelligence/generative AI. The public page showed no customer-review proof at audit time. Use the Kindle product URL as the primary campaign destination:

`https://www.amazon.com/Outsource-Your-Own-Brain-Solopreneurs-ebook/dp/B0HG9NB8PD`

## Audience model

Start with the book's documented audience, then expand by adjacent problem rather than by indiscriminate targeting.

1. **Core:** AI-curious solopreneurs: consultants, writers, coaches, and designers.
2. **Adjacent:** freelancers, small-agency owners, independent educators, creators, and knowledge workers drowning in context switching.
3. **Problem audiences:** people discussing AI productivity, prompt overload, delegation, attention fragmentation, decision quality, workflow design, and responsible AI use.
4. **Professional audiences:** founders and operators who need repeatable systems but do not want to surrender judgment to automation.

The system should score audience relevance from the topic being discussed, not infer sensitive traits or build identity profiles.

## Operating architecture

### 1. Source library

Create a structured content library from the canonical manuscript, KDP metadata, the cover, and verified author material.

Each source unit stores:

- chapter and section reference;
- claim type: principle, example, process, question, or quotation;
- approved paraphrase;
- prohibited overclaim;
- audience tags;
- source URL when an external fact is used;
- expiration or review date for time-sensitive facts.

Only source units marked publishable may enter the generation queue. No invented reviews, sales numbers, client results, scarcity, or testimonials.

### 2. Content atom generator

Turn one approved source unit into channel-specific variants:

- short text post;
- short educational thread or carousel script;
- 30- to 60-second video script;
- practical checklist;
- long-form article or newsletter section;
- discussion reply;
- Amazon Ads keyword or product-targeting hypothesis.

Every atom gets a single job: discovery, education, conversation, click, or conversion. Do not reuse identical copy across channels.

### 3. Distribution lanes

**Lane A — Amazon-native discovery**

- Run Sponsored Products for the Kindle ASIN.
- Use automatic targeting for discovery and manual keyword/product targeting for winners.
- Add negative targets from search-term reports.
- Keep a separate paperback campaign only after the Kindle campaign has enough signal.
- Optimize against attributed sales, detail-page views, and read-through proxies rather than clicks alone.

**Lane B — owned public publishing**

- Publish practical, non-sales-first lessons to the author's website, public book page, YouTube, and connected social accounts.
- Every piece links to the Amazon listing or the public book showcase.
- Use a content ladder: one weekly cornerstone idea, several short derivatives, and one periodic direct invitation to buy.

**Lane C — public conversation discovery**

- Monitor public posts and communities for relevant questions.
- Reply only when the source conversation is genuinely relevant and the reply adds a useful answer before the book mention.
- Mention the book only when it directly answers the request, with one link at most.
- Never auto-reply to every keyword match, mass-comment, or hijack unrelated trending topics.

**Lane D — permission-based distribution**

- Send to the existing email list only where consent exists.
- Offer a useful excerpt, checklist, or implementation prompt before the purchase link.
- Allow unsubscribe handling automatically.
- Do not purchase, scrape, or enrich contact lists.

**Lane E — earned discovery**

- Maintain a list of podcasts, newsletters, blogs, communities, and event pages whose stated topic matches the book.
- Generate personalized, truthful pitch drafts from public submission instructions.
- Send only where the destination explicitly accepts submissions or where the channel's rules permit contact. No mass cold outreach.

## Autonomous engagement loop

Run continuously with a daily control cycle:

1. Collect permitted public signals and first-party analytics.
2. Deduplicate topics, accounts, URLs, and claims.
3. Score relevance, audience fit, freshness, safety, and likely value.
4. Select the highest-value content atoms within channel quotas.
5. Run policy checks for truthfulness, disclosure, privacy, spam risk, copyright, and KDP Select exclusivity.
6. Publish or queue automatically when all checks pass.
7. Record the exact content, channel, timestamp, destination, source units, and policy result.
8. Measure reach, saves, replies, clicks, detail-page views, ad cost, attributed sales, and negative signals.
9. Promote winning themes, suppress weak or fatiguing themes, and expire stale claims.
10. Stop a channel or campaign automatically when a safety, complaint, spend, or performance threshold is crossed.

This is an approval-free runtime, not an unbounded runtime. The controls are machine-enforced and fixed during setup.

## Default guardrails

| Control | Initial default |
|---|---:|
| Posts per public social account per day | 3 |
| Promotional posts per account per 7 days | 2 |
| Replies per account per day | 10 |
| Automated DMs | 0 |
| Cold email | 0 |
| Repeat reply to same author/thread | 1 per 30 days |
| Maximum links per public reply | 1 |
| Minimum relevance score for a book mention | 0.85 |
| Unsubscribe / opt-out handling | immediate |
| Daily ad-spend ceiling | configure before activation |
| Monthly ad-spend ceiling | configure before activation |

The system should lower quotas automatically after complaints, blocks, low-quality feedback, or unusual posting errors.

## Message rules

Every promotional asset must:

- lead with a real problem or useful insight;
- make one concrete promise that the book actually supports;
- identify the book and author accurately;
- use the current Amazon price only when fetched from the live listing;
- label affiliate relationships or sponsored placements where required;
- avoid guaranteed productivity, income, health, or career outcomes;
- avoid fake urgency and fabricated scarcity;
- avoid claims that the author has reader results unless a verified source exists;
- preserve the distinction between AI-assisted marketing copy and the author's authorship claims.

The system must never ask readers for positive reviews, offer compensation for reviews, review its own book, coordinate review exchanges, or post under a disguised identity.

## Testing and optimization

Use controlled tests with one variable changed at a time:

- problem-led hook versus identity-led hook;
- practical checklist versus conceptual explanation;
- Kindle CTA versus paperback CTA;
- chapter-specific topic versus broad AI topic;
- static cover asset versus short educational video.

Keep a variant only when it improves a predefined metric without increasing complaint, unsubscribe, block, or policy-violation rates. Do not optimize for impressions alone.

### Primary metrics

1. Qualified reach: unique people exposed in relevant contexts.
2. Engagement quality: saves, substantive replies, completion rate, and outbound click rate.
3. Amazon intent: detail-page views, sample/borrow activity where available, and attributed orders.
4. Economics: advertising cost per attributed order and contribution margin.
5. Trust: complaint rate, opt-outs, blocks, content removals, and policy exceptions.

## Suggested cadence

**Daily:** signal collection, two to three educational posts, permitted replies, ad pacing, anomaly checks, and metric logging.

**Weekly:** one cornerstone article or video, one direct book invitation, creative rotation, negative-target update, and fatigue review.

**Monthly:** audience/topic report, channel-level spend review, source-library expiry review, and automatic removal of underperforming or stale assets.

## Implementation phases

### Phase 1 — Measurement and source grounding

- Store the two ASINs and canonical product URL in configuration.
- Build the source-unit library from the manuscript and existing marketing pack.
- Add immutable claim and disclosure rules.
- Add event logging and a dry-run mode.

**Done when:** the system can generate and policy-check content without publishing.

### Phase 2 — Owned content publishing

- Connect only accounts the author controls.
- Add channel adapters, per-channel quotas, and idempotency keys.
- Publish educational content first; allow direct promotion at the defined cadence.

**Done when:** one complete week runs without duplicate posts, broken links, or policy exceptions.

### Phase 3 — Public conversation replies

- Add relevance scoring, thread-level cooldowns, opt-out detection, and reply templates.
- Start with replies that do not include a link; add the book link only when the relevance score and value threshold pass.

**Done when:** every reply has a stored source, reason code, and policy result.

### Phase 4 — Amazon Ads optimization

- Create Sponsored Products campaigns for `B0HG9NB8PD`.
- Set a hard daily and monthly ceiling.
- Import search-term reports, harvest winners, add negatives, and pause wasteful targets.

**Done when:** spend never exceeds the configured ceiling and every optimization has an audit record.

### Phase 5 — Autonomous optimization

- Add fatigue detection, channel health scoring, creative retirement, and budget reallocation.
- Permit automatic pause, not automatic risk expansion.
- Produce a weekly report without requiring an approval step.

**Done when:** the loop can run for 30 days with bounded spend, no policy incidents, and a complete audit trail.

## Required one-time setup inputs

The runtime cannot safely invent these values:

- social accounts and publishing permissions;
- email sender and consented list;
- Amazon Ads access;
- daily and monthly advertising ceilings;
- permitted geographic markets;
- disclosure text and author bio;
- notification destination for exceptions and weekly reports.

After setup, none of these should require per-post approval. A human remains the legal owner of the accounts and budget, but the normal engagement loop is autonomous.

## Explicit non-goals

- No spam campaigns or automated cold DMs.
- No mass scraping of people or private communities.
- No review manipulation or incentive exchange.
- No fake testimonials, invented analytics, or unsupported claims.
- No direct digital distribution of the Kindle book while KDP Select exclusivity applies.
- No automatic increase of ad budget after a positive signal.
- No publishing to a new channel until its terms, credentials, and rate limits are configured.

## Source notes

- The live listing audit was performed on Amazon.com on 2026-09-16.
- KDP Select currently states that the Kindle edition remains digitally exclusive to KDP during enrollment, while physical formats may continue elsewhere.
- Amazon Ads currently positions Sponsored Products as the starting point for book promotion and supports automatic and manual targeting.
