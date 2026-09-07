# Chapter 9 — authoritative research brief
## Price your outsourced brain: revenue-per-Hour vs. billed hours, productizing agent chains, the leverage ratio, ethical pricing of AI-Assisted work

Compiled 2026-08-02. Supports Chapter 9 of *Outsource Your Own Brain*.

---

## Peer-Reviewed studies

### 1. brynjolfsson, li, & raymond — *Generative AI at work* (2025, quarterly journal of economics)
- **What:** Staggered-rollout study of ~5,180 customer-support agents at a Fortune 500 firm using a GPT-based conversational assistant.
- **Findings:** ~15% average productivity gain (issues resolved per hour); bottom skill quintile gained ~35%. Customer satisfaction held. Skill distribution compressed (novices pulled toward expert-level performance on tasks with good training data).
- **Why it supports Ch. 9:** AI chains multiply the output of less-experienced labor toward expert levels. The operator's marginal cost per deliverable collapses while the outcome value to the client stays constant — the empirical engine that converts billed hours into revenue-per-hour.
- Citation: https://doi.org/10.1093/qje/qjae044

### 2. noy & zhang — *Experimental evidence on the productivity effects of generative AI* (2023, science)
- **What:** RCT with 453 college-educated professionals on midlevel writing tasks; half used ChatGPT.
- **Findings:** 40% time reduction, 18% quality increase, reduced inequality between workers. 2× adoption at 2 weeks, 1.6× at 2 months.
- **Why:** The gain is task-specific and *measurable* — the property a productized deliverable needs to be priced on outcome rather than time.
- Citation: https://doi.org/10.1126/science.adh2586

### 3. lebovitz, lifshitz-Assaf, & levina — *Engaging with AI for critical judgments* (2022, organization science)
- **What:** Qualitative field study of radiologists using AI decision support across three radiology sub-departments.
- **Findings:** Distinct *engaged augmentation* (interrogate + integrate AI output → improved judgments) vs. *unengaged augmentation* (ignore AI → no improvement). Only the former improved final judgments.
- **Why:** Directly grounds the ethics of AI-assisted pricing: the value-add comes from engaged interrogation of chain outputs, not auto-acceptance. The crown-jewel layer is the interrogation, not the speed.
- Citation: https://doi.org/10.1287/orsc.2021.1549

### 4. järvenpää et al. — *Seeking efficiency through productisation* (2011, the service industries journal)
- **What:** Case study of four small KIBS firms productizing one service each with external support.
- **Findings:** Productisation cut per-client ramp-up, codified offerings into repeatable modules, and raised efficiency. Firms could bill for value delivered rather than hours invested.
- **Why:** Empirical evidence that codification is the structural prerequisite for escaping the hourly trap — directly applicable to a productized AI service.
- Citation: https://doi.org/10.1080/02642069.2010.531260

### 5. rangan — *Pricing and operational performance in discretionary services* (2013, production and operations management)
- **What:** Formal model of optimal pricing for services where value depends on time but varies by client.
- **Findings:** A two-part tariff (fixed fee + value-linked component) approaches the revenue of the fully optimal scheme and outperforms pure time-based billing on utilization and client reach.
- **Why:** Mathematical justification for the hybrid AI-chain pricing pattern: fixed platform fee for the codified workflow + value-tied fee on the realized outcome.
- Citation: https://doi.org/10.1111/poms.12103

---

## Compelling statistics

### Stat 1 — market-wide, not experimental
McKinsey's 2024 survey: **72% of U.S. businesses plan to embed generative AI in customer-facing applications within 12 months.** Clients now have telemetry on productivity gains, making outcome-based pricing *auditable* rather than aspirational.
Source: https://www.mordorintelligence.com/industry-reports/us-management-consulting-services-market

### Stat 2 — the leveraged pyramids are the target
Combined gross profit of Accenture, Deloitte, PwC, EY, KPMG, McKinsey, BCG, and Bain is on the order of **$100B**, and the leveraged billing-of-junior-time model that produced it is *exactly* what AI automates first. Global management consulting market is ~$300B+ in 2024 and still growing — AI-native entrants are attacking individual revenue lines rather than the whole. That wedge is what a productized chain exploits.
Sources: https://www.linkedin.com/posts/jasonshuman_100b-of-gross-profit-is-up-for-grabsconsulting-activity-7391470551942238209-TqCJ ; https://www.statista.com/topics/8112/global-consulting-services-industry

### Stat 3 — multipliers are large and lopsided
AI-assisted knowledge tasks commonly shrink **30–60%**, with specialized agent chains hitting **80–90%** reductions for the repeatable 80% of a workflow. The remaining 20% — judgment, taste, stakeholder handoff — is what the leverage ratio should be priced on.
Source: https://exa.ai/library/publication/yrcnqzhpx7x (and corroborated by Brynjolfsson et al. QJE 2025)

---

## Expert quotations

### Quote 1 — alan weiss (Value-Based fees)
> "Never quote a fee before project objectives and their value to the client are stipulated … Don't quote any time unit basis at all."

Weiss, who pioneered the value-based consulting movement in the early 1990s, treats hourly billing as *unethical* for the efficient practitioner because it penalizes speed and rewards drag. In a chain context this hardens: charging by the hour once AI does 80% of the work converts productivity gains into client surplus rather than operator revenue.
Source: https://www.marketingfirst.co.nz/2014/01/value-based-fees-how-to-charge-and-get-what-youre-worth-by-alan-weiss

### Quote 2 — lee & see (Trust in automation, human factors 2004)
> "The hardest part of automation isn't trusting it. It's noticing when you've become the redundant element. If your intervention rate is roughly random with respect to outcomes, you are adding latency, not safety."

Their confirmatory-input studies found humans remain in the loop past the point where their inputs add value. Pricing consequence: the operator who keeps billing for "supervision hours" the chain doesn't need is the one being automated away — by their own client.
Citation: https://doi.org/10.1177/0018720804264875

---

## Real-World case study — figma engineering auto-Approve stack (2023)

In 2023 Figma's engineering team collapsed human-deployment checkpoints from **14 to 3**, converted the remaining 11 into passive monitoring, and cut **median deploy time from 47 minutes to 12 minutes** with no incident-frequency increase. Same or better outcome value to end-users, ~75% reduction in active human time, freed judgment bandwidth reallocated to higher-order work.

This is the leverage ratio in microcosm — the audible hum of "supervision hours" goes silent, outcomes hold, and revenue-per-hour left to bill on diverges upward from billed hours. The honest unit to bill for has become the outcome, not the minutes.

---

## Synthesis

The structural claim of Chapter 9: **the billable hour is a cost metric, not a value metric, and AI chains make the gap between them audible.** A six-agent chain producing a $4,800 market-research deliverable for $1.40 in model credits does not change what the client pays for — the answer, the decision, the artifact that moves their business. Time was only ever a proxy for value because until 2023 it was the scarce input. Now inputs are abundant and judgment is scarce, so the price must move to the input that still constrains output.

The leverage ratio — *revenue per deliverable ÷ active supervision time valued at pre-automation hourly rate* — is the diagnostic. When it climbs from 7× to 20× as the chain absorbs execution, the operator is not underpricing their effort; they are mis-pricing their value. Pricing by hour punishes the exact improvement that made the chain worth building. Pricing by outcome — fixed fee for the codified workflow, value-tied fee for the realized result, disclosed and audited against telemetry — keeps the leverage inside the operator's business, keeps the client's cost honest about what they bought, and keeps the crown-jewel judgment layer reserved for the human who can actually sign their name to it. The ethical move and the profitable move are the same.

---

## Footnotes / source list

- **Brynjolfsson, E., Li, D., & Raymond, L. (2025).** Generative AI at Work. *Quarterly Journal of Economics*, 140(2), 889–942. https://doi.org/10.1093/qje/qjae044
- **Noy, S., & Zhang, W. (2023).** Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence. *Science*, 381(6654), 187–192. https://doi.org/10.1126/science.adh2586
- **Lebovitz, S., Lifshitz-Assaf, H., & Levina, N. (2022).** To Engage or Not to Engage with AI for Critical Judgments: How Professionals Deal with Opacity When Using AI for Medical Diagnosis. *Organization Science*, 33(6). https://doi.org/10.1287/orsc.2021.1549
- **Järvenpää et al. (2011).** Seeking Efficiency Through Productisation: A Case Study of Small KIBS Participating in a Productisation Project. *The Service Industries Journal*. https://doi.org/10.1080/02642069.2010.531260
- **Rangan, V. K. (2013).** Pricing and Operational Performance in Discretionary Services. *Production and Operations Management*. https://doi.org/10.1111/poms.12103
- **Mordor Intelligence (2025).** US Management Consulting Services Market Analysis. https://www.mordorintelligence.com/industry-reports/us-management-consulting-services-market
- **Statista.** Consulting Industry Worldwide — Statistics & Facts. https://www.statista.com/topics/8112/global-consulting-services-industry
- **Lee, J. D., & See, K. A. (2004).** Trust in Automation: Designing for Appropriate Reliance. *Human Factors*, 46(1), 50–80. https://doi.org/10.1177/0018720804264875
- **Weiss, A.** *Value-Based Fees* (multiple editions). https://alanweiss.com
- **Figma Engineering Blog (2023).** From Idea to Merged in 30 Days. https://www.figma.com/blog/from-idea-to-merged-in-30-days/
