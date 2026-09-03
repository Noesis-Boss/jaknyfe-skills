---
name: marketing-prompt-pack
description: Patched library of 81 Claude marketing prompts across 9 categories (lead magnets, Facebook, email, repurposing, case studies, brand, product promotion, sales copy, ad copy) with a grounding layer that blocks invented facts, fake testimonials, invented stats, and undisclosed native ads. Use when writing marketing copy from the prompt library, or when adapting any template prompt for real publication.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  source: claude_marketing_prompts_03–11 image set (evaluated 2026-09-03)
  version: "1.0"
---

# Marketing Prompt Pack (81 prompts, patched)

Verbatim prompt library from the Claude marketing images, wrapped in a grounding layer.

**Original weakness (2026-09-03 eval): skeleton 7.9/10, grounding layer weak.** The prompts define great structures but silently let the model invent testimonials, stats, metrics, competitor facts, and disguised ads. This pack fixes that without rewriting the skeletons.

## How to use

1. **Prepend this block to every prompt:**

```text
GROUNDING RULES (non-negotiable):
- Use only facts, numbers, testimonials, and claims I provide in CONTEXT below.
- Mark anything invented as [VERIFY] and anything missing as [NEED INPUT].
- Never fabricate testimonials, customer names, metrics, or results.

CONTEXT:
[Product/offer]: ...
[Audience]: ...
[Brand voice]: ...
[Real proof available — testimonials, stats, prices]: ...
[Hard facts — deadlines, caps, guarantees that are TRUE]: ...
```

2. Fill the CONTEXT block before running. Empty proof fields → outputs will contain `[NEED INPUT]` where proof belongs. That is correct behavior — do not remove them.
3. Apply the per-prompt ✏️ patches noted inline in each category file.
4. Run order for a new offer: `06-brand-strategy` → `01-lead-magnets` → `03-email-sequences` → `08-sales-offer-copy` → `02-facebook-content` / `09-ad-copy`. Use `04-content-repurposing` to multiply everything you publish.

## Category files

| File | Category | Prompts |
|---|---|---|
| `prompts/01-lead-magnets.md` | Lead Magnet Creation | 9 |
| `prompts/02-facebook-content.md` | Facebook Content | 9 |
| `prompts/03-email-sequences.md` | Email Sequences | 9 |
| `prompts/04-content-repurposing.md` | Content Repurposing | 9 |
| `prompts/05-case-studies-testimonials.md` | Case Studies & Testimonials | 9 |
| `prompts/06-brand-strategy.md` | Brand Strategy | 9 |
| `prompts/07-digital-product-promotion.md` | Digital Product Promotion | 9 |
| `prompts/08-sales-offer-copy.md` | Sales & Offer Copy | 9 |
| `prompts/09-ad-copy.md` | Ad Copy | 9 |

## The four hard rules

1. **No invented proof.** Testimonials, case metrics, and customer names come from paste or they become `[NEED INPUT]`. (Hits: 02-2, 03-1/9, 05-*, 07-2, 08-1/2, 09-4/8/9)
2. **No invented numbers.** Stats, "combined values," benchmark figures come from CONTEXT or get `[VERIFY]`. (Hits: 01-9, 02-6, 05-3/6, 07-5, 08-3)
3. **No fake scarcity/urgency.** Deadlines, caps, and bonuses must be true. (Hits: 03-6, 07-9, 08-1/7, 09-1)
4. **No undisclosed native ads.** Prompt 02-9 ("ad disguised as organic") and 09-2 ("blends into editorial") require FTC/platform sponsorship disclosure — tone-matching yes, concealment no.

## Known limits

- Prompts remain templates: they still need real audience/offer research behind the CONTEXT block. The pack fixes fabrication, not demand validation.
- Prompt 05-5 (hypothetical case studies) stays flagged as internal-brainstorming-only even after patching.
