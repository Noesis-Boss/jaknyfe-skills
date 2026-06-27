# ClientOps — Build Plan
*Combined: Review collection (#1) + Client portal / scope-creep shield (#2) + Karen defense (#3) + review-velocity (#4) for micro-SMBs*
*Date: 2026-06-20*

---

## 1. The product (one sentence)
**"ClientOps" — the client-facing dashboard for service SMBs: collect reviews, lock in scope, get paid on time, defend your reputation.**
Position: NOT a CRM, NOT a project manager. The single pane the SMB owner opens every morning to manage clients + reputation.

---

## 2. Target customer (the wedge)
**Bakery-tier local service businesses + solo freelancers + small agencies.**
- 1-10 employees, 50-500 clients/year
- Owns their own Google Business listing
- Sends invoices manually or via Wave/QuickBooks alone
- Cannot afford Birdeye ($299+), Podium ($399+), HoneyBook ($100+)
- TAM: ~33M US local service SMBs + ~73M US freelancers

---

## 3. Core feature set (V1 — must ship, 2-3 weeks)

| # | Feature | Pain addressed |
|---|---------|-----------------|
| **F1** | **Review-request funnel** (QR + SMS + email templates, post-job auto-trigger) | #1 core |
| **F2** | **Reputation dashboard** (Google/Yelp/Facebook rating + velocity + alert on bad review) | #1 core, #3 |
| **F3** | **One-tap negative-review response + dispute file generator** | #3 |
| **F4** | **Client portal** (login link, see project status, files, invoices — branded) | #2 |
| **F5** | **SOW / scope-lock** (template + e-signature; work cannot proceed without signed addendum) | #2 (scope creep) |
| **F6** | **Stripe-backed invoicing + escrow** (auto-bill on milestone; client funds held) | #2 (dispute) |
| **F7** | **"Karen mode"** (flag coordinated review attack; auto-file across Google/Yelp/BBB; evidence pack PDF) | #3 |
| **F8** | **Public testimonial widget** (drop-in HTML for SMB site/social — drives review velocity) | #4 |

---

## 4. Explicit non-features (V1)
- NO calendar/scheduling
- NO team chat
- NO project management / kanban
- NO AI features (chatbot, summarization) — stay boring, ship fast
- NO mobile app (responsive web only)
- NO multi-location support

**Reasoning:** SMB owners don't want another Notion. They want fewer tabs, not more.

---

## 5. Architecture

**Frontend:** Single React (Vite + Tailwind + shadcn) PWA. Hosted on a **Zo Site** (publish to public zocomputer.io URL).
**Backend:** Zo Site API routes (Hono on Bun) — fast enough for V1.
**DB:** PostgreSQL via the Paperclip-restore Postgres on port 5433 (already running, 7 active companies). Schema below.
**Auth:** Two roles: `owner` (SMB) + `client` (the SMB's customer, magic-link login).
**Integrations:** Google Business Profile API (reviews), Stripe (payments), Twilio (SMS).
**Hosting:** Zo Site (auto-managed) — Don's stack is already proven.

---

## 6. Data model (sketch)
```
businesses (id, name, owner_email, google_place_id, stripe_account_id, plan, created_at)
clients (id, business_id, name, email, phone, portal_token)
projects (id, business_id, client_id, title, scope_doc_id, status, locked)
sow_documents (id, project_id, body_md, signed_at, signature_url, addendum_of)
invoices (id, project_id, stripe_invoice_id, amount_cents, status, escrow_tx_id)
reviews (id, business_id, source, external_id, author, rating, body, posted_at)
review_requests (id, business_id, client_id, channel, sent_at, clicked, posted)
review_alerts (id, business_id, review_id, severity, dismissed)
karen_cases (id, business_id, triggered_at, evidence_pack_url, status)
```

---

## 7. Success criteria (Don's "definition of done")
1. End-to-end V1 demo: SMB signs up → creates client → sends review request → client posts Google review → SMB sees it in dashboard → creates SOW → client signs → invoice paid via Stripe escrow
2. Live at `clientops-XXX.zocomputer.io`, public, screenshot-verified
3. Stripe webhook working (test mode OK)
4. Google Business Profile OAuth flow working against a real test business
5. AGENTS.md + DESIGN.md created at `Projects/clientops/`

---

## 8. Build phases (3 weeks)

**Week 1 — Foundation**
- Day 1-2: Scaffold Zo Site, schema, auth (owner + magic-link client), business + client CRUD
- Day 3-4: F4 client portal (read-only project view) + F5 SOW editor + e-sig
- Day 5: F6 Stripe invoicing (test mode)

**Week 2 — Reviews**
- Day 6-7: F1 review-request funnel (QR generator, SMS via Twilio)
- Day 8-9: F2 reputation dashboard + F3 negative-review response templates
- Day 10: F8 testimonial widget (public HTML)

**Week 3 — Defense + Polish**
- Day 11-12: F7 Karen mode (attack detection logic + evidence-pack generator)
- Day 13-14: Billing, plan enforcement, free vs $39/mo tier
- Day 15: Screenshot, deploy public, write DESIGN.md + AGENTS.md

---

## 9. Pricing (V1)
- **Free** — 1 location, 25 reviews/mo, basic dashboard
- **$39/mo** — Unlimited reviews, SOW + invoices, Karen mode
- **$79/mo** — + Stripe escrow, multi-location (V2)
*(Sits exactly in the Birdeye/NiceJob gap — $75-$299)*

---

## 10. Distribution (built-in, post-launch)
- POS integration (Toast/Square) — review-request fires on payment completion
- Accountant referral kit (one-page PDF + 20% revenue share)
- Marketing-agency white-label (V2)

---

## Open decision (need Don's call)

**Scope of V1.** The plan above ships 8 features in 3 weeks. Three viable cuts:

A) **Full plan as-is (8 features, 3 weeks).** More risk, but the "everything the SMB needs" pitch is what wins at this price tier. Bundled pain is the moat.

B) **Phase 1 = Reviews only (F1, F2, F3, F8 — 4 features, 1.5 weeks).** Ship the most validated pain (10K-vote thread). Add client-portal + Karen mode in V2. Faster first dollar, but loses the "single pane" wedge.

C) **Phase 1 = Client portal only (F4, F5, F6 — 3 features, 1.5 weeks).** Faster to ship, cleaner scope, freelancer-first. Reviews + Karen in V2. Higher LTV per user, but TAM is narrower.