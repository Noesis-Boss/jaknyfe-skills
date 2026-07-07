# 2-Tier Weight-Loss Product — Validated Design

**Date:** 2026-07-07
**Status:** Design validated via brainstorming session (5 sections)
**Owner:** Don Lowery (jaknyfe)

---

## 1. Methodology (source: brother's 100 lbs / 9 mo result — 50 lbs / 3 mo)

The system is **exercise (walking) + protein targeting + calorie deficit**. No supplements, no pills, no extremes — which makes it ad-safe and sustainable.

- **Phase 1 (months 1–3) — "Kickstart":**
  - Walking **≥ 6,000 steps/day**
  - Calorie deficit **≥ 500 cal/day** measured against ~2,000 base + exercise burn
  - Protein **≥ 0.75 g × TARGET body weight** (e.g. 175 lb target → 150 g protein/day)
  - Goal: rapid initial loss, lock habits, protect muscle mass

- **Phase 2 (months 4–9) — "Transformation":**
  - Same protein + deficit discipline
  - **Gym replaces most walking** to drive muscle gain + protect metabolism
  - Goal: sustain loss, avoid rebound, body recomposition

**Core principle:** the method is *math you can automate* — steps, protein target, deficit status. That is the product moat.

---

## 2. Tier Split

| | **Tier 1: "The Kickstart"** | **Tier 2: "The Transformation"** |
|---|---|---|
| Maps to | Phase 1 (mo 1–3) | Phase 2 (mo 4–9) |
| Promise | "Lose your first 50 with walking + protein — no gym required" | "Turn the loss into a body that stays — gym + mindset, no rebound" |
| Barrier | Near-zero (walk + food) | Gym access / home weights |
| Format | 12-wk self-paced course + tracker | 24-wk course + coaching/community |
| Price | ~$67 one-time (tripwire) | ~$39/mo continuity |

---

## 3. Delivery Format & Platform

**Chosen: Course + lightweight web tracker (free standalone front door).**
Course format (**B**): in-app lessons on the Zo Site **+ downloadable PDF guides** per tier (selected).

The free **tracker** (Zo Site) is the front door. Because it must **hold each user's data over time**, it requires an **email-based account** — **passwordless magic-link OR Google OAuth** (both yield a verified email; low friction, no password to forget). Account creation captures the email natively (= lead for nurture/retargeting). Always-visible "Unlock the 12-week plan" upsell retained. The signup is a *value exchange* (your data persists across sessions), not a separate lead-magnet gate.

**Auth & storage:** Email-based — **passwordless magic-link OR Google OAuth** — both produce a verified email tied to the account. Magic-link emails sent via Resend (already connected). Google OAuth requires a Google Cloud OAuth client (client ID/secret stored as secrets) + a registered redirect URI. Per-user data (weight, steps, calories eaten, exercise burn, protein) persisted in SQLite (Zo Site backend / managed user service). No passwords stored. Privacy policy + explicit consent at signup — email is PII (FTC/GDPR-aligned).

Built on existing Vite/React stack; source owned by user. Stripe Connect (already connected) for checkout.

---

## 4. Content Outline & Build Sequence

**Tier 1 "Kickstart" (12 wks):**
- Wk 1–2: Baseline, walking protocol (6k steps), protein-target math, 500 deficit
- Wk 3–6: Habit locking, protein-first meals, light food awareness
- Wk 7–10: Plateaus, step progression, deficit tightening
- Wk 11–12: Phase-transition prep (gym intro, mindset for Phase 2)

**Tier 2 "Transformation" (24 wks):**
- Gym progression replacing walking; muscle-gain focus / recomp
- Plateaus, social eating, travel, sleep
- Rebound-proofing + maintenance exit

**Build order:**
1. Free tracker Zo Site (front door / MVP) — email magic-link + Google OAuth + persistent per-user storage
2. Tier 1 course (12 modules)
3. Tier 2 course + coaching/community layer (after Tier 1 converts)

---

## 5. Compliance & Claims (weight loss = restricted ad category)

- **No before/after images.** Use progress *data* (the curve), not bodies.
- **No "are you overweight?" / idealized-body** framing (Meta bans).
- **No "extreme weight loss" claims** (TikTok bans). "100 lbs in 9 months" = a *specific individual result*, shown as a **case study with "results not typical / individual results vary" disclaimer**, never a promise.
- **FTC testimonial rule:** brother's story must be honest + disclose typical results; can't imply everyone gets 100 lbs.
- **No disease/cure language** — behavioral, not medical.
- **In-product disclaimer** on every tier page + tracker: "Consult your physician; individual results vary."
- **Email capture = PII.** Account signup requires a privacy policy + explicit consent; lead data used only per the stated purpose. Complies with platform lead-form rules (Meta/LinkedIn require consented Custom Audiences + linked privacy policy).

**Brother's story = hero case study with full disclaimer** (trust anchor), not the headline claim. Marketing leads with the *method*, not a scale number. The tracker shows *your* inputs vs *targets* — never promises an outcome.

---

## 6. GTM & Pricing

**Funnel:** Free tracker → Tier 1 ($67 one-time) → Tier 2 ($39/mo continuity).

**Where it lives:** Tracker + course on a Zo Site (own source, publishable). Stripe payment links for checkout. Marketing/case-study on the site or a zo.space route.

**Channels:** Lead **organic** — tracker is shareable ("here's my protein/deficit number"); walk+protein angle is non-extreme so it survives ad review. Paid (Meta/TikTok) only after funnel converts, with Section 5 disclaimers baked in. X accounts for founder-led proof.

---

## 7. Next

Ready to set up for implementation: scaffold the free tracker Zo Site first, then Tier 1 course content.
