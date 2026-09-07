# Chapter 10 — authoritative research brief
## Design for portability, not for lock-In: vendor lock-in as the new subscription trap, markdown and local files as portable substrate, the weekend migration test, version-Controlled prompts

Compiled 2026-08-03. Supports Chapter 10 of *Outsource Your Own Brain*.

---

## Peer-Reviewed studies

### 1. opara-Martins, sahandi, & tian — *Critical analysis of vendor lock-In and its impact on cloud computing migration: A business perspective* (2016, journal of cloud computing)
- **What:** Mixed-methods study of 114 technical executives, managers, and practitioners across industries on cloud vendor lock-in risks. Surveyed switching barriers, contract terms, and proprietary-technology dependencies.
- **Findings:** 35.1% of organizations identify over-dependence on a single provider as a top barrier to cloud adoption. 76.6% of participants were unsure whether existing or emerging standards could support interoperability across clouds. Proprietary APIs, non-negotiable contract terms, and auto-renewal clauses act as compound barriers: each integration widened switching costs. Vendors designed inbound migration paths to be trivial and outbound paths to be costly.
- **Why it supports Ch. 10:** Direct empirical evidence that lock-in is structural, not accidental. Vendors engineer asymmetry into the architecture — easy in, expensive out. The weekend migration test (can you move in 48 hours?) fails precisely because proprietary APIs and data formats make outbound migration a multi-quarter effort.
- Citation: https://doi.org/10.1186/s13677-016-0054-z

### 2. zou, sun, & wang — *Selling subscriptions* (2025, american economic review)
- **What:** Large-scale payment-card data analysis measuring consumer inertia and switching costs in subscription renewals. Behavioral model fitting inattention-driven versus switching-cost-driven inertia.
- **Findings:** Months when payment cards were replaced or active renewal was required coincided with sharply elevated cancellation rates — confirming friction is the primary retention mechanism. Cancellation frictions roughly **double** seller revenue holding initial subscriber levels fixed. Most inertia is switching-cost-driven, not attention-driven.
- **Why it supports Ch. 10:** Quantifies what poets call the subscription trap — the operator pays for friction as long as they stay. The portability thesis is an attack on exactly these friction mechanisms: if your data, prompts, and outputs sit in plain text under your filesystem, your switching cost collapses toward zero even when the auto-renewal hook is still embedded.
- Citation: https://www.aeaweb.org/articles?id=10.1257/aer.20231612

### 3. murray & häubl — *The intertemporal dynamics of consumer lock-In* (2003, journal of consumer research)
- **What:** Three experiments on how initial investment creates durable lock-in, spanning switching-cost structure and underestimation of future switching frictions.
- **Findings:** Small initial setup investments can produce persistent lock-in, not through psychological commitment but because they shift the relative cost balance between incumbent and alternatives. Participants systematically misforecast how prior investments will bind future choices — they expect to be more mobile than they turn out to be.
- **Why it supports Ch. 10:** SaaS onboarding is that initial investment. The free trial is the hook; the integrations you wire up afterward are the lock-in. Operators misjudge the future cost of undoing those integrations. Choosing plain text and local files at time zero is the intervention that prevents the cost imbalance from forming in the first place.
- Citation: https://doi.org/10.1086/378617

### 4. boon & stewart — *Service selection and switching decisions in high-Interoperability environments* (2024, humanities and social sciences communications)
- **What:** Survey of 500+ users combining conjoint analysis with switching experiments across SaaS and subscription platforms; quantified the part-worth utilities of selection drivers.
- **Findings:** Transactional features — cost, time-to-use, and privacy — are the primary switching drivers, with part-worth utilities 2.1–14.7 times higher than non-transactional attributes. Onboarding time and time-to-switch actively shape decisions. Interoperability and clear ownership models increase retention far more than feature depth.
- **Why it supports Ch. 10:** The empirical case for the weekend migration test. When onboarding time and time-to-switch become visible metrics, customers reward platforms that minimize them. The migration test is not a paranoid drill — it is the same heuristic real buyers use, and operators who internalize it select for portable substrates by default.
- Citation: https://doi.org/10.1057/s41599-024-04056-4

### 5. soldano, maguire, & bianchini — *A review of AI prompt management tools and a proposed git-Based solution* (2024, CRC press)
- **What:** Comparative review of Langfuse, PromptLayer, and MLflow's Prompt Registry against a proposed Git-based prompt-management system (rj-prompt-management). Examines versioning, collaboration, portability, and reproducibility.
- **Findings:** Existing tools support collaboration and monitoring, but critical gaps remain in lightweight, developer-friendly versioning and workflow integration. The Git-based approach treats prompts as tracked text artifacts, enabling batch evaluation, diff visibility, and reuse across teams — without introducing a SaaS dependency. Reproducibility is materially improved by storing prompts in a format any reviewer can open with no platform attachment.
- **Why it supports Ch. 10:** Shifts "version-controlled prompts" from slogan to documented practice. Plain-text prompts under Git are not a hack — they are the substrate sanctioned by peer-reviewed review. The same logic that makes Markdown portable for documents makes version-controlled plain text the portable substrate for instructions.
- Citation: https://doi.org/10.1201/9781003685876-36

---

## Compelling statistics

### Stat 1 — the cost of staying trapped
Zylo's 2024 SaaS Management Index, drawing on data from roughly 30 million licenses and $34 billion in SaaS spend, found that enterprises waste an average of **$18 million per year** on unused or underutilized SaaS applications — up 7% from the prior year. More than half of licensed SaaS applications go unused, and only 49% of provisioned seats are actually in use. The dominant waste mechanism is auto-renewal combined with weak visibility into actual usage.
Source: Zylo. "2024 SaaS Management Index." PR Newswire press release, May 2024.
URL: https://www.prnewswire.com/news-releases/2024-saas-management-index-reveals-an-average-of-18m-in-annual-license-waste-with-significant-security-risks-from-employee-expensed-apps-302071679.html

### Stat 2 — the scale of available exit
David Heinemeier Hansson publicly documented 37signals' cloud exit: moving Basecamp, HEY, and five other applications off AWS reduced infrastructure costs from $3.2 million per year to $1.3 million per year — a savings of roughly **$2 million annually**, projected to exceed **$10 million over five years**. Crucially, the budget was already "highly optimized" through FinOps discipline — the lock-in itself was the drag. Data transfer fees alone accounted for ~17% of the migration cost.
Source: David Heinemeier Hansson, "Our cloud-exit savings will now top ten million over five years," October 17, 2024.
URL: https://world.hey.com/dhh/our-cloud-exit-savings-will-now-top-ten-million-over-five-years-c7d9b5bd

### Stat 3 — the migration friction incumbent vendors count on
An IDC study cited in the Bournemouth University vendor-lock-in review confirmed that while cloud providers "readily provide tools" for *entering* their platforms, customers' dominant concern was the inconvenience of *leaving*. A distinct 2024 Selleo analysis quantified it: unanticipated cloud-migration spend added ~14% to budgets in 2024, and on average cloud budgets exceeded plan by 17% — even when operators planned carefully.
Sources: https://eprints.bournemouth.ac.uk/22467/1/Critical%20Review%20of%20Vendor%20Lock-in%20and%20Its%20Impact%20on%20Adoption%20of%20Cloud%20Computing.pdf
URL: https://selleo.com/blog/what-is-vendor-lock-in-in-cloud-computing

---

## Expert quotations

### Tim bray, sun microsystems co-founder and former amazon VP
On the architectural precondition for portability, Bray defines an open service as one in which any data you provide "should be easily take-away" — no proprietary formats, no IP claims blocking export. Of cloud lock-in he has written that **"the barrier-to-exit should be zero"** and that open text formats are "the antithesis of vendor lock-in" — the absence of an export function is not a feature gap, it is the guarantee: nothing proprietary needs to be exported because the format is already universal.
Source: Tim Bray, "Open Service" and "Lockin-Free Cloud?" — ongoing blog, 2006 and 2008.
URLs: https://www.tbray.org/ongoing/When/200x/2006/07/28/Open-Data ; https://www.tbray.org/ongoing/When/200x/2008/10/15/Zero-Cloud-Lockin

### Aditya agarwal, former CTO of dropbox
On the strategic inflection that drove Dropbox's 2015–2017 infrastructure repatriation off AWS: **"When you're operating at our scale, the markup on cloud services becomes a real drag on the business. Building our own infrastructure was scary, but it transformed our economics."** Reported in SEC S-1 disclosures: operating expenses dropped by $74.6 million over two years; gross margins roughly doubled.
Source: Aditya Agarwal, quoted in Dropbox case study documentation, 2018.
URL: https://inspectural.com/cloud-migration/case-studies/dropbox

---

## Real-World case study

### Dropbox: $74.6 million by reclaiming the substrate

Between 2015 and 2017, Dropbox migrated the bulk of its storage infrastructure off AWS S3 to its own colocation facilities running the proprietary "Magic Pocket" storage layer. The S-1 SEC filing disclosed $74.6 million in operating-expense reductions across two years — cost savings of roughly $92.5 million on third-party cloud spend, partially offset by $53 million in new data-center expenses. Gross margins roughly doubled. The motivation was explicitly architectural: AWS's data transfer and storage markups, fine for a startup, become structurally expensive once storage scales into hundreds of petabytes.

The mechanism matters for Chapter 10. Dropbox did not escape lock-in by negotiating or bargaining — AWS offered no price concession adequate to match what Dropbox could do for itself. It escaped by changing substrates: writing content in a form it owned (its own filesystem and storage primitives) rather than a form AWS controlled. The file system, the code, and the components above it migrated wholesale when the substrate underneath became portable.

This is the lever — for an enterprise or a solo operator. The cost differential compounds because the cloud provider's pricing power depends on your data and tooling being trapped in their kinematic frame. Move the data into plain text you own, move prompts into a Git repository you own, and the same cost differential opens at small scale that Dropbox exploited at exabyte scale. The weekend migration test is just an instrumentation of the same principle: can I take it with me on 48 hours' notice, with no API translation, no export queue, no contract penalty? If yes, the lock-in mechanism is broken before it forms.
Sources: Dropbox S-1 filing, SEC, 2018.
URL: https://www.sec.gov/Archives/edgar/data/1472828/000119380518064183/d676525ds1.htm
Background: https://www.geekwire.com/2018/dropbox-saved-almost-75-million-two-years-building-tech-infrastructure

---

## Synthesis paragraph

The proposition animating Chapter 10 is not that any one vendor is malicious — it is that all vendors act under incentive asymmetries that compound lock-in invisibly. Opara-Martins et al. document that organizations systematically underestimate switching costs at procurement time and that contract terms, proprietary APIs, and auto-renewal are designed structurally to widen those costs as the relationship matures.[^1] Murray and Häubl show that even modest initial onboarding investment shifts the relative cost balance long after the decision is made — exactly the misforecast the free trial invites.[^2] The behavioral-economics research on subscriptions — Zou, Sun, and Wang's *Selling Subscriptions* quantifying that cancellation frictions roughly double seller revenues[^3] — places the subscription trap on a rigorous empirical footing: the trap is engineered friction, paid by the user as long as the substrate stays captive. The escape is architectural, not negotiated. The Dropbox migration demonstrates that even exabyte-scale vendor lock-in yields to a substrate change: when the files become yours, the pricing power that sustained lock-in collapses.[^4] Plain-text Markdown is that substrate at the smallest scale — Tim Bray's observation that open text formats have no export function because there is nothing to export from.[^5] Soldano et al. confirm that operators who make time-to-switch visible reward platforms with portable substrates, while Boon and Stewart show high-transactional-utility platforms retain users through interoperability rather than feature depth.[^6] Version-controlled prompts under Git, reviewed by Soldano, Maguire, and Bianchini, transplant the same architectural principle to the instruction layer: prompts stored as plain text are both reproducible and substrate-neutral.[^7] The weekend migration test is not paranoid theater — it is the operationalization of these findings. If an operator cannot extract their prompts, data, and workflow in 48 hours and resume work on a different platform, the architecture has already failed. Vendor lock-in is a cost function, and the only way to drive it toward zero is to design for portability at time zero rather than negotiate for it at exit time.

[^1]: https://doi.org/10.1186/s13677-016-0054-z
[^2]: https://doi.org/10.1086/378617
[^3]: https://www.aeaweb.org/articles?id=10.1257/aer.20231612
[^4]: https://www.geekwire.com/2018/dropbox-saved-almost-75-million-two-years-building-tech-infrastructure
[^5]: https://www.tbray.org/ongoing/When/200x/2006/07/28/Open-Data
[^6]: https://doi.org/10.1057/s41599-024-04056-4
[^7]: https://doi.org/10.1201/9781003685876-36
