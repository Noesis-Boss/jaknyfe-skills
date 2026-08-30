---
name: gumroad-product-builder
description: Build market-validated Gumroad digital products using a 6-phase gated system — from audience research to publish-ready artifact. Validates pain points with commercial intent scoring before building. Zero-cost stack. Use when building a Gumroad product, digital template, Notion dashboard, or any info-product from scratch.
metadata:
  author: jaknyfe.zo.computer
compatibility: Created for Zo Computer
allowed-tools: use_app_notion, use_app_x, x_search, web_search, read_webpage, generate_image, create_stripe_product
---

# Gumroad Product Builder

A 6-phase gate-driven system for building Gumroad products that people actually pay for.

**Source:** Adapted from Benneth Ogbuagu's "The Solopreneur's Gumroad Blueprint" — [article](https://medium.com/profitable-minds/i-built-an-ai-system-that-creates-gumroad-products-from-scratch-1896f8c43615) | [product](https://writerbenneth.gumroad.com/l/solopreneur-gumroad-blueprint)

---

## Connected Platforms

| Platform | Integration | When Used |
|---|---|---|
| **Notion** | `use_app_notion` | Track products, launches, sprint progress, pain-point databases |
| **X/Twitter** | `use_app_x` | Post launch threads, engage communities, DM buyers |
| **Stripe/Gumroad** | `create_stripe_product` | Create payment links for products (Gumroad-style flows) |
| **Zo AI** | `generate_image` | Generate cover images from Phase 3 prompts |
| **Web search** | `x_search`, `web_search` | Phase 1 pain-point research across Reddit, Twitter, Quora |

---

## The 6 Phases

### Phase 0 — Onboarding & Targeting
Captures two tracked variables before anything else runs:
- **Who** you're building for (audience)
- **What** revenue outcome you're targeting

Every subsequent phase references these explicitly: pain-point prioritization, pricing psychology, product format.

### Phase 1 — Deep Pain-Point Research
Crawls Reddit, Twitter/X, Quora, and Gumroad bestsellers for commercial intent signals.

**Linguistic triggers to surface:**
- *"I wish someone would just…"*
- *"Is there a tool for…"*
- *"I hate doing this…"*

**Commercial intent scoring (1–5):**
| Score | Signal | Action |
|-------|---------|--------|
| 1 | "This would be nice" | Discard |
| 2 | "I should look into this sometime" | Discard |
| 3 | "I need a solution" | Low priority |
| 4 | "I need this NOW" | Proceed |
| 5 | "I'll pay whatever it takes" | Strong proceed |

**GATE 1:** Only pain points scoring 4+ clear the gate.

**Platform integrations:**
- Use `x_search` to search Twitter/X for frustration tweets from target audience
- Use `web_search` for Reddit/Quora research
- Store results in Notion database

### Phase 2 — Product Options
Generates 3 distinct concepts across different formats:
1. **Template/Checklist** — low build effort, $9–27
2. **Mini-course/Guide** — medium build, $27–97
3. **Tool/System** — high build, $97–197

Each concept explains fit against Phase 0 variables, build time, and revenue potential.

**GATE 2:** Human selects one concept to proceed with.

### Phase 3 — Full Product Architecture
Produces everything needed to list before a single file is created:
- Benefit-driven product name
- 3-point sales copy arc: hook → transformation → CTA
- 3 pricing tiers with clear differentiation
- Cover image prompts (2–3 AI image prompts) → use `generate_image`
- Gumroad upload checklist
- Bonus product specs per tier

**GATE 3:** Human approves architecture before Phase 4.

### Phase 4 — Full Product Creation
Builds the complete artifact — no placeholders, no "add more as needed."
- Every section, field, view, and property populated
- Sample data included (not empty fields)
- Usage guide / README embedded
- Delivery format: Google Sheets link or downloadable export

### Phase 5 — Execution Roadmap
14-day launch sprint on zero-cost stack.

**Stack:** Gumroad (hosting) + Twitter/Reddit/LinkedIn (traffic) + Canva (assets) + Notion/Google Sheets (build)

**Sprint:**
| Days | Action | Platform |
|------|--------|----------|
| 1–2 | Finalize + upload to Gumroad | Gumroad |
| 3–4 | Write 3-part Twitter/X thread | X/Twitter |
| 5–6 | Post to 2 relevant subreddits | Reddit |
| 7–8 | Email list with preview + early-bird link | Gmail |
| 9–10 | LinkedIn post (if B2B audience) | LinkedIn |
| 11–12 | Engage in 2 relevant communities | Reddit/Discord |
| 13–14 | Monitor dashboard, DM 5 engaged users | X/Twitter, Gumroad |

---

## Platform Actions Reference

### X/Twitter (`use_app_x`)
```javascript
// Post launch thread
use_app_x("x-post-tweet", {
  text: "Hook tweet that stops the scroll...",
  reply_to_tweet_id: "<first-tweet-id>"  // chain subsequent tweets
});

// Send DM to engaged user
use_app_x("x-send-dm", {
  recipient: "@username",
  text: "Thanks for engaging! Here's the link → ..."
});
```

### Notion
```javascript
// Create product tracking page
use_app_notion("notion-create-page", {
  parent: "<notion-root-page-id>",
  title: "Gumroad Launch Sprint — [Product Name]",
  pageContent: "Phase 0: [audience]\nPhase 1: [pain point]\n..."
});

// Create product database
use_app_notion("notion-create-database", {
  parent: "<parent-page-id>",
  title: "Gumroad Products",
  properties: {
    "Name": { title: {} },
    "Audience": { rich_text: {} },
    "Pain Point": { rich_text: {} },
    "Concept": { select: { options: ["Template", "Mini-Course", "Tool"] } },
    "Status": { select: { options: ["Research", "Building", "Launching", "Live"] } },
    "Revenue": { number: { format: "dollar" } },
    "Launch Date": { date: {} }
  }
});
```

### Generate Cover Images
```javascript
// Use cover prompts from Phase 3
generate_image({
  prompt: "Clean flat-lay of a desk with worksheet, laptop, and coffee, minimal aesthetic, soft natural light, professional product photography style",
  file_stem: "gumroad-cover-[product-name]"
});
```

---

## Critical Validation Question

Before launching, answer this:

> **What is the exact phrase your buyer types at 11pm when they're frustrated enough to pay for a solution?**

Your sales copy must echo their exact language — not your description of their problem.

---

## Usage

```bash
# Full interactive wizard
node Skills/gumroad-product-builder/scripts/gumroad-product-builder.js

# Jump to specific phase
node gumroad-product-builder.js --phase 1

# Show current state
node gumroad-product-builder.js --status

# Reset state
node gumroad-product-builder.js --reset
```

---

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | This file — full reference |
| `scripts/gumroad-product-builder.js` | Interactive CLI wizard with all 6 phases |
| `references/solopreneur-gumroad-blueprint-article.md` | Archived source article |