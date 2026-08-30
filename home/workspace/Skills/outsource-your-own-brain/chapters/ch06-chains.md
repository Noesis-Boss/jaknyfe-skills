# Chains Beat Willpower — Design the Workflow (Ch. 6)

A chain is links where each link's **output is a promise** to the next link (structured claims → structured draft → polished artifact → shipped). Not one blob prompt.

**Where the human goes — judgment steps only, clustered in four spots:**
1. **Curation** — which of ten sources is worth including; which of three angles is strongest.
2. **Commitment** — the claim that goes on record, the number in the proposal, the tone in the inbox.
3. **Escalation** — noticing output weird enough to fire a sub-chain instead of pressing go.
4. **Steering** — changing the system on a quarterly pattern: bump a prompt, retire a source, tighten a review window.

**Two rules for human placement:**
- Humans decide on **intermediates, never raw input** — let the chain compress first; choosing, not preprocessing.
- If a human-in-the-loop step takes **>15 minutes**, the chain is under-spec'd upstream — add a filter, rubric, or judging pass.

## Minimum viable chain

Smallest set of links from raw input to shipped output with one human judgment baked in: **Research → Draft → Revise → Send**. Have the draft step mark open decisions inline as bracketed questions (`[ANGLE: real client example or generic?]`) — those brackets are what the judgment step consumes.

## Confidence sub-chain (graceful self-correction)

Alongside Draft, the model self-grades against a one-page rubric ("Is every claim sourced? Is the CTA explicit? Does the angle match the audience poll?"). Below threshold → don't ship to Revise; **rerun Draft with the low grade spelled out** ("Tone flagged off-brand; tighten client-example sections"). The chain corrects itself instead of asking a human to clean up.

**Pruning**: you may inherit long chains (Research → Validate → Draft → Confidence-Check → Revise → Schedule → Send → Log). Most links don't earn their place. A link stays only if removing it measurably degrades the promised output.
