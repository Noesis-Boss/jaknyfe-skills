# Bookmaker Prompts

The five canonical prompts. Use verbatim — the wording is tuned.
Replace `[brackets]` with your specifics.

---

## PROMPT 1: High-Impact Book Idea Architect

```
Assume the role of a seasoned publishing strategist. Develop five commercially viable book concepts in [your niche].

For each:

• Powerful title + persuasive subtitle
• Target reader demographics
• Differentiated positioning statement
• Market size estimate
• Why readers would pay $20-$30
• Relevant trends aligning with demand

Validate high-potential ideas before committing months to writing.
```

**Required bracket:** `[your niche]`

**Output:** Five concepts with title, subtitle, demographics, positioning,
market size, willingness-to-pay rationale, and trend alignment.
Use to pick the winner before writing.

---

## PROMPT 2: Strategic Book Blueprint Developer

```
Construct a chapter-by-chapter framework for [genre] book titled [your title] for [target audience]. Include 10-15 chapters.

Per chapter:

• Benefit-driven title
• 3-5 essential concepts
• Word count (1,500-3,000)
• Reader transformation
• Transition to next chapter
• Hook for Chapter One
• Satisfying final chapter close

Delivers complete structural roadmap before drafting.
```

**Required brackets:** `[genre]`, `[your title]`, `[target audience]`

**Output:** 10-15 chapter outline with per-chapter title, concepts, word
count, transformation, transition, plus a Chapter One hook and a final
chapter close. The structural backbone of the manuscript.

---

## PROMPT 3: Full-Length Chapter Draft Generator

```
Draft complete manuscript for Chapter [number]: [title] focused on [topic].

Specs:

• Readership: [audience]
• Tone: [conversational/authoritative]
• Length: [1,500-3,000 words]

Include:

• Compelling opening
• 3-4 sections with subheadings
• Specific examples/case studies
• Practical, actionable insights
• Bridge to next chapter

Use strong, active language. Avoid generic phrasing.
```

**Required brackets:** `[number]`, `[title]`, `[topic]`, `[audience]`,
`[conversational/authoritative]`, `[1,500-3,000 words]`

**Output:** A complete chapter draft matching the blueprint in Stage 2.
Run once per chapter.

---

## PROMPT 4: Narrative & Illustration Development Tool

```
Create eight original narrative pieces demonstrating [core concept] for [genre] book.

Each story (150-250 words):

• Vivid details, authentic dialogue
• Clear narrative arc (beginning, conflict, resolution)
• Resonates with [target audience]
• Meaningful takeaway without being instructional

Goal: Craft emotionally engaging illustrations deepening reader connection.
```

**Required brackets:** `[core concept]`, `[genre]`, `[target audience]`

**Output:** Eight short (150-250 word) stories/illustrations that
demonstrate the concept through narrative rather than lecture. Drop
into chapters as openings, sidebars, or section anchors.

---

## PROMPT 5: Evidence & Authority Integration Framework

```
Developing Chapter [X] on [subject]. Compile authoritative research:

• 3-5 peer-reviewed studies with accessible summaries
• 2-3 compelling statistics from reputable sources
• 1-2 expert quotations from recognized authorities
• 1 relevant case study demonstrating concept
• Synthesis paragraph supporting central argument

Include proper citations. Note how each strengthens reader trust.
```

**Required brackets:** `[X]`, `[subject]`

**Output:** A research bundle — studies, stats, quotes, case study,
synthesis — to weave into a chapter for credibility. Run per chapter
where evidence matters.

---

## Chaining

Stages are designed to run in order:

1. **Ideate** — pick a niche, get 5 concepts, choose one.
2. **Blueprint** — outline the chosen title.
3. **Draft** — write each chapter following the blueprint.
4. **Illustrate** — generate narrative pieces to embed.
5. **Evidence** — back each chapter with research.

The `bookmaker.ts pipeline` command chains 1→2→3→4→5 with one set of
flags. For finer control, run `bookmaker.ts stage N` for each stage.
