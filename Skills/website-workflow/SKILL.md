---
name: website-workflow
description: Plan or build a business, sales, personal-brand, portfolio, or local-business website using a focused strategy-first workflow. Use when the user asks for a website plan, homepage, landing page, portfolio, personal-brand site, or local-business site.
metadata:
  author: jaknyfe.zo.computer
---

# Website Workflow

Choose one of the six modes from the request. Combine modes only when the user asks for both planning and implementation. A planning request produces a clear brief and page plan; a build request produces working code in the project's existing stack or the requested editable HTML, CSS, and JavaScript.

## Modes and intake

Gather only details that materially affect the result. Reuse details already supplied. Ask one concise question when a missing detail changes the site or its claims; otherwise label reasonable assumptions and continue.

1. **Website strategy:** business type, brand, audience, offer, objective, aesthetic. Deliver essential pages, homepage section order, audience journey, primary and secondary CTAs, useful features, trust evidence, and required content.
2. **Premium homepage:** brand, business type, audience, offer, customer problem, desired outcome, style, colors, primary CTA. Build navigation, hero, benefits, services, process, proof, FAQ, closing CTA, and footer.
3. **Conversion landing page:** product/service, audience, problem, desired outcome, price, benefits, bonuses, action. Build the argument from problem to offer, benefits/features, proof, pricing, guarantee (only if supplied), FAQ, and final CTA.
4. **Personal brand:** name, profession, expertise, audience, services, achievements, projects, style, CTA. Build hero, bio, expertise, services, portfolio, proof, achievements, featured content, contact, and social links.
5. **Portfolio:** profession/specialization, name, target clients, work categories, aesthetic, CTA. Build hero, gallery, project cards and case studies, services, process, proof, about, and contact form.
6. **Local business:** business name/type, city or service area, services, hours, phone, address, unique benefit, CTA. Build hero, services, real reviews, pricing when provided, location/map when available, hours, FAQ, contact, and a mobile call action. Include accurate location-specific page titles, descriptions, headings, and contact details.

## Strategy and copy rules

- Center the page on one audience, one primary outcome, and one primary CTA. Keep secondary actions visually subordinate.
- Make the value proposition specific to the supplied offer and audience. Use direct-response principles: concrete benefit, evidence, clear offer, and an obvious next step.
- Never invent testimonials, client names, ratings, case-study results, credentials, awards, prices, guarantees, availability, discounts, or deadlines. Omit missing proof or label sample content clearly as a replaceable placeholder. Use urgency only when a real constraint is provided.
- Treat user-provided claims as inputs, not verified facts. Flag material claims that need confirmation. For local SEO, use natural location wording and genuine service-area details; never keyword-stuff or fabricate a local presence.
- Keep forms and buttons honest: do not imply a form submits, a booking works, or a payment completes unless the project has a working destination or integration.

## Build workflow

1. Inspect the project README, AGENTS.md, and any applicable DESIGN.md before changing code. Apply design tokens literally. Preserve the existing framework and routing conventions.
2. For implementation, use `frontend-design` for the visual and interaction work. Use `design-md` when a persistent design system is needed, `zo-project-template` for a new standalone project, and `open-seo-local-seo` for evidence-based local visibility analysis when requested. Do not duplicate their procedures here.
3. If no stack is specified and the user wants a code artifact, produce plain editable HTML/CSS/JavaScript when that meets the request. For a real new project, follow the workspace Zo project convention and select Zo Space or Zo Site based on scope; do not replace an existing public route or homepage by default.
4. Build semantic, responsive, accessible markup. Support keyboard use, visible focus, readable contrast, reduced motion, useful image alternatives, and small-screen layouts. Set page title and description; use structured data only when facts are known and the site's format supports it.
5. Keep all content editable and make unfinished assets or integrations explicit. Avoid unnecessary dependencies, decorative filler, and unsupported claims.
6. When editing or deploying a user-facing site, validate with the project's available checks and inspect a rendered screenshot at desktop and mobile sizes before calling the work complete. For Vite sites, confirm `base` and asset paths before publishing. Publish only when explicitly requested; screenshot the live page after deployment.

## Deliver

For a plan, return the brief, page/section outline, journey, CTAs, trust/content needs, and assumptions or unresolved facts. For code, identify the files changed and summarize the working behavior, verification performed, and remaining placeholders. Keep the handoff concise and distinguish real functionality from visual mockups.
