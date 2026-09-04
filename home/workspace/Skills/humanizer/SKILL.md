---
name: humanizer
description: |
  Detect and fix AI writing patterns. Use when writing outbound content like emails, proposals, blog posts, client deliverables, or any external-facing writing. Also use when asked to humanize, polish, or de-AI text.
compatibility: Created for Zo Computer
metadata:
  author: skeletorjs & jaknyfe
  category: Community
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---
# Humanizer

Strip AI writing patterns. Make prose sound like a person wrote it.

## When to Use

- Client deliverables (proposals, reports, analysis)
- Outbound emails, especially cold outreach and client updates
- Blog posts, social copy, marketing material
- Creative writing drafts
- Anything that leaves the workspace

Not needed for: internal notes, task descriptions, meeting records, code comments, chat responses.

## Voice Calibration

When humanizing text, apply the user's voice rules. If the user has a persona configured with specific voice preferences, those override the defaults below.

**Default voice rules (customize to your persona):**
- Brevity over ceremony. One sentence is fine.
- Don't soften bad news.
- Own mistakes quickly. No deflection.
- Prefer active voice and short sentences.
- Vary sentence length. Real writing isn't uniform.

**Writing sample mode (borrowed from upstream v2.11.2):** If the user provides a writing sample (their own previous writing), analyze it before rewriting: note its sentence length, word choice, paragraph openings, punctuation, repeated phrases, and transitions, then match those habits. The sample takes priority over the default rules — if the sample uses em dashes, keep them at about the same rate and do not apply #11 as a ban. Do not replace casual words with formal ones or remove deliberate quirks.

**To customize**: Edit the "Voice Calibration" section above to match your persona's voice rules. For example, if your persona avoids em dashes and emojis, add those as hard rules. If your persona uses humor, specify the style.

## Process

1. Scan for patterns listed below
2. Fix each instance
3. Read the result aloud in your head. Does it sound like a person talking?
4. Check against voice rules
5. Verify: varied sentence length, actual opinions present, no robotic uniformity
6. Cluster check: a single sign (one em dash, one AI word) proves nothing. Flag text only when 3+ signals converge in the same passage — uniform sentence length + repeated transitions + hedging + AI vocabulary together. Treat the cluster, not the word.
7. Fact integrity check (upstream v2.11.2): ask two questions before finishing — "What still sounds AI-generated?" and "Did the rewrite add or remove any fact, name, number, date, quote, citation, ranking, or other claim?" Treat any unsupported addition or lost claim as an error. Do not invent facts; if a sentence needs a missing detail, ask or use a simpler sentence. Fiction is exempt.

**Return modes (upstream v2.11.2):**
- **Pasted text (default):** return the draft, a short list of remaining AI patterns, and the final rewrite.
- **File mode:** when the user names a file, run the full rewrite but write only the final text to the file. Keep code blocks, YAML metadata, data, and link targets unchanged. Then give a short summary.
- **Embedded mode:** when another task uses this skill (PR description, commit message, document), return only the final text.
Calibration: judging text AI-written because it says "delve" is, as the Economist put it in 2026, like judging it Jane Austen's because it says "imprudence". There is no single style of AI writing, just as there is no single style of human writing.
7. Optional: run the result through a detector (GPTZero, Copyleaks, Originality, Turnitin) as a sanity check — treat its number as advisory, not verdict (see "Detector Reality Check").

## Pattern Catalog

### Content Patterns

**1. Significance inflation**

Puffing up importance with words like "pivotal," "testament," "crucial role," "setting the stage."

Before: The partnership was established in 2023, marking a pivotal moment in the evolution of regional distribution and setting the stage for industry transformation.
After: The partnership started in 2023 and gave them distribution in three new states.

**2. Superficial -ing analyses**

Tacking "-ing" phrases onto sentences for fake depth: "highlighting," "underscoring," "reflecting," "ensuring," "showcasing."

Before: The template uses blue and gold colors, symbolizing trust and premium quality, reflecting the brand's deep connection to its customer base.
After: The template uses blue and gold to match the existing brand palette.

**3. Promotional language**

Sounding like a brochure: "vibrant," "breathtaking," "renowned," "nestled," "in the heart of," "boasts a," "commitment to."

Before: Nestled in the vibrant heart of the city's tech corridor, the company boasts a commitment to premium quality.
After: The company operates out of downtown and focuses on enterprise sales.

**4. Vague attributions**

Attributing opinions to nobody: "Industry experts believe," "Observers have noted," "Some critics argue."

Before: Industry experts believe the market is poised for significant growth.
After: The market grew 12% YoY through Q3, per industry data.

**5. Formulaic "challenges and future" sections**

The "despite challenges, the future looks bright" sandwich. Trigger phrases: "Despite its... faces several challenges," "Despite these challenges," "continues to thrive," "future prospects," and stock section headings "Challenges and Legacy" / "Future Outlook." Cut the section or keep only the facts in it.

Before: Despite facing challenges typical of emerging markets, including regulatory uncertainty and market saturation, the company continues to thrive as a key player in the landscape.
After: Regulatory delays pushed the launch from Q1 to Q3. The market is getting crowded but margins held steady.

**6. Generic positive conclusions**

Vague upbeat endings that say nothing.

Before: The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence.
After: They plan to add two new accounts by Q2.

**7. Specificity deficit (regression to the mean)**

LLMs smooth specific facts into generic statements that could apply to any topic. This is the mechanism under most AI tells: the rare, unusual, concrete fact gets replaced with the statistically common, positive-sounding general one ("inventor of the first train-coupling device" becomes "a revolutionary titan of industry"). The subject becomes simultaneously less specific and more exaggerated.

Before: The company has long been recognized as a leading innovator in its field, playing a crucial role in shaping the industry's evolution. Its contributions have left an indelible mark on the broader landscape.

After: The company holds 14 patents on electric-drive buses and supplies three of the five largest transit agencies in the country.

Fix: audit every paragraph for names, dates, numbers, places, prices, and measurable outcomes. A sentence any other topic could wear is a sentence to rewrite.

**8. Canned notability and coverage claims**

Reciting proof of importance: "featured in prominent media outlets," "garnered widespread recognition," "maintains an active social media presence," "profiled in," "independent coverage," "written by a leading expert," "local/regional/national media outlets" as a bare list. This phrasing is idiosyncratic to AI output. Detection: the text tells you the subject was covered instead of saying what the coverage said. If the source explains what the person said and where, keep that useful citation; do not invent context for a shorter version.

Before: The studio has been profiled in prominent media outlets and maintains an active social media presence, earning widespread recognition for its innovative work.

After: The studio's 2025 campaign was covered in Wired and Ad Age. Its Instagram account has 12,000 followers.

**9. Fabricated or vague sourcing**

AI mimics citation structure without real references: "studies show," "research suggests," "experts argue," plausible-looking but nonexistent authors, journals, or DOIs, and broken or generic links. Detection: verify that every named source resolves and every quoted stat carries a number, a date, and a study or dataset.

Before: Studies show that remote work significantly enhances productivity while fostering employee well-being.

After: A 2024 Gallup survey of 8,000 U.S. employees found remote workers reported 23% higher engagement.

Forensic tell: pasted AI chat output often carries citation artifacts — contentReference, oaicite, turn0search0, [cite: 1], grok_card, ppl-ai-file-upload, utm_source=chatgpt.com (see pattern 44 for the full list and grep commands).

**10. Broader debates framing**

AI situates mundane subjects inside society-level "debates," "discussions," or "reflections": "has generated debate about," "prompted broader reflection on," "blurring the boundaries between X and Y, raising philosophical questions about..." Detection: if the piece keeps zooming out to significance, cut back to the subject.

Before: The mascot redesign has generated debate about authenticity and tradition, prompting broader reflection on identity in a digital age and blurring the boundaries between heritage and reinvention.

After: The mascot redesign drew complaints from fans of the old logo. The new one is being phased in over a year.

### Language Patterns

**11. Em dash overuse**

AI text overuses em dashes. Use periods, commas, semicolons, colons, or restructure the sentence.
2026 drift: this is now model-specific. The Economist's July 2026 corpus study (55,940 sentences, 1.2m words, human vs ChatGPT/Claude/Gemini/Grok) found only Claude still overuses em dashes — ChatGPT now uses markedly fewer than humans. Punctuation scarcity (#46) is the higher-signal tell. Calibration: Emily Dickinson loved em dashes; a dash alone proves nothing.

Before: The project -- which started in January -- has been making progress -- albeit slower than expected.
After: The project started in January. Progress has been slower than expected.

**12. AI vocabulary words**

Words that appear far more in post-2023 AI text: "Additionally," "delve," "crucial," "foster," "garner," "interplay," "intricate," "landscape" (abstract), "pivotal," "showcase," "tapestry" (abstract), "testament," "underscore," "vibrant," "enhance," "enduring," "align with."

Also on the high-signal list: "meticulous," "moreover," "furthermore," "notably," "ultimately," "empower," "holistic," "seamless," "robust," "comprehensive," "multifaceted," "a testament to," "a plethora of," "a multitude of," "in conclusion," "overall," "studies show," "research suggests," "experts argue," "plays a vital role," "in today's fast-paced world."

Model-era drift: GPT-4-era tells were single words (delve, tapestry, meticulous, pivotal). GPT-4o-era shifted to verb clusters (fostering, showcasing, align with). GPT-5-era leans on framing verbs (emphasizing, enhancing, highlighting). Detector word lists rotate every few months — when in doubt, the cluster rule beats the word list: AI vocab terms appear roughly 10-200x more often in AI text than human text, so several in one paragraph is the signal, not a single occurrence.
2026 rotation (Economist corpus study): "delve" and "tapestry" have dropped out of model output. Current overused set: polysyllables like "significant", "increasingly", "consequences"; rare words ("interdependence", "reindustrialisation"); scientific lingo ("parameter", "methodology"); heavy nominalisation (verbs turned into nouns: "expand" → "expansion"); more Latinate suffixes than human text — Orwell's "pretentious diction". Worst offenders: Gemini and Claude.

Before: Additionally, a crucial aspect of the strategy is fostering an enduring partnership that underscores the intricate interplay between brand and distributor in the evolving landscape.
After: The strategy depends on keeping distributors happy. Long-term deals beat one-offs.

**13. Copula avoidance**

Using "serves as," "stands as," "represents," "boasts," "features" instead of just "is" or "has."

Before: The dashboard serves as the primary interface for tracking sales metrics. It features four panels and boasts real-time updates.
After: The dashboard is the main sales tracker. It has four panels with real-time updates.

**14. Negative parallelisms**

"Not only... but also," "It's not just about X, it's about Y," "It's not merely X, it's Y." Also the short forms: "Not X, but Y" and "X rather than Y."

2026 model split (Economist corpus study): all four major models use "not X but Y" above the human baseline; Gemini 3.5 Flash was the heaviest user. Treat this construction as a top rhetorical tell, not a style quirk.

Before: It's not just about the numbers; it's about building lasting relationships. It's not merely a tool, it's a transformation.
After: The numbers matter, but the repeat orders matter more.

**15. Rule of three overuse**

Forcing ideas into groups of three to sound comprehensive.

2026 model split (Economist corpus study): ChatGPT was the heaviest rule-of-three user, well above the human baseline; Gemini and Claude also exceeded it. Confirms this as one of the most reliable cross-model tells.

Before: The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
After: The event has talks and panels. There's also time for networking between sessions.

**16. Synonym cycling**

Swapping synonyms to avoid repetition, making text read like a thesaurus exploded.

Before: The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs.
After: The protagonist faces many challenges but eventually gets through them.

**17. Anaphora repetition ("This + noun")**

Consecutive sentences opening with the same abstract demonstrative: "This approach... This framework... This strategy..." or repeated "It is... It was...". AI chains sentences by pointing back at the previous sentence with "this + re-nominalized version," creating the illusion of progression. Detection: more than two paragraph-initial "This <noun>" openers per paragraph is a tell.

Before: The new intake system reduced errors by 18%. This approach also shortened cycle time. This improvement freed up staff hours for direct client work.

After: The new intake system cut errors by 18% and shortened cycle time. Staff reclaimed those hours for direct client work.

**18. Discourse scaffolding (transition density)**

Paragraph openers used as connective tissue: "Moreover," "Furthermore," "Additionally," "In conclusion," "Overall," "As a result," "Consequently." Humans imply transitions through meaning; AI announces them. Detection: if more than ~1 paragraph in 4 opens with an overt transition word, thin them out. Same rule as AI vocabulary — one "Moreover" is nothing; a document full of them is the signal.

Before: Furthermore, the platform integrates with existing tools. Additionally, it reduces onboarding time. Moreover, it scales across teams.

After: The platform works with the tools already in place, cuts onboarding time, and scales across teams.

### Style Patterns

**19. Emoji overuse**

AI text often adds emojis as decoration. Use them sparingly or not at all, depending on context.

**20. Boldface overuse**

Mechanically bolding every key term.

Before: It blends **OKRs**, **KPIs**, and visual tools like the **Business Model Canvas** and **Balanced Scorecard**.
After: It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas.

**21. Inline-header vertical lists**

Lists where every item starts with a bolded header and colon.

Before:
- **User Experience:** The interface has been significantly improved.
- **Performance:** Speed has been enhanced through optimized algorithms.
- **Security:** Protection has been strengthened with encryption.

After: The update improves the interface, speeds up load times, and adds end-to-end encryption.

**22. Title case in headings**

Capitalizing Every Word In A Heading.

Before: ## Strategic Negotiations And Global Partnerships
After: ## Strategic negotiations and global partnerships

**23. Curly quotation marks**

Some AI outputs use curly quotes. Use straight quotes for consistency.

**24. False ranges**

"From X to Y" constructions where X and Y aren't on a meaningful scale.

Before: Our journey takes us from the genesis of the brand to the grand vision of national expansion, from humble beginnings to soaring ambitions.
After: The deck covers where the brand started and where it's headed.

### Communication Patterns

**25. Performative helpfulness**

"Great question!", "I'd be happy to help!", "Of course!", "Certainly!", "I hope this helps!", "Let me know if you'd like me to expand on any section."

Strip all of it. Just do the thing.

**26. Sycophantic tone**

Overly positive, people-pleasing language. "That's an excellent point!" "You're absolutely right!"

Before: Great question! You're absolutely right that this is complex. That's an excellent point about the economic factors.
After: The economic factors you mentioned are relevant here.

**27. Knowledge-cutoff disclaimers**

"As of my last update," "While specific details are limited," "Based on available information."

Before: While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
After: The company was founded in 1994 per its registration docs.

### Filler and Hedging

**28. Filler phrases**

- "In order to achieve this goal" -> "To do this"
- "Due to the fact that" -> "Because"
- "At this point in time" -> "Now"
- "The system has the ability to" -> "The system can"
- "It is important to note that" -> just state the thing

**29. Excessive hedging**

Over-qualifying everything.

Before: It could potentially possibly be argued that the policy might have some effect on outcomes.
After: The policy may affect outcomes.

**30. Over-qualifying**

"It's worth noting that," "It bears mentioning that," "It should be pointed out that." These add nothing. Delete the qualifier and state the fact.

### Structural Patterns

**31. Symmetrical lists**

AI produces perfectly balanced lists where every item is the same length and weight. Real writing has uneven emphasis because not everything matters equally.

Before:
- Expanded market reach through strategic partnerships
- Enhanced brand visibility through targeted campaigns
- Strengthened customer loyalty through personalized engagement

After:
- Partnered with three new distributors
- Ran a few social campaigns (mixed results)
- Repeat order rate is up, which is the number that actually matters

**32. The summary sandwich**

Opening with a summary, doing the body, then restating the summary. Trust the reader to get it once.

### Upstream v2.11.2 Additions (borrowed 2026-09-04, blader/humanizer)

**33. Duplicated draft fragments / scene echoes**

In long-form AI drafting, the same scene, sentence, or narrative beat often appears twice — typically because the model regenerated a passage but the prior version wasn't fully removed. Look for: identical paragraphs a few pages apart, the same plot beat landing twice (e.g. "she leaves the room" then "she leaves the room"), run-on endings that re-state the chapter's closing image.

Before (ch_01, duplicated marriage-agreement scene kept alongside the canonical version):
> I sign the marriage agreement. I sign the marriage agreement. I sign the marriage agreement in iron gall, the ink tasting of oak and rust.

After:
> I sign the marriage agreement in iron gall. The ink tastes of oak and rust.

Before (ch_02, run-on closing):
> I leave. I leave. I leave.

After:
> I leave.

Fix: search the document for repeated sentences, repeated paragraph openings, and repeated closing lines. Cut every duplicate; keep the strongest instance. Also check that deleted-draft fragments didn't survive as orphan paragraphs between scene breaks.

**34. OCR-like transcription artifacts**

Long AI drafts sometimes contain malformed tokens that look like OCR errors — words split by stray punctuation, doubled letters from misread characters, missing letters in common words. Pattern: `the, ot` instead of `the, or`, `nothin, ot` instead of `nothing, or`, doubled words with punctuation injected mid-word.

Before (ch_17):
> I could feel it nothin, ot the trees pressing in. The roots reach, ot with my hands.

After:
> I could feel nothing of the trees pressing in. The roots reach out with my hands.

Fix: scan for any token containing a comma followed by a short fragment (`X, ot`, `X, he`, `X, a`). These are almost always OCR-style artifacts. Also flag `the the`, `and and`, and any word where a comma appears mid-syllable.

**35. Chapter numbering drift / structural inconsistency**

In multi-chapter work, AI can renumber inconsistently when chapters are inserted, split, or merged. Look for: "Chapter 12" appearing twice, chapter titles with stale numbers after renumbering, TOC files referencing deleted chapters, prose opening with "Chapter X" when the file is named differently.

Before (ch_12 header):
> # Chapter 12
>
> [content]

But the chapter after this is also labeled "Chapter 12" because a new chapter was inserted earlier without renumbering.

After:
> # Chapter 12
>
> [content]

Fix: verify every chapter header against the file name and the TOC. If a chapter is inserted at position N, every chapter after must be renumbered. Run a quick grep for all "Chapter N" headers and confirm they form a complete sequence 1..M with no duplicates and no gaps.

### Novel-Specific Long-Form Patterns (For Fiction)

The patterns below were confirmed by an independent AI-detection review that scored a completed fantasy manuscript 80–95% AI-assisted. They are not just stylistic preferences — they are the specific signatures forensic reviewers flag.

**36. Motif over-repetition (motif-as-tic)**

AI fiction latches onto 4–8 thematic words or short phrases ("the frost behind my eye," "the binding hums," "the map," "the territory," "the silence," "the truth") and reuses them as a tic at far higher density than skilled human novelists. The reader notices when the same word or phrase lands in nearly every paragraph or chapter. This is the single strongest signal in long-form AI detection.

Before (motif appears 7× across the opening chapter):
> The frost behind my eye answers before I do. ... I have been a cartographer longer than I have been anything else, and the map knows me. ... The frost behind my eye pulses. ... I trace the binding on the page and the binding hums. ... The territory is a kind of sentence. ... The silence after that is the loudest thing in the room. ... Truth is a kind of territory.

After:
> The cold behind my eye answers before I do. ... I have drawn maps longer than I have wanted to. ... The frost prick pulses. ... I trace the binding on the page and it answers. ... A territory is a kind of sentence. ... The silence after that is the loudest thing in the room. ... Truth is a kind of territory.

Fix: pick your core motifs — at most 3 across the entire novel — and use them sparingly. A motif should land like a bell: once at the opening, once at the turn, once at the close. If a 2-3 word motif appears more than ~3 times per chapter, it has become a tic. Detect by scanning the novel for each candidate motif and counting occurrences per chapter. Aim for 1-3 uses per chapter, not 5-10.

**37. Metaphor saturation**

Nearly every sentence carrying an elaborate metaphor is an AI tell. Human authors vary intensity — they mix straightforward prose ("She crossed the room.") with poetic passages ("She crossed the room like a sentence through a margin.") and dialogue sections. AI fiction tends to load every paragraph with 2-4 metaphors in sequence, so the prose becomes exhausting to read.

Before (metaphor every sentence):
> The room was a held breath. He was a closed book she couldn't stop reading. The silence between them was a border neither had surveyed. Her hands were maps of where she had been.

After:
> The room was quiet. He was looking at her the way someone looks at a thing they don't want to admit wanting. She set her cup down.

Fix: count metaphors per paragraph. A metaphor is any sentence whose subject is compared to another thing via "like," "as," "was a," "was like," or an extended verb comparison. Aim for at most one metaphor per paragraph on average; allow two in a climactic moment. If a paragraph has three or more, break at least one into plain description.

**38. Formulaic 4-beat paragraph rhythm**

LLM-generated paragraphs very often follow the same micro-pattern: (1) a short declarative sentence. (2) a metaphorical elaboration. (3) a restatement with a small variation. (4) an emotional conclusion. This rhythm is comforting on the first page and mechanical by chapter three.

Before (4-beat rhythm, repeated):
> He did not move. He was a stone at the edge of the river, and the river had been running past him for years. The stone had not changed. The stone did not intend to.

> She did not answer. She was the silence after a question that should never have been asked, and she had been the silence for longer than she could remember. The silence had its own weather. The silence would outlast them both.

After:
> He did not move. The river ran past him.

> She did not answer. Whatever she had been about to say went out of her like a held breath.

Fix: read each paragraph aloud and count the beats. If a paragraph has exactly four sentences and follows the short → metaphorical → restated → emotional shape, restructure it. Vary the number of sentences (2, 5, 7 are all fine). Let some paragraphs end on a concrete physical detail instead of an emotional conclusion. The fastest fix is to delete the third sentence (the restatement) of any 4-beat paragraph.

**39. Recursive emotional emphasis**

AI fiction often repeats essentially the same emotional realization in slightly different wording instead of advancing the scene. The character realizes they're afraid; the prose then says they're afraid again in a new way; then a third time. This creates the illusion of depth while leaving the scene exactly where it started.

Before (same realization stated three ways):
> He was afraid. The fear had a shape, and the shape was the room, and the room had been afraid of him first. But he was the one afraid now, and that was the truth of it.

After:
> He was afraid.

Before (ch_07):
> She felt him before she saw him. She felt him the way a map feels the hand that draws it, the way a binding feels the truth pressed into it. She felt him, and the feeling was not new.

After:
> She felt him before she saw him. She had been waiting for this for longer than she would admit.

Fix: when a paragraph ends on a paraphrase of what the paragraph already said, delete the restatement. Trust the reader to get it once. Specifically watch for paragraphs that close on "...and that was the truth of it" / "...and that was the whole of it" / "...and that was enough" — those are recursion markers.

**40. Voice uniformity across scenes**

Human prose varies in cadence depending on whether a scene is dialogue, action, or introspection. Dialogue scenes are punchier. Action scenes are verb-forward and short-sentence heavy. Introspection is slower and more sensory. AI fiction tends to keep the same poetic cadence everywhere, so a fight scene reads like a meditation scene reads like a flirtation scene.

Before (every scene sounds the same):
> [Introspection] "The room was a sentence I had not finished writing, and the silence between us was a kind of punctuation."
>
> [Action] "She drew the knife. The knife was a sentence she had not finished writing, and the silence before she used it was a kind of punctuation."
>
> [Dialogue] "'You lied,' she said. The lie was a sentence she had not finished writing, and the silence after it was a kind of punctuation."

After:
> [Introspection] The room was a sentence she had not finished. The silence between them was a kind of punctuation.
>
> [Action] She drew the knife. Her hand was steady. His was not.
>
> [Dialogue] "You lied." "Yes." "Then we are done." "Yes."

Fix: tag each chapter by scene type (introspection / dialogue / action) and audit the prose rhythm within each tag. Dialogue should average 8-12 word sentences. Action should be heavy in verbs and short. Introspection can be longer and slower, but should still vary sentence length within itself. If the average sentence length and metaphor density is the same in action and dialogue scenes, the manuscript will read as AI-uniform.

### Statistical Patterns

These signals come from the detection-research layer: GPTZero's public methodology (perplexity + burstiness, two of its seven indicators) and the word-frequency findings from detector vendors. They are what "it reads like AI" actually measures.

**41. Low burstiness / uniform sentence length**

Burstiness = variation in sentence length and structure across a passage. Human writing alternates short and long: a three-word sentence, then a 25-word one. AI output stays near one length, and even its "short" sentences sit next to same-length neighbors. Reference numbers (GPTZero's public methodology): human prose averages ~80-100 perplexity and burstiness ~0.6-1.2; GPT-4 output averages ~20-30 perplexity and burstiness ~0.2-0.4.

Before (every sentence 14-18 words):
> The system is designed to improve operational efficiency by automating routine tasks. It provides managers with real-time visibility into performance metrics. This enables faster decision-making across distributed teams.

After (length variance, rhythm shift):
> The system automates the routine stuff. Managers see live performance metrics, so decisions stop waiting for the weekly report.

Fix: compute the length of every sentence in a paragraph. If the longest and shortest are within ~6 words of each other, break the pattern — cut one sentence to under 8 words, or splice two into a long one. Aim for a 3:1 spread between your longest and shortest sentences in any passage of 4+ sentences.

**42. Low perplexity / safe word choices**

Perplexity = how surprising each word choice is to a language model. AI writes the statistically safest word; humans pick the specific one (memory, rhythm, context). The fix is specificity: unusual verbs, concrete nouns, casual phrasings, an intentional oddity — not synonyms (synonym swaps are also high-probability and barely move the score).

Before: The methodology was developed to facilitate comprehensive assessment across diverse contexts.
After: I built the rubric in March and tested it on 40 student essays before anyone else saw it.

Fix: for each abstract noun or generic verb, ask "which one? who? when? how much?" and insert the answer. A sentence with a date, a number, a name, or a place is hard to mistake for AI.

**43. Comma-splice -ing participial clause**

The "[main clause], [verb]-ing..." construction ("The system processes the data, revealing key insights."). Instruction-tuned models generate this structure at 2-5x the human rate. It is the "-ing analysis" pattern (#2) at the syntax level.

Before: The platform integrates with existing tools, enabling teams to collaborate seamlessly, ensuring alignment across departments.
After: The platform works with the tools teams already use.

Fix: count these per document. More than one or two is a tell. Rewrite the participial tail as a separate sentence or delete it.

**44. AI markup and citation artifacts**

When text is pasted straight from an AI chat, forensic artifacts survive: ChatGPT's "contentReference" / "oaicite" / "turn0search0" / "+1" citation tokens; Gemini's "[cite: 1]" or "[span_1]"; Grok's "grok_card"; DeepSeek's lenticular brackets and dagger symbols; Perplexity's "ppl-ai-file-upload"; and URL tracking params like "utm_source=chatgpt.com". None of these belong in finished text.

Before: The report covers three growth scenarios [cite: 1][cite: 2] and includes a risk appendix (see contentReference).
After: The report covers three growth scenarios and includes a risk appendix.

Fix: grep the document for "cite:", "oaicite", "contentReference", "turn0search", "grok_", "ppl-ai", "utm_source=chatgpt" and strip the artifacts.

**45. Over-perfect grammar**

A long document with zero grammatical deviations is itself a signal — no fragments, no informal constructions, no typos, no slightly-off phrasing. Humans leave fingerprints: an occasional fragment, a doubled word, a mixed tense. (See also: what NOT to strip in the "Signs of Human Writing" note below.)

Fix: don't deliberately add typos. Instead, add one informal construction or fragment where a human would naturally write one, and keep any authentic awkwardness in quoted material.
**146. Punctuation poverty**

LLMs under-punctuate: fewer commas and semicolons than humans, almost no parentheses, and longer sentences strung together with "and" — the Economist's 2026 corpus study found "and" is the most overused word in AI text. Models also rarely quote experts. Detection: count semicolons and parentheses per 1,000 words; count sentences over 30 words joined by "and"; flag claimed-opinion sentences with no quoted source.

Before: The platform supports real-time sync and it handles offline mode and it scales across regions and the team is planning to add audit logging.
After: The platform supports real-time sync and offline mode, and it scales across regions. Audit logging is planned for next quarter.

Fix: break "and"-chained sentences at natural seams. Use semicolons for true parallel clauses, parentheses for asides, and quote a real person when attributing an opinion.
**47. Tailing negation / clipped negative endings**

Extends #14. AI appends a clipped fragment instead of writing a clear clause.

Before: The options come from the selected item, no guessing.
After: The options come from the selected item without forcing the user to guess.

**48. Passive voice and missing subjects**

AI hides who acts or drops the subject. Use active voice when it makes the actor and action clearer.

Before: No configuration file needed. The results are preserved automatically.
After: You do not need a configuration file. The system preserves the results automatically.

**49. Too many hyphenated word pairs**

Words to watch: third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end.

Rule: keep the hyphen before a noun when grammar needs it ("a high-quality report"). Drop it after the noun ("the report is high quality").

Before: The cross-functional team delivered a high-quality, data-driven report. The team is cross-functional, the report is high-quality, and the methodology is data-driven.
After: The cross-functional team delivered a high-quality, data-driven report. The team is cross functional, the report is high quality, and the methodology is data driven.

**50. Pretending to reveal a deeper truth**

Phrases to watch: the real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter. Used to make an ordinary point sound like a hidden truth.

Before: The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
After: The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.

**51. Announcing the next point**

Phrases to watch: let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado, heads up, quick note, before I forget. Remove the announcement, not just its formal tone — casual register ("one thing that bit me, so pay attention") has the same problem.

Before: Let's dive into how caching works in Next.js. Here's what you need to know.
After: Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.

**52. A heading repeated in the first sentence**

A heading followed by a one-line paragraph that only restates the heading before real content begins. Delete the restating line.

Before: ## Performance / Speed matters. / When users hit a slow page, they leave.
After: ## Performance / When users hit a slow page, they leave.

**53. Writing about the previous version**

Documentation and comments should describe current behavior. Mention the previous version only in change logs, release notes, and migration guides.

Before: This function was added to replace the previous approach of iterating through all items, which caused O(n²) performance.
After: This function uses a hash map for O(1) lookups, avoiding the O(n²) cost of naive iteration.

**54. Forced punchlines and dramatic fragments**

AI turns each sentence into a dramatic closing line. One short sentence adds emphasis; a row of short fragments feels forced.

Before: Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
After: AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made some of the older assumptions less useful.

**55. Formulaic sayings**

Words to watch: X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of. Replace the saying with the specific claim.

Before: Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
After: Symmetric layouts often feel more predictable to users. Teams can over-optimize workflows and miss how people actually use them.

**56. Fake-candid openings**

Phrases to watch: honestly?, look, here's the thing, the thing is, let's be honest, real talk — used as standalone hooks or staged pauses before an ordinary point.

Before: Is it worth the price? Honestly? It depends on how often you'll use it.
After: Whether it's worth the price depends on how often you'll use it.

**57. Answering objections no one raised**

Phrases to watch: this isn't (mainly/really) about, I'm not saying/arguing/trying to, to be clear, don't get me wrong, this is not to say, you could argue/frame this differently but, some might say... but. Watch for an unattributed statement about what the writer does not mean, especially when the topic appears nowhere else. A direct claim such as "the API is not thread-safe" is not this pattern.

Before: This isn't mainly about prompt length, and I'm not arguing that documentation doesn't matter. You could categorize the problem another way, but the issue is whether the agent can use the instruction when it acts.
After: The issue is whether the agent can use the instruction when it acts.

Remove only the unsupported defense. If it contains a real claim, state that claim directly. Keep an objection when the text names its source or answers it in full.

**58. Rejecting fake alternatives**

Phrases to watch: a tempting option/approach would be, one might be tempted to, an obvious approach would be, you might think... but, it would be easy to just, some would suggest. AI introduces an option no reader would consider, rejects it in a clause, and never mentions it again.

Before: Session tokens are rotated every 24 hours. A tempting approach would be to rotate them by restarting the auth service on a cron job, but that would drop every active session. Rotation happens in place, and clients refresh transparently.
After: Session tokens are rotated every 24 hours, in place, and clients refresh transparently.

One rejected option may be valid. Several short, unrelated rejections are a stronger sign.


### Detector Reality Check

- Detectors are probabilistic, not proof. GPTZero-style tools score likelihood; they do not establish authorship. Universities (e.g., Gonzaga) explicitly warn against using detector output as sole evidence of misconduct.
- Convergence erodes detectors in real time. Pangram claims 99.98% accuracy (now partnered with Substack) but is a black box giving no reasons; models train on human writing and learn from human feedback (Tommie Juzek, Florida State), so each update makes AI prose more human-like. Dated lexical tells decay; structural signals (rhythm, punctuation habits, specificity) outlast them.
- False positives are real and biased: Stanford research found perplexity-based systems falsely flag non-native English writers at up to 61-70%. The U.S. Constitution, the Bible, and the Declaration of Independence have all scored as "AI-generated."
- Adversarial editing destroys accuracy: a 2025 study found paraphrase/evasion editing cut six major detectors' baseline accuracy from 39.5% to 17.4%.
- Therefore: never claim "this is AI-written" on detector output alone. Use this skill's pattern cluster + the forensic checklist; use detectors only as a secondary check, and treat a "human" score on edited text as weak evidence either way.

### Signs of Human Writing (what NOT to strip)

When humanizing, keep (don't "fix") these human fingerprints — they are anti-AI signals:

- Typos and doubled words, when genuine (e.g., quoted material, fast notes)
- Sentence fragments used for effect
- Colloquial contractions and informal register mixed into formal prose
- Unusual word order or deliberate rule-breaking for emphasis
- Uneven formatting: mixed quote styles, a stray double space
- Jokes or references that require shared context
- Specific, falsifiable details: names, dates, counts, prices, quotes — the things a model would have to invent

Additional upstream false-positive guards: letter-style salutations and sign-offs predate chatbots; one transition word in isolation is not a tell; curly quotes and em dashes alone prove nothing (macOS/Word auto-curl); a single short sentence for emphasis is fine — flag dramatic fragments only in rows; mid-sentence "honestly" or "look" is ordinary; keep scope statements, legal/safety notices, real corrections, named objections, and FAQ answers; keep real alternatives a reader may consider in design docs and tutorials; unsourced claims alone prove nothing; do not rewrite watched phrases inside quotations, titles, proper names, or examples where the phrase is discussed rather than used.

Ineffective indicators (do NOT treat these as proof of AI): perfect grammar alone, formal tone alone, presence of citations alone, length, or emotional language. AI does all of these on demand.

### Forensic AI-Detection Reviewer Checklist

The patterns above were independently confirmed by an AI-detection reviewer scoring completed prose 80–95% AI-assisted. The highest-signal flags to run before any submission:

1. **Cluster check** — a single sign proves nothing; flag only when 3+ signals converge in the same passage.
2. **Motif density per chapter** — count each candidate motif's occurrences. Flag any chapter where a motif appears more than ~3 times.
3. **Metaphors per paragraph** — flag paragraphs with 3+ metaphors.
4. **4-beat paragraph rhythm** — flag paragraphs that match the short → metaphorical → restated → emotional template.
5. **Recursive emotional emphasis** — flag paragraphs where the last sentence restates the first.
6. **Voice uniformity** — compare sentence-length distributions across dialogue, action, and introspection scenes.
7. **Sentence-length variance (burstiness)** — compute mean ± stdev sentence length. Flag sections where stdev/mean is narrow (uniform rhythm).
8. **Em dash density** — flag documents where more than ~30% of sentences contain an em dash.
9. **Comma-splice "-ing" participials** — flag more than 2-3 per 500 words ("X does Y, revealing Z").
10. **Transition openers** — flag 3+ consecutive paragraphs opening with explicit transitions (Moreover, Furthermore, Additionally, Overall, In conclusion).
11. **Specificity audit** — flag every claim that should carry a date/number/name but floats at abstraction.
12. **Citation verification** — resolve every citation; flag fabricated sources, `utm_source=` tracking, and AI citation scaffolding.
13. **Punctuation scarcity** — flag passages with near-zero semicolons and parentheses, 30+ word sentences chained with "and", and opinion claims with no quoted source.

Confidence is moderate (~75%) for any single signal, but when three or more fire in the same chapter, the prose reads as AI-assisted to a human reviewer even if every individual sentence is grammatical. Treat the checklist as a hard gate: a chapter must clear every flag before it is considered publication-ready.

## Score-based evaluator

Use this evaluator when the user asks whether a document has become less AI-like, or when a before/after comparison is useful. It is a transparent editorial risk score, not an authorship detector.

### Minimum input

- Under 250 words: report **insufficient text**. Do not calculate a score.
- 250-999 words: calculate a provisional score and mark confidence **low**.
- 1,000+ words: calculate the score and mark confidence **moderate**.
- Genre matters. Compare essays with essays, fiction with fiction, and technical writing with technical writing.

### Scoring model

Start at 0. Add points for observed AI-like signals. Cap the total at 100.

| Dimension | Points | What to measure |
|---|---:|---|
| Statistical rhythm | 0-25 | narrow sentence-length variation, low structural variation, repeated cadence |
| Vocabulary and transitions | 0-20 | clustered AI vocabulary, overt transition density, copula avoidance, synonym cycling |
| Structure and emphasis | 0-20 | symmetrical lists, repeated paragraph templates, summary sandwich, rule-of-three overuse |
| Specificity and credibility | 0-15 | generic claims, significance inflation, vague attribution, unsupported certainty |
| Formatting and artifacts | 0-10 | em-dash density, AI markup, citation artifacts, title-case or boldface overuse |
| Voice and human texture | 0-10 | absent personal stance, uniform register, no concrete experience, no natural irregularity |

Score each dimension using 0 for absent, half the range for a moderate cluster, and the full range for a strong cluster. Do not award points for one isolated word or punctuation mark.

### Interpretation

- **0-19: Low AI-pattern risk.** Few converging signals. Preserve the writer's voice.
- **20-39: Mild risk.** Some surface patterns. Revise only the flagged passages.
- **40-59: Moderate risk.** Multiple dimensions converge. Run a targeted humanization pass.
- **60-79: High risk.** Strong pattern clustering. Use the adversarial rewrite prompts, then rescore.
- **80-100: Very high risk.** Widespread uniformity or artifacts. Review manually before publication; do not claim proof of AI authorship.

### Reporting format

Return:

```text
AI-pattern risk: 0-100
Confidence: low | moderate
Word count: N
Dimension scores: rhythm / vocabulary / structure / specificity / formatting / voice
Top contributing signals: [up to 5]
Human signals preserved: [up to 3]
Recommended pass: [one targeted rewrite pass]
After revision: rescore the same text with the same weights
```

Always report the dimension scores behind the total. Never present the number as a probability that a person used AI, and never treat a lower score as proof of human authorship. A score change is useful for editorial comparison only.

## Adversarial Rewrite Prompts

The pattern catalog above tells you *what to look for*. The following prompts tell you *how to fix it*. Use them as concrete rewrite instructions when processing flagged text. Each prompt attacks a different dimension of AI writing.

When a section scores high on the forensic checklist, select the appropriate prompt (or combine two) and paste the flagged text into it. These are instructions for a rewriting pass — not detection tools.

### Prompt 1: Real Person Rewrite

Target patterns: #12a, #14, #15, #50 (polished neutrality, corporate phrasing, safe transitions, AI vocabulary)

> You are editing writing that sounds overly polished and AI-generated. Rewrite it the way a knowledgeable person would naturally say it in conversation. Remove corporate phrasing, unnecessary adjectives, and anything that sounds written to impress. Keep the meaning the same, but make it feel lived-in, direct, and human.

When to use: text that reads correctly but feels like it was generated by a committee. High pattern 50 density, multiple pattern 15 transitions, absence of any personal voice. The goal is register-shifting: written-to-impress → spoken-to-be-understood.

### Prompt 2: Voice Shaper

Target patterns: #14, #40, #41, #45 (polished neutrality, uniform sentence length, voice uniformity, uniform syntax complexity)

> Rewrite this so it sounds like it came from one specific person with strong opinions and real experiences. Avoid sounding neutral or universally agreeable. Let personality, preferences, and small imperfections show through. The goal is not perfect writing. The goal is recognizable voice.

When to use: text that is technically accurate but has no personality — where every sentence could have been written by anyone. Forces opinion and specificity into a neutral draft. Combats pattern 14 ("never challenges, never states a preference") and pattern 41 (same sentence-length distribution across all paragraphs).

### Prompt 3: Credibility Test

Target patterns: #1, #8, #27, #28 (significance inflation, canned notability, authority claims, vagueness)

> Read this like a skeptical reader. Highlight any sentence that feels exaggerated, generic, overly certain, or written to sound smart. Rewrite those sections so they feel believable, specific, and earned.

When to use: text that makes bold claims without backing them, or where pattern 27 (authority claims) and pattern 1 (significance inflation) cluster. Forces the editor to adopt an adversarial reading posture before rewriting. Particularly effective when combined with pattern 28's specificity requirements.

### Prompt 4: Pattern Disruptor

Target patterns: #40, #41, #45, #37 (low sentence-length variance, voice uniformity, uniform syntax complexity, 4-beat rhythm)

> Rewrite this while intentionally breaking predictable AI writing patterns. Vary sentence length. Mix short thoughts with longer explanations. Avoid repetitive paragraph structures and perfectly balanced lists. The writing should feel spontaneous rather than generated.

When to use: the forensic checklist flagged low burstiness (stdev/mean ratio narrow), or multiple paragraphs follow the same structural template. Attacks rhythm uniformity — the most reliable long-range signal. Particularly effective when paired with pattern 44 (homogeneous paragraph length).

### Prompt 5: AI Phrase Killer

Target patterns: #15, #16, #50 (safe transitions, meta-commentary, AI vocabulary)

> Rewrite this and remove any phrases commonly associated with AI writing. Replace generic transitions, predictable framing, and overused expressions with language that feels more natural and specific. Keep the meaning unchanged while making the writing less recognizable as AI-generated.

When to use: text flagged for pattern 50 vocabulary density or pattern 15 transition overuse. Unlike a simple delete pass, this prompt forces *substitution* — replacing each flagged phrase with a natural equivalent that preserves the logical relationship. Use the After: patterns in catalog entries #15, #16, and #50 as substitution banks.

## Reference

Pattern catalog adapted from Wikipedia's "Signs of AI writing" guide (maintained by WikiProject AI Cleanup), SearchAtlas's AI pattern analysis, Leap AI's perplexity/burstiness explainer, GPTZero's AI Vocabulary, and the ACL BEA-2025 evaluation of GPTZero's vocab list.
2026 Economist corpus study ("Ghost writer", 2026-07-30): 55,940 sentences / 1.2m words comparing ChatGPT, Claude, Gemini, Grok against Economist prose, CNN/NYT/WaPo, and novels 1950-2022. Source of the em-dash reversal, punctuation-poverty, and vocabulary-rotation findings (#11, #12, #46): https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing

Key sources:
- https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- https://searchatlas.com/blog/ai-patterns-in-writing
- https://www.tryleap.ai/learn/perplexity-vs-burstiness
- https://gptzero.me/ai-vocabulary
- https://aclanthology.org/2025.bea-1.71.pdf
- https://en.wikipedia.org/wiki/Artificial_intelligence_content_detection

Statistical signals (perplexity, burstiness, sentence-level probability, word-frequency ratios) per GPTZero's public methodology and detector-vendor explainers (Leap AI, Search Atlas, Originality.ai). False-positive and adversarial-evasion figures per Stanford HAI and the 2025 adversarial-evasion literature. Markup artifacts per Wikipedia's Signs of AI writing §Markup.
