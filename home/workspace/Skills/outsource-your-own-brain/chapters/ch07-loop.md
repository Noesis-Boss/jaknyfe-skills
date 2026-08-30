# The Loop — Measure, Refine, Let Go (Ch. 7)

## The five metrics that matter

1. **Tokens-per-output-dollar** — cost efficiency of each chain.
2. **First-pass acceptance rate (FPAR)** — % of drafts that ship with zero edits. The only metric that chases quality and efficiency simultaneously.
3. **Hours reclaimed per week.**
4. **Failure mode frequency** — what breaks, how often.
5. **The let-go ledger** — the record of what you've stopped watching and what happened after.

## FPAR — the delegation dashboard

- Low FPAR = prompt under-specified, context thin, or asking the model something it can't do at your price tier → you're babysitting, not delegating.
- High FPAR = nailed it **or** your bar slipped (rubber-stamping).
- **Target: 70% first-pass on routine work within 60 days** of standing up a chain. Below → babysitting. Above 95% → raise your bar.
- Track weekly.

**Vague prompts fail because they leave the output space open.** "Write a summary" has fifty valid shapes. "120 words: lead sentence → three bullet takeaways → one implication line" collapses the space. Describe the **artifact**, not the task.

**Composition beats mega-prompts** (worked example): a 600-token prompt doing research+structure+voice+length scored 31% FPAR. Split into three prompts (research → JSON blob; draft → email; polish → word count + voice) → 78% FPAR in two weeks. Same model, same cost.

## The 30-run rule (and the loop itself)

1. Stand up the chain.
2. **Run it thirty times without changing anything.**
3. Measure.
4. Refine the prompt **or** cut a link — never both in the same week.
5. Climb the letting-go curve one stage.
6. Repeat.

## The letting-go curve (4 stages)

| Stage | Name | Behavior |
|---|---|---|
| 1 | **Vigilant co-pilot** | Babysit every run, read every output. Necessary at first — stay too long and you've built a slow version of yourself. |
| 2 | **Spot checker** | Sample: every third email, every fifth draft. If samples hold, trust the unsampled. |
| 3 | **Exception reviewer** | You only see what the agent flags — failed lookups, ambiguous queries, below-confidence items. The system must raise its hand. **Where most chains should settle; can last years.** |
| 4 | **Absent by default** | You see nothing until a human downstream reports something off. |

The hard part isn't building for each stage — it's stepping back when the metrics say you can. Most stall at Stage 2 forever because spotting errors *feels* like control. It's a tax paid to avoid the discomfort of trust.

## The remove-yourself criterion (pruning)

If you've been the same link for a quarter and the chain runs fine when you skip it — remove yourself. Your presence is the chain's hidden single point of failure. The vanishing-VA test: if you disappeared for two weeks, which chains survive?

## The 80/20 of agent prompts

Most chain value comes from a few lines of the prompt: the deliverable spec and the source guidance. Don't polish the preamble; iterate the spec against measured FPAR.
