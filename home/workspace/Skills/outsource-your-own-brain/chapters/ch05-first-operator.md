# Your First AI Operator — Staff the Clone (Ch. 5)

## The org chart of one

Split all work into two columns:
- **Owner-only**: client delivery, client conversations, creative work where judgment IS the product.
- **Delegable**: research, drafting, inbox triage, competitor scans, market summaries, quote hunts, data-gathering — the business's work that's been silently billed to the owner at premium rates.

The recipient of the delegable column is a **structured prompt**: runs the same task at the same quality in minutes, costs cents, doesn't quit. **Research is the ideal first seat** — high-volume, low-judgment, easily verified. Audit AI output like a junior hire on day two: skim, spot-check, push back where thin. You stop doing the *gathering*; judgment stays on the decision the research enables.

## The job description as a structured prompt (4 blocks, in order)

1. **Role and audience** — one sentence naming the *decision* the briefing supports. "Research analyst for [practitioner type] producing briefings that support [specific business decision]." Naming the decision kills drift into generalities.
2. **The deliverable spec** — format, section headers, word limits, required tables/lists, and the success metric you'll personally apply. "Three-section briefing ≤600 words: market size/trend, top-5 competitors with positioning, two openings for my niche."
3. **Source guidance** — what counts as evidence. "Prioritize trade-association reports, government stats, company press releases. Avoid SEO blog posts unless citing a primary source. Flag statistics older than three years as stale."
4. **Skill codes and constraints** — your standards written down: crisp attribution, exact figures, rank competitors by relevance not size, end with one actionable next-step suggestion. **Plus anti-hallucination constraint**: "Do not invent named clients or attributed quotes. If you cannot find a named source within two attempts, state 'no verifiable source found' and move on."

## Operationalizing: prompt → asset

- **Save as a file, not a note**: `operators/research_operator_v3.md`. The file is the personnel file. Bump the version on each real-work refinement, note what changed.
- **Lock the inputs**: one argument (topic), one optional context block. "Topic: [X]. Context: [Y] for [decision Z]." No free-typing assignments — a different prompt every run means a different briefing every run.
- **Schedule where the business feels it**: daily 7 AM news scan; client-prep on intake-booking day; competitor scan monthly. Without the schedule, it's a capability you forget.
- **Audit on a cadence, not a feeling**: 15 min/week on one random output. Did it save 20 minutes? Did I trust it? One edit per week compounds.
- Run on your stack (workspace agent + calendar/script trigger), not a chat window you must remember to open.

**Rhythm**: write once → refine twice on real output → from v3 forward your job is scaling its calls, not rewriting it.

## Promotion and cloning

Promotion = editing the job description (add a skill code or deliverable block for the recurring gap). Cloning = same 4-block skeleton, different deliverables/constraints: research → competitor scan → client-fit triage → content angles. Version the **template** too, so structural improvements propagate to all clones in one pass. When operator B takes operator A's output as input, your org chart is real.

