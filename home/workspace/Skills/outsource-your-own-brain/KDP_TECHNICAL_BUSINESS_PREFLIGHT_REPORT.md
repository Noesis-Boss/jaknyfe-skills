# Amazon KDP Technical and Business Book Preflight Report

## Scope and confidence

Reviewed `publishing/books/DELowery/Outsource-Your-Own-Brain/Outsource-Your-Own-Brain.epub` directly. The EPUB contains 28 ZIP entries, 21 XHTML documents, 18 spine documents, a cover image, title page, copyright page, navigation document, and approximately 81,525 extracted words. The review checked EPUB structure, metadata, navigation, headings, visible draft markers, links as embedded, chapter text, and representative technical/business claims. External URLs were not opened or fact-checked, and no KDP account metadata was supplied. This report assesses publication-readiness risks; it does not predict Amazon approval.

## Executive decision

**Not ready.** The EPUB has publication-stopping placeholder material, an empty title page, inconsistent/unfinished-looking front matter, and visible draft/evidence artifacts in the interior. The file is materially more complete than the earlier source-bundle review, but it still needs a final production and source-verification pass.

## 1. KDP approval-risk assessment

### [Blocker] Placeholder publication data remains in the copyright page

- **Location:** `EPUB/text/ch002.xhtml`, Copyright
- **Excerpt:** `ISBN: 978-0-0000000-0-0 (placeholder , assign before publication)`
- **Why it matters:** A placeholder ISBN and placeholder publisher/production fields show that the interior is not final publication material.
- **Proposed revision:** Replace the ISBN, publisher, cover-design, and interior-design fields with final approved data, or remove fields that do not belong in the edition.
- **Confidence:** High

### [Blocker] Title page is empty while the EPUB title is `UNTITLED`

- **Location:** `EPUB/text/title_page.xhtml`; `EPUB/content.opf`; `EPUB/nav.xhtml`
- **Excerpt:** `<title>UNTITLED</title>` and `<section epub:type="titlepage" class="titlepage"> </section>`
- **Why it matters:** The EPUB has no usable title-page content, and the navigation document exposes `UNTITLED`. This is a direct publication-readiness defect and can produce an incomplete reader-facing book.
- **Proposed revision:** Add the final title, subtitle, author/publisher identity, and any required edition information to the title page; set the document and navigation titles to the final book title.
- **Confidence:** High

### [High] Interior contains explicit draft/process language

- **Location:** `EPUB/text/ch016.xhtml`, Chapter 14
- **Excerpt:** `This unpublished chapter draft was generated using the tool-free content creation model. Two earlier sections were removed at the author’s request; the numbering below reflects the final order.`
- **Why it matters:** The text labels the chapter as unpublished and exposes internal production history. It reads like working material, not final reader-facing prose.
- **Proposed revision:** Remove the process note and proof the chapter after the removed sections; retain only reader-facing content.
- **Confidence:** High

### [High] Copyright-page production placeholders remain beyond the ISBN

- **Location:** `EPUB/text/ch002.xhtml`
- **Excerpt:** `Publisher: Noesis Publishing (placeholder)`; `Cover design: (placeholder)`; `Interior design: (placeholder)`
- **Why it matters:** Multiple unresolved placeholders can create misleading or incomplete publication metadata.
- **Proposed revision:** Replace each field with verified final information or delete the field. Do not leave parenthetical production notes in the final interior.
- **Confidence:** High

### [High] AI-content disclosure and authorship status are not established by the EPUB

- **Location:** Entire EPUB; especially Chapter 14 process note and AI-related subject matter
- **Excerpt:** `generated using the tool-free content creation model`
- **Why it matters:** The file shows AI-related production language but does not establish the complete production history needed to determine the applicable KDP AI-content declaration. It also exposes a process statement that may not be intended for publication.
- **Proposed revision:** Confirm what AI generated, edited, or only assisted; make the applicable KDP declaration; remove or rewrite internal process language unless intentionally part of the book.
- **Confidence:** High; author process confirmation is required

### [High] Evidence section contains malformed or suspicious source links

- **Location:** `EPUB/text/ch017.xhtml`, Evidence & authority; Chapter 11 source list
- **Excerpt:** `https://www.jstor.org/stable/43699200)).`
- **Why it matters:** Several embedded URLs contain trailing `))` or punctuation as part of the visible link text. These are difficult to validate and may be broken or misleading when copied by readers.
- **Proposed revision:** Validate every URL, remove citation punctuation from the URL target/text, and replace inaccessible or weak sources with stable authoritative links.
- **Confidence:** High for formatting defect; external destination status not checked

### [High] Evidence and case-study claims require source verification

- **Location:** Chapters 3, 4, 6, 7, 9, 10, 12, 14, and 15
- **Excerpt:** `Weekly proposal drafting dropped from 28 hours to 9 hours (-68%).`
- **Why it matters:** Precise performance, productivity, market, and legal claims are presented as evidence or case studies. The EPUB includes URLs, but the sources and methodology were not verified in this review.
- **Proposed revision:** Verify each claim against its cited source, identify private/proprietary case studies as such, provide dates and sample/context, and label estimates as estimates.
- **Confidence:** Medium; claims are visible, source validity remains unchecked

### [Medium] Case studies may be read as factual endorsements

- **Location:** Chapters 3–15
- **Excerpt:** `A NoesisGroup operator built a custom GPT trained on twelve months of prior proposals.`
- **Why it matters:** Named organizations, people, performance numbers, and client outcomes can create permission, attribution, confidentiality, and credibility questions.
- **Proposed revision:** Confirm permission and factual basis; anonymize further or label examples as composite/illustrative where appropriate.
- **Confidence:** Medium

## 2. Content and technical/business readiness

### [High] Chapter and navigation structure includes internal evidence subsections in the reader TOC

- **Location:** `EPUB/nav.xhtml`, Chapters 1–15
- **Excerpt:** `Narrative illustrations`; `Evidence & authority`; `Peer-reviewed studies (5)`; `Compelling statistics`
- **Why it matters:** The navigation exposes production-framework headings and many evidence subheadings. This may be intentional, but it makes the book read like a compiled research package rather than a finalized trade nonfiction interior.
- **Proposed revision:** Decide whether evidence and narrative sections belong in the reader-facing structure. Simplify the TOC to the intended reader hierarchy and move source notes to endnotes or back matter if appropriate.
- **Confidence:** High

### [High] Chapter 4 heading contradicts its stated subject

- **Location:** `EPUB/text/ch006.xhtml`, Chapter 4 heading and `EPUB/nav.xhtml`
- **Excerpt:** `Chapter 4: the decision layer: where inputs become inputs`
- **Why it matters:** The chapter’s apparent concept is decision-making, but the heading says “inputs become inputs,” which looks like a copy or generation error and weakens navigation clarity.
- **Proposed revision:** Confirm and correct the heading, likely to the intended phrase describing inputs becoming decisions or outputs; update the matching navigation label and identifier.
- **Confidence:** High

### [High] Technical guidance is version-sensitive and provider-agnostic without operational boundaries

- **Location:** Chapters 1–15, especially Chapters 5, 6, 10, and 12
- **Excerpt:** `If any tool dies: paste the same files into the replacement.`
- **Why it matters:** AI providers differ in export, privacy, retention, file limits, model behavior, tool permissions, and enterprise controls. Readers could apply portability advice to confidential material without adequate safeguards.
- **Proposed revision:** State the assumptions, identify provider/version scope where relevant, and add a warning to verify retention, export, privacy, and confidential-data controls before migration.
- **Confidence:** High

### [High] Financial and business claims need assumptions, dates, and qualification

- **Location:** Chapters 7, 9, 10, and 13
- **Excerpt:** `Pure services ≈ 1x revenue`; `Asset-layer businesses command 2x-5x.`
- **Why it matters:** Valuation multiples and savings claims vary by sector, growth, margins, recurring revenue, market conditions, and dataset. Readers may interpret these as actionable financial guidance.
- **Proposed revision:** Cite the source and date, define the comparison set, show assumptions, and state that examples are illustrative rather than valuation or investment advice.
- **Confidence:** High

### [Medium] Some quantitative examples contain arithmetic or framing that needs proof

- **Location:** Chapters 2, 3, 4, 6, and 9
- **Excerpt:** `Do that four times a day and you’ve bought back two and a half hours.`
- **Why it matters:** The result depends on the assumed 35-minute saving, frequency, workdays, and whether the recovered time is actually available. Similar case-study figures appear throughout the book.
- **Proposed revision:** Show the calculation and assumptions, and describe the result as an illustrative scenario unless measured and documented.
- **Confidence:** High

### [Medium] Some source attributions are incomplete or visibly malformed

- **Location:** `EPUB/text/ch005.xhtml`, `EPUB/text/ch016.xhtml`, and `EPUB/text/ch017.xhtml`
- **Excerpt:** `See chapter text for source attributions.`
- **Why it matters:** A reader-facing source section that defers attribution to another location is less usable, while malformed URLs and inconsistent citation styles reduce reproducibility.
- **Proposed revision:** Consolidate complete citations in notes or references, use one citation style, and ensure each claim maps to a source.
- **Confidence:** High

### [Medium] Privacy, legal, and professional-use boundaries need stronger placement

- **Location:** Chapters 5, 10, 12, and 14
- **Excerpt:** `paste the same files into the replacement`
- **Why it matters:** The book discusses client proposals, confidential files, NDAs, legal examples, and AI tools. A reader could infer that copying client or regulated information into a replacement service is safe.
- **Proposed revision:** Add a prominent privacy/confidentiality warning before operational instructions and advise jurisdiction-specific legal, tax, and professional review where applicable.
- **Confidence:** High

### [Low] Core terminology and progression are generally coherent

- **Location:** Chapters 1–15 and supporting evidence sections
- **Excerpt:** `Capture, decide, and produce get externalized to a substrate`
- **Why it matters:** The central progression from capture to triage, delegation, measurement, boundaries, and ownership is understandable.
- **Proposed revision:** Retain the progression; perform a final terminology and heading consistency pass after removing production artifacts.
- **Confidence:** High

## 3. Line-edit findings

### [High] Visible spacing and punctuation defects remain in the EPUB text

- **Location:** Throughout, especially Chapters 3, 4, 5, 6, 13, 14, and 17
- **Excerpt:** `the proposal ,a voice memo, a prospect email`; `the moment your hours stop scaling with your client count, and your revenue starts scaling`
- **Why it matters:** Spaces before commas, missing spaces after commas, and awkward inserted spaces make the book look unproofed and can reduce reader confidence.
- **Proposed revision:** Run a controlled punctuation-spacing pass, then proof the rendered EPUB in an actual reader. Do not use an unrestricted global replacement without reviewing dialogue, citations, and em-dash conventions.
- **Confidence:** High

### [Medium] Draft-style fragments and generation artifacts remain

- **Location:** `EPUB/text/ch016.xhtml` and `EPUB/text/ch017.xhtml`
- **Excerpt:** `the moment your hours stop scaling with your client count` and `The next chapter is about that , the surprising thing`
- **Why it matters:** These passages contain malformed spacing and sentence construction that suggest unfinished editing.
- **Proposed revision:** Rewrite the affected sentences after comparing them with the intended chapter transition and proof all cross-chapter references.
- **Confidence:** High

### [Medium] Repeated slogan language may feel machine-like

- **Location:** Across Chapters 1–15
- **Excerpt:** `AI produces the first pass; the human produces the decision.`
- **Why it matters:** The principle is useful, but repeated near-verbatim formulations can make the interior feel templated.
- **Proposed revision:** Keep the canonical formulation in the introduction and conclusion; vary or shorten later repetitions.
- **Confidence:** High

### [Low] Capitalization is inconsistent in headings

- **Location:** All chapter XHTML headings and navigation
- **Excerpt:** `Chapter 15: the brain you outsource becomes the brain you keep`
- **Why it matters:** Sentence-case headings may be intentional, but the mixed treatment of chapter titles, evidence labels, and navigation entries should be standardized.
- **Proposed revision:** Select one heading convention and apply it consistently across XHTML, NCX, and nav.xhtml.
- **Confidence:** Medium

## 4. Audience and market fit

The book has a clear promise for AI-curious solopreneurs: delegate routine cognitive labor while retaining judgment, taste, and accountability. Its practical frameworks, examples, and 30-day build are strong market assets. Market readiness is reduced by the empty title page, exposed production notes, very large evidence sections in the main flow, unqualified quantitative claims, and unresolved privacy/version assumptions. No sales or approval guarantee is implied.

## 5. KDP deliverable and acceptance-readiness checklist

| Item | Status | Evidence/notes |
|---|---|---|
| Front matter | Needs review | Cover exists; title page XHTML is empty |
| Title page | Missing | `<section epub:type="titlepage" class="titlepage"> </section>` |
| Copyright page | Needs review | Present, but contains placeholders |
| Table of contents | Needs review | Nav exists, but exposes internal evidence hierarchy and `UNTITLED` |
| Disclaimers | Needs review | Privacy, legal/tax, financial, and professional-use boundaries need review |
| References/bibliography | Needs review | Evidence URLs exist, but require validation and cleanup |
| Notes/citations | Needs review | Footnotes and links are present; citation quality is inconsistent |
| Figures/tables/code formatting | Needs review | No figures/tables were separately validated in a reader |
| Appendices/worksheets | Needs review | No distinct appendix decision was supplied |
| Back matter | Needs review | About-the-author section exists; final resources/CTA/acknowledgments need review |
| Links | Needs review | Embedded URLs were inspected syntactically, not opened |
| Blurb | Missing | No KDP description supplied in the EPUB |
| Author name | Needs review | Author identity needs confirmation against KDP metadata |
| Series data | Missing | No series status supplied |
| Edition/version date | Needs review | EPUB metadata date is `2026-08-05`; edition information is not clear |
| Credentials/bio | Needs review | About-the-author section exists; credentials should be confirmed |
| AI-content disclosure | Needs review | Production history and applicable declaration require author confirmation |

## Final KDP-fix action list

1. Replace the empty title page, `UNTITLED` metadata, and all copyright-page placeholders.
2. Remove the unpublished/process note and decide whether evidence/narrative subsections belong in the reader-facing interior and TOC.
3. Proof the entire EPUB for punctuation spacing, malformed sentences, headings, cross-references, and navigation labels.
4. Validate every source URL and substantiate quantitative, legal, technical, valuation, and case-study claims with dated citations and assumptions.
5. Confirm rights, author identity, privacy/disclaimer language, final KDP metadata, and AI-content disclosure before final rendering and submission.

## Author confirmations needed

- Is D.E. Lowery the final KDP author/pen name and copyright claimant?
- What is the final ISBN, publisher/imprint, edition, subtitle, series status, and KDP description?
- Which case studies are real, composite, private, or illustrative, and are permissions documented?
- Which claims and quotations have been source-checked, and what version/date assumptions apply to AI tools?
- Was AI used to generate, edit, or only assist the book, and what KDP disclosure applies?

## Post-fix verification — 2026-08-21

Source and build fixes were applied to `publishing/books/DELowery/Outsource-Your-Own-Brain/manuscript.md` and rebuilt with `scripts/build_book.sh`.

- **Fixed:** Empty title page. EPUB now contains the final title, subtitle, author, and year.
- **Fixed:** `UNTITLED` title metadata.
- **Fixed:** Placeholder ISBN, publisher marker, cover-design marker, and interior-design marker removed from the copyright page. The ISBN remains an author/KDP metadata decision and is not invented here.
- **Fixed:** Chapter 4 heading corrected to `where inputs become decisions`.
- **Fixed:** Internal unpublished/process note removed.
- **Fixed:** Stray `Saved to Documents/research/...` artifact removed.
- **Fixed:** Three deferred source-attribution bullets changed to reader-facing wording.
- **Fixed:** Broad punctuation-spacing defects and malformed trailing citation punctuation were mechanically corrected, followed by rebuild.
- **Verified:** EPUB cover declaration is present; EPUB body begins with the Copyright section rather than a duplicate title heading; PDF rebuilt successfully to 212 pages.

Remaining before publication: validate external sources, confirm rights and AI disclosure, finalize ISBN/edition/KDP metadata, decide whether the evidence hierarchy should remain in the reader-facing TOC, and proof the rendered EPUB/PDF visually in the target reading environments.
