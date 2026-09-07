# ScholarSearch — Maximum Outreach Marketing Plan

_Live: https://noesisgroup.com/scholarsearch/ · 8,255 scholarships · 31 categories · AdSense-monetized_

## 1. Situation Snapshot

**Assets we already have (free leverage):**
- 8,255 scholarships across 31 categories (Masonic, STEM, diversity, state-based, etc.) in a clean SQLite DB — perfect for programmatic SEO.
- Working React/Vite site deployed on noesisgroup.com (subpath `/scholarsearch/`).
- Google AdSense integrated → **traffic = revenue**. Every new visitor compounds.
- Don's existing distribution muscle: 3 X accounts (`@jak_nyfe`, `@jaknyfe`, `@zdsentry`), a 3-agents-×-3×-daily X growth cadence, 22 automations, Resend email, and Zo Space.
- A proven weight-loss funnel playbook (free front-door → paid) we can mirror.

**The one constraint that shapes everything:** the site lives on a subpath of noesisgroup.com, not a branded domain. For maximum outreach we should (a) maximize organic search to that URL and (b) build a branded capture surface (newsletter) we own.

## 2. Goal & North-Star Metric

- **Primary goal:** Maximize *reach* (unique visitors) to ScholarSearch.
- **North-star:** Monthly unique visitors (UV).
- **Secondary:** AdSense impressions/revenue · email subscribers · scholarship detail-page views.
- **Targets (stretch):** 10k UV/mo by day 90 · 50k by month 6 · 200k by month 12.

## 3. Audience (primary → secondary)

1. **Students** (HS juniors/seniors + current undergrads) — highest intent, hardest to reach organically except via search.
2. **Parents/guardians** — control the search行为, very reachable via Facebook groups & email.
3. **Masonic / fraternal networks** — our unique differentiator (deep Masonic scholarship data); reachable via lodges & affiliated orgs.
4. **Counselors & financial-aid offices** — amplifiers (they repost to hundreds of students).

## 4. Channel Strategy (ranked by outreach leverage)

| # | Channel | Reach | Effort | Cost | Time-to-impact | Why |
|---|---------|-------|--------|------|----------------|-----|
| 1 | **Programmatic SEO** (category/state/demographic landing pages + schema) | Very High | Med | $0 | 1–3 mo (compounding) | Free, durable, matches our data; feeds AdSense |
| 2 | **X/Twitter automation** (existing 3-agent cadence) | High | Low | $0 | Immediate | Muscle already built; founder-led + bot posting |
| 3 | **TikTok / Reels** ("scholarship of the day") | Very High | Med | $0–paid | 2–6 wks | Students live here; short-form travels |
| 4 | **Reddit & communities** (r/Scholarships, r/college, Masonic subs) | High | Med | $0 | 1–4 wks | Value-first seeding, high trust |
| 5 | **Email newsletter** (lead magnet = matched scholarships) | Med (owned) | Low | $0 | 2 wks | Converts visitors into repeat reach |
| 6 | **Partnerships** (lodges, counselors, aggregators) | High | High | $0–barter | 1–3 mo | Borrowed audiences, backlinks (SEO boost) |
| 7 | **Paid (Meta/TikTok/Search)** | High | Med | $$ | Immediate | Scale what organic proves; budget-gated |

**Insight:** Channels 1 + 2 + 3 are the outreach multipliers. 1 compounds for free; 2 is already running; 3 unlocks the student demo we can't reach via search alone.

## 5. 90-Day Phased Plan

### Days 1–30 — Foundation & Engine
- [ ] **SEO groundwork:** generate programmatic landing pages from the DB — one per category, per US state, and high-value demographic combos ("Women in STEM scholarships in Texas"). Add `FAQPage` + `JobPosting`/`EducationalOccupationalProgram` schema. (This is the single biggest outreach lever.)
- [ ] **Fix crawlability:** submit `/scholarsearch/` + sitemap to Google Search Console; internal links from noesisgroup.com homepage.
- [ ] **Launch X distribution:** repurpose one agent stream (or add a 4th) to post 1–2 scholarship opportunities/day from a dedicated handle, threading "how to apply." Use the `hook-generator` skill for first lines.
- [ ] **Stand up newsletter capture:** Zo Space lead-capture page → Resend. Offer "3 scholarships matched to you" as the hook.
- [ ] **Baseline analytics:** GA4 + Search Console + AdSense dashboard; set UV target.

### Days 31–60 — Community & Short-Form
- [ ] **TikTok/Reels:** 1 "scholarship of the day" vertical clip/day (template + CapCut). Cross-post IG/Shorts.
- [ ] **Reddit seeding:** weekly value posts in r/Scholarships, r/college, state subs, Masonic communities — never spam, always lead with a real list.
- [ ] **Masonic partnership push:** email 50 lodges/Grand Lodges with a co-branded "free scholarship finder" offer + backlink ask.
- [ ] **Newsletter:** first 4 issues; track open/click.

### Days 61–90 — Paid Scale & Optimize
- [ ] **Paid test:** $10–20/day Meta/TikTok to top-performing Reels; $5–10/day Search ads on "scholarships for [category]". Scale winners only.
- [ ] **Counselor program:** free embeddable widget/links for school sites (backlinks + reach).
- [ ] **Double down on SEO winners:** expand the best-performing category/state pages; prune dead links (DB has `url_status` flags).
- [ ] **Review & reset targets** off real UV/AdSense data.

## 6. Content Engine (repeatable)
- **Scholarship-of-the-day:** 1 post/day (X thread + Reel + newsletter slot). Pulls from DB by deadline proximity.
- **Category digests:** weekly "10 nursing scholarships closing soon."
- **Deadline reminders:** email 14/7/3 days before a saved scholarship closes.
- **Founder POV:** Don's `@jak_nyfe` posts mission/win stories (trust, not just links).

## 7. Using the Zo Stack (already paid for)
- **X automations** → daily scholarship posts (extend existing 3-agent cadence).
- **Zo Space** → branded newsletter landing + deadline-reminder signup (owns the audience).
- **Resend** → newsletter + deadline emails (free tier covers early scale).
- **Multi-account X** → separate "ScholarSearch" voice from `@zdsentry`/personal to avoid audience bleed.
- **22 automations** → repurpose one for the SEO-page generator + link-health checker.

## 8. Quick Wins (this week)
1. Submit sitemap to Search Console + link from noesisgroup.com homepage.
2. Spin up the newsletter capture page on Zo Space.
3. Queue 7 days of "scholarship of the day" X posts via automation.
4. Post one value-first thread in r/Scholarships.

## 9. Measurement
- GA4 (UV, engaged sessions), Search Console (impressions, CTR, rankings), AdSense (RPM, revenue), Resend (subs, open rate).
- Weekly 15-min review; kill what doesn't reach, double down on what does.

## 10. Assumptions & Open Questions (tell me to refine)
- **A1 — Budget:** assuming $0–$500/mo to start (organic-first). Confirm if paid can be larger.
- **A2 — Branded domain:** assuming we keep the subpath for now. A branded domain (scholarsearch.org) would lift CTR/trust — worth it?
- **A3 — Primary audience:** assuming students + parents + Masonic networks (per our data edge). Confirm priority.
- **A4 — Account to post from:** assuming a dedicated ScholarSearch X handle vs. reusing `@zdsentry`. Your call.

**Want me to execute the top quick wins next?** I can (a) generate the programmatic SEO landing pages, (b) build the Zo Space newsletter capture, and (c) wire the daily X scholarship automation.
