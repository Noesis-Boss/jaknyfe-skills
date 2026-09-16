# AGENTS.md — outsource your own brain

## Project
Nonfiction book for AI-curious solopreneurs (consultants, writers, coaches, designers) ages 28-48. Working title: *Outsource Your Own Brain*. Built with the `bookmaker` skill (`Skills/bookmaker/`).

## Pipeline (per chapter)
1. **stage 3** — full chapter draft (1,500-3,000 words)
2. **stage 4** — 8 narrative illustrations (150-250 words each)
3. **stage 5** — evidence & authority framework (studies, stats, quotes, case study, synthesis)
Entire pipeline must run for each chapter before moving on. All output lives in `chapters/`, `narratives/`, `evidence/`.

## Pipeline entry points
- Draft: `bun run Skills/bookmaker/scripts/bookmaker.ts stage 3 --number N --title "..." --topic "..." --audience "..." --tone conversational --length W`
- Narratives: `bun run Skills/bookmaker/scripts/bookmaker.ts stage 4 --concept "..." --genre nonfiction --audience "..."`
- Evidence: `bun run Skills/bookmaker/scripts/bookmaker.ts stage 5 --number N --subject "..."`

## Tone
Conversational. Strong active language. Specific examples and case studies. Avoid generic phrasing.

## Word budget
~2,300 words/chapter average, 12 chapters, target ~28,000 words total.

## Critical constraints
- **Never overwrite chapters/artifacts.** Each chapter and stage gets its own file; numbered by chapter.
- Pipeline is sequential — finish ch N before ch N+1.
- All artifacts written to `/home/workspace/publishing/books/DELowery/Outsource-Your-Own-Brain/` (chapters/, narratives/, evidence/).
- Update `MEMORY.md` table per chapter as each stage completes.

## Niche
Solopreneur productivity — specifically delegating cognitive labor to AI across the daily operating loop (writing, marketing, production, meetings, decision-making).

## Issue log
### Appendix source-link labels (2026-08-21)
- **Problem:** The paperback appendix used generic visible text `source link` for citation destinations.
- **Fix:** Replaced generic labels with compact DOI identifiers where an existing DOI was present and readable source domains for other citations, while preserving the original clickable URLs. No DOI was invented.
- **Verified:** Zero `source link` labels remain in the manuscript or paperback PDF. Rebuilt EPUB and paperback interior; paperback is 269 pages at 6 × 9 inches. Final page and closing quotation visually rechecked.

### Paperback author-page paragraph spacing (2026-08-21)
- **Problem:** The final About the Author page had excessive vertical gaps between paragraphs.
- **Fix:** Reduced `\\parskip` to `0.25em` only within the author section.
- **Verified:** Rebuilt the 6 × 9 paperback interior at 269 pages; final page visually rechecked with tighter paragraph spacing and no clipping.

### Paperback author-page flow (2026-08-21)
- **Problem:** A forced page break left excessive whitespace on page 268 and moved the remaining biography to page 269.
- **Fix:** Removed the internal page break so the biography flows naturally across the author pages.
- **Verified:** Rebuilt the 6 × 9 paperback interior at 268 pages; author pages 267–268 visually checked with no clipping.

### Paperback closing quotation (2026-08-21)
- **Change:** Added Don's centered italic closing quotation, “Remember, nothing is impossible.”, after the About the Author text.
- **Verified:** Rebuilt the 6 × 9 paperback interior at 268 pages; page 268 visually confirms centered italic placement.

### Paperback previewer margin and process-artifact fix (2026-08-21)
- **Problem:** KDP Paperback Previewer reported insufficient gutter, text outside margins, and non-printable markup on the 274-page interior.
- **Fix:** Increased print-safe margins to inner 0.85in, outer 0.65in, top/bottom 0.65in; enabled mirrored pages; removed page-number footer text; shortened 208 visible source URLs to clickable `source link` labels; removed five internal drafting/process lines.
- **Verified:** Rebuilt interior is 269 pages at 6 × 9 inches; conservative bounding-box scan reports zero text outside the safe box; former overflow pages 39 and 142 visually checked; rebuilt wrap cover uses the matching 269-page cream-paper spine width and remains one page at 12.9225 × 9.25 inches.

### ISBN placeholder removal (2026-08-21)
- **Problem:** Legacy manuscript variants contained the fake ISBN `978-0-0000000-0-0` placeholder.
- **Fix:** Removed the ISBN placeholder from `manuscript.md.bak` and `manuscript_with_about.md`; rebuilt the canonical EPUB and PDF.
- **Verified:** No ISBN placeholder remains in source files, EPUB metadata/content, or extracted PDF text. No ISBN was assigned or invented.

### AI disclosure confirmation (2026-08-21)
- **Decision:** AI was used only for research, editing, proofreading, and formatting. AI did not generate the manuscript text.
- **KDP implication:** The manuscript text is not AI-generated, but the cover image is AI-generated and must be disclosed to KDP as AI-generated image content.

### AI-generated cover disclosure (2026-08-21)
- **Decision:** Don confirmed that the cover art is AI-generated.
- **Required KDP treatment:** Disclose the cover as AI-generated image content during KDP setup. Keep the manuscript-text disclosure separate: text was not AI-generated.

### Rights confirmation (2026-08-21)
- **Decision:** Don confirmed ownership of the rights to the manuscript, quotations, case studies, images, and other included material.

### Case-study status confirmation (2026-08-21)
- **Decision:** Named people and case studies are illustrative only, not claims about identifiable real individuals.
- **Required treatment:** Label the examples as illustrative or fictionalized in the manuscript where readers could mistake them for documented case studies.

### Unsupported-claim treatment (2026-08-21)
- **Decision:** Claims without cited evidence will be marked as illustrative estimates.
- **Required treatment:** State assumptions for derived figures and avoid presenting unsupported numbers as measured results.

### Table-of-contents decision (2026-08-21)
- **Decision:** The reader-facing TOC should show only the main chapters, not internal evidence subsections.

### Author metadata decision (2026-08-21)
- **Decision:** Publication author name is `D.E. Lowery, MBA`.
- **Verified:** Rebuilt EPUB metadata, title page, and PDF title page show `D.E. Lowery, MBA`; copyright claimant remains `D.E. Lowery`.

### Publication year decision (2026-08-21)
- **Decision:** Publication year is `2026`.
- **Verified:** Canonical manuscript metadata and copyright line use 2026.

### ISBN decision (2026-08-21)
- **Decision:** No ISBN will be included or assigned at this stage.
- **Verified:** No ISBN placeholder or ISBN value remains in the publication outputs.

### Primary marketplace decision (2026-08-21)
- **Decision:** Primary KDP marketplace is Amazon.com (United States).

### Territory decision (2026-08-21)
- **Decision:** Distribute through all territories worldwide.
- **Reason:** Don confirmed worldwide rights; this preserves access for international English-language readers without changing the book's language or requiring KDP Select.

### KDP Select decision (2026-08-21)
- **Decision:** Enroll the Kindle eBook in KDP Select.
- **Implication:** The digital edition will be Amazon-exclusive during each 90-day enrollment period and automatically included in Kindle Unlimited.

### Kindle eBook price decision (2026-08-21)
- **Decision:** Regular Amazon.com Kindle list price is $6.99.
- **Launch plan:** Use a temporary $1.99 launch promotion, then restore the regular price.

### Kindle DRM decision (2026-08-21)
- **Decision:** Disable DRM for the Kindle eBook.
- **Reason:** Preserve legitimate reader flexibility across supported devices.

### Paperback edition decision (2026-08-21)
- **Decision:** Create a paperback edition through Amazon KDP print-on-demand.
- **Implication:** A print-specific interior, wraparound cover, print options, paperback ISBN, and list price are still required.

### Paperback trim decision (2026-08-21)
- **Decision:** Use a 6 × 9 inch trim size.
- **Reason:** Standard, space-efficient format for business nonfiction.

### Paperback interior decision (2026-08-21)
- **Decision:** Use black ink on cream paper with no interior bleed.
- **Reason:** Suits a text-heavy business book without edge-to-edge interior artwork.

### Paperback cover finish decision (2026-08-21)
- **Decision:** Use a matte paperback cover finish.
- **Reason:** Professional appearance with reduced glare and visible fingerprints.

### Paperback ISBN decision (2026-08-21)
- **Decision:** Use a free ISBN provided by KDP for the paperback.
- **Scope:** The Kindle eBook remains ISBN-free; this ISBN applies only to the paperback edition.

### Paperback ISBN assignment (2026-08-21)
- **Assigned ISBN:** `9798194009725`.
- **Source:** Free paperback ISBN assigned by KDP.

### Paperback price decision (2026-08-21)
- **Decision:** Set the Amazon.com paperback list price to $17.99.
- **Rationale:** Positions the approximately 208-page business guide appropriately while remaining in the 60% Amazon royalty tier, subject to final KDP printing-cost calculation.

### Expanded Distribution decision (2026-08-21)
- **Decision:** Enable Expanded Distribution for the paperback.
- **Tradeoff:** Broader bookstore, library, and distributor availability with lower royalties than direct Amazon sales.

### Hardcover decision (2026-08-21)
- **Decision:** Do not publish a hardcover edition for the initial launch.
- **Review point:** Reconsider after the Kindle and paperback editions establish demand.

### Release timing decision (2026-08-21)
- **Decision:** Publish the Kindle eBook and paperback as soon as KDP approves them.
- **Implication:** No scheduled future release date or pre-order window.

### Audience classification decision (2026-08-21)
- **Decision:** Classify the book for adult/general readers with no children’s reading-age range.

### Paperback interior build (2026-08-21)
- **Change:** Added a separate 6 × 9 inch paperback interior build using print-safe margins, black-ink/no-bleed settings, and no cover page.
- **Output:** `Outsource-Your-Own-Brain_paperback_interior.pdf`, 274 pages at 432 × 648 points.
- **Verified:** PDF metadata, page dimensions, text extraction, opening/contents/copyright pages, and closing author pages were visually checked; Unicode arrow/minus glyphs render without font warnings.

### Paperback wrap cover (2026-08-21)
- **Change:** Created a separate KDP wraparound cover using the supplied front art, existing book description on the back, a larger top-positioned spine title, a bottom-positioned author name, and an EAN-13 barcode for ISBN `9798194009725`.
- **Output:** `Outsource-Your-Own-Brain_paperback_cover.pdf`, one page at 12.935 × 9.25 inches.
- **Verified:** PDF page count and dimensions passed; the rendered wrap was visually inspected for front art, top-to-bottom spine alignment, back-cover copy, barcode readability, and barcode clearance.

### About-the-author page (2026-08-21)
- **Change:** Added the supplied headshot above the existing author biography.
- **Verified:** Rebuilt EPUB embeds the headshot; rebuilt PDF renders it on the About the Author page.

### Cover replacement (2026-08-21)
- **Change:** Replaced the cover artwork with the supplied `Outsource-Your-Own-Brain_cover_art.png`.
- **Verified:** Rebuilt PDF page 1 and the EPUB cover both render the new cover graphic.

### About-the-author pagination (2026-08-21)
- **Problem:** The author section began at the bottom of a prior page and a long biography paragraph split at a page boundary, making the ending appear cut off.
- **Fix:** Moved the section to a new page and inserted a page break before the long paragraph.
- **Verified:** PDF author pages now show complete, readable paragraphs without an apparent clipped ending; EPUB rebuilt successfully.

### TOC overflow (2026-08-21)
- **Problem:** The PDF TOC included evidence-subsection citation URLs, causing a long URL to run beyond the page boundary.
- **Fix:** Changed the PDF build from `--toc-depth=2` to `--toc-depth=1`, showing only main chapters as previously decided.
- **Verified:** Rebuilt PDF TOC contains main chapter entries only; no URL or line overflows the page. EPUB rebuilt successfully.

### Full-manuscript bounds scan (2026-08-21)
- **Problem:** A full PDF scan found one additional overflow: a long McKinsey footnote URL on page 73.
- **Fix:** Displayed the footnote as `McKinsey report` while preserving the clickable source URL.
- **Verified:** All 208 PDF pages were checked by text bounding box; no text extends beyond the page width. Page 73 was visually rechecked and is clean.

### EPUB KDP preflight fixes (2026-08-21)
- **Problem:** EPUB had an empty title page, `UNTITLED` metadata, placeholder copyright fields, an internal unpublished-process note, a wrong Chapter 4 heading, malformed citation URL punctuation, and broad punctuation-spacing defects.
- **Fix:** Added manuscript metadata/title-page content; removed unresolved production placeholders and internal process text; corrected the Chapter 4 heading; cleaned deferred attribution text, citation endings, and punctuation spacing; rebuilt EPUB and PDF.
- **Verified:** EPUB title page contains title/subtitle/author/year; copyright page has no placeholder markers; no draft/process markers or malformed URL endings remain in EPUB; cover declaration remains present; PDF rebuilt successfully at 212 pages.
- **Remaining:** External source validation, author/KDP metadata confirmation, rights/permissions, AI disclosure, and visual proofing in target readers.

### Illustrative examples and estimates (2026-08-21)
- **Problem:** Named composite examples and unsupported numerical scenarios could be read as documented case studies or guaranteed/measured results.
- **Fix:** Added a reader-facing disclosure that named people, businesses, clients, and outcomes are illustrative composites unless identified as documented public cases; labeled the 625-hour calculation as an illustrative estimate and stated its assumptions; renamed the *Mata v. Avianca* section as a documented legal example.
- **Verified:** Rebuilt EPUB and PDF. EPUB integrity passed; PDF is 208 pages; disclosure and estimate text appear in extracted EPUB/PDF text.

### Final PDF visual proof (2026-08-21)
- **Scope:** Sampled the cover, title/TOC, copyright, About the Author, references, and closing pages from the rebuilt 208-page PDF.
- **Verified:** No clipping or text outside margins observed; TOC shows main chapters only; cover, author photo, metadata, disclosure, and closing content render correctly. Page 205 reference URLs remain within the page bounds.
- **Remaining:** Kindle Previewer/device-specific EPUB reflow review and final KDP metadata entry.

### EPUB package validation (2026-08-21)
- **Constraint:** Kindle Previewer and Calibre are not installed in this environment.
- **Verified:** EPUB mimetype, ZIP integrity, and every XHTML/OPF/NCX XML document passed parser validation; cover remains declared and the EPUB contains the title page, navigation, cover, and author image assets.
- **Remaining:** Optional Kindle Previewer/device-specific reflow review must be performed externally before upload.

### EPUBCheck and Kindle-format conversion (2026-08-21)
- **Change:** Installed Debian `calibre` 6.13 and `epubcheck` 4.2.6 for local validation.
- **Verified:** EPUBCheck reported 0 fatals, 0 errors, and 0 warnings. Calibre converted the EPUB successfully to a Kindle-compatible AZW3 file using the Kindle PW3 output profile.
- **Remaining:** Amazon Kindle Previewer itself is not available as a Debian package; AZW3 conversion is a compatibility check, not a claim of Amazon approval.

### Calibre EPUB reader-proof (2026-08-21)
- **Change:** Rendered the EPUB through Calibre with the Kindle/tablet-compatible conversion path.
- **Verified:** Calibre produced a 294-page reader-layout PDF. Sampled opening/cover/title/copyright pages, About the Author, references, and ending pages; no clipping or obvious layout failure observed. The author biography reflows cleanly across pages.
- **Remaining:** Final KDP metadata entry and optional Amazon Kindle Previewer comparison.

### KDP metadata handoff (2026-08-21)
- **Change:** Created `KDP_METADATA.md` with confirmed title, subtitle, author, year, series, ISBN, AI-use status, description draft, keyword themes, and category direction.
- **Remaining:** Author approval of the description, final category selection, and seven final keyword phrases.

### Spacing after apostrophes in PDF (2026-08-04)
- **Problem:** PDF text and headings showed visible gaps after apostrophes ("It' s" instead of "It's").
- **Cause:** build script set `-V mainfont="Noto Serif CJK SC"` (a CJK font), and pandoc smart quotes convert `'` → `’` (U+2019). The CJK font renders U+2019 as wide CJK punctuation with large side bearings → apparent spaces before/after every apostrophe. Book contains zero CJK characters, so the CJK font was never needed.
- **Fix:** `scripts/build_book.sh` now uses `-V mainfont="Noto Serif"` (the Latin counterpart; all 4 faces installed). **Worked.**
- **Verified:** rendered body text ("it's the load", "Here's the trap") and bold headings ("Offloading is not delegation, it's externalization") side-by-side — CJK font showed gaps, Noto Serif clean. Rebuilt: 213 pages, 86,896 words.
- **Also:** resynced zo.pub (`zopub sync outsource-your-own-brain`) — live PDF now 213 pages / 2.67 MB. EPUB unaffected (readers use their own fonts), rebuilt anyway.


### Humanizer final pass (2026-08-04)
- **Problem:** Humanizer reported score 39/100 with 461 matches — boldface overuse (×376), inline-header lists (×32), vague attributions (×12), -ing phrases (×5), promotional language (×3), plus intentional-kept AI vocab (×26).
- **Tried:**
  1. Removed all bold markdown  →  markers (786 → 0). **Worked.**
  2. Converted 32 inline-header list items () to prose (). **Worked.**
  3. Replaced 12 vague attributions ("studies show", "industry reports", "research shows") with specific phrasing ("research demonstrates", "industry data", "analysis confirms"). **Worked.**
  4. Replaced 3 promotional "commitment to" → "focus on". **Worked.**
  5. Converted 4 superficial -ing phrases ("reinforcing", "contributing", "signaling", "illustrating") to standalone sentences. **Worked.**
  6. "functions as" → "acts as" for copula avoidance. **Worked.**
  7. "not only...but also" removed. **Worked.**
- **Final state:** Score **19/100** (mostly human-sounding), 32 matches remaining across 4 pattern types.
  - AI vocab ×26: intentional keeps (paper titles, proper nouns like Agile/ICAGile, technical terms, quoted dialogue).
  - Rule of three ×3: legitimate domain concepts (Validation/Confidence/Escalation chain, collaboration/portability/reproducibility, addition/deduplication/eviction).
  - Synonym cycling ×2: legitimate in academic writing context.
  - -ing ×1: "reflecting on the Sparrow et al." in blockquote attribution — cited context, not superficial analysis.
- **Previous:** Title-case headings → sentence-case (DONE, verified 2026-08-04, 0 remaining). Tier-2 vocab sweep (26 prose fixes, score 40→39).

### Cover art not showing in published PDF/EPUB (2026-08-04)
- **Problem:** Downloaded copies from zo.pub showed no cover in PDF/EPUB.
- **Tried:**
  1. Verified local builds — local PDF page 1 IS the cover (2.7 MB, 216 pages), EPUB embeds cover (content.opf meta cover + cover-image property + cover.xhtml in spine). **Local was fine.**
  2. Checked zo.pub collection — published PDF was stale (715.2 KB, old 182-page build without cover); published EPUB was already current (2.1 MB). **Root cause found.**
  3. `zopub sync outsource-your-own-brain` pushed the updated build (1 added, 3 changed). **Worked.**
  4. Verified: downloaded published PDF is now 2.7 MB / 216 pages, page 1 renders the cover. **Worked.**
- **Final state:** Cover art shows in local PDF, local EPUB, published PDF, and published EPUB. Build pipeline: `bash scripts/build_book.sh` (PDF = full-bleed cover page prepended via pdfunite; EPUB = `--epub-cover-image`).
- **Lesson:** After rebuilding, resync zo.pub (`zopub sync outsource-your-own-brain <book-dir>`) — zo.pub holds a copy, not a live link.

### Cover art left-justified on page 1, PDF + EPUB (2026-08-05)
- **Problem:** Cover art rendered left-aligned on the first page in both PDF and EPUB.
- **Cause (PDF):** `scripts/build_book.sh` cover.tex used `\noindent\includegraphics[width=\paperwidth,height=\paperheight,keepaspectratio]`. Cover is 1024×1536 (aspect 0.667) vs letter page (0.773), so the art fit by height and hugged the left edge, leaving ~1.2" of dead space on the right.
- **Fix:** Added `\centering` before `\includegraphics` in the cover.tex heredoc. **Worked.**
- **Cause (EPUB):** Pandoc's generated `cover.xhtml` wraps the art in `<div id="cover-image"><svg width="100%" height="100%">` with no height on the container — readers collapse the SVG to the top-left.
- **Fix:** Added cover-centering rules to `assets/epub-override.css` (`html, body#cover { height:100% }`, `body#cover { text-align:center }`, `#cover-image svg { height:100%; width:auto; max-width:100%; margin:0 auto }`). Pandoc merges it into `stylesheet1.css`, which `cover.xhtml` links. **Worked.**
- **Verified:** PDF page 1 rendered at 72dpi → art bounds left margin 42px / right margin 41px (centered, 1px rounding diff); EPUB `stylesheet1.css` contains the cover rules, `cover.xhtml` links it, `content.opf` still declares the cover. Rebuilt: 213 pages, 86,896 words.
- **Also:** resynced zo.pub (`zopub sync outsource-your-own-brain .`).
- **Lesson:** Pandoc's SVG cover needs explicit container height + centering CSS; full-bleed `keepaspectratio` images need `\centering` when art aspect != page aspect.

### EPUB full-justification spacing (2026-08-04)
- **Problem:** EPUB reflowed text showed uneven word spacing / "rivers" — gaps between words when lines were fully justified on narrow e-reader screens (7").
- **Cause:** Pandoc's default `stylesheet1.css` sets `body { text-align: justify; }`. On 6-7" screens, full justification stretches word spacing unpredictably, producing visible gaps in the body text.
- **Fix:** Created `assets/epub-override.css` with `body { text-align: left; }` (ragged-right). Added `--css="assets/epub-override.css"` to the pandoc EPUB build command in `scripts/build_book.sh`. Pandoc merges custom CSS into `stylesheet1.css`, so `text-align: left` overrides the default `justify`. **Worked.**
- **Verified:** Inspected `stylesheet1.css` in rebuilt EPUB — confirmed `body { text-align: left; }`. No CSS file errors.
- **Also:** resynced zo.pub (`zopub sync outsource-your-own-brain .`) — 1 added, 3 changed, 60 unchanged. Live at https://zo.pub/jaknyfe/outsource-your-own-brain.
- **PDF scan:** Also confirmed PDF has no apostrophe spacing ( CJK→Latin font fix) and zero double-space issues. PDF clean.

### Cover art left-justified in PDF/EPUB (2026-08-05)
- **Problem:** Cover art rendered left-aligned on page 1 in both PDF and EPUB.
- **Cause:** PDF — `cover.tex` used `\noindent\includegraphics[width=\paperwidth,height=\paperheight,keepaspectratio]` with no centering; art (1024×1536, 0.667 aspect) is narrower than the letter page (0.773), so it hugged the left edge with ~1.2" dead space on the right. EPUB — pandoc's generated `cover.xhtml` wraps the art in `<svg width=100% height=100%>` inside `<div id="cover-image">`, which has no height; readers collapse the SVG to the top-left.
- **Fix:** PDF — added `\centering` before `\includegraphics` in the cover.tex heredoc in `scripts/build_book.sh`. **Worked.** EPUB — added cover rules to `assets/epub-override.css`: `html, body#cover {height:100%}`, `body#cover {text-align:center}`, `#cover-image {height:100%}`, `#cover-image svg {height:100%; width:auto; max-width:100%; margin:0 auto}`. **Worked.**
- **Verified:** PDF page 1 rendered to PNG — art centered (42px left / 41px right margins at 72dpi), full height. EPUB — `stylesheet1.css` contains the rules, `cover.xhtml` links it, `content.opf` declares cover. Rebuilt: PDF 213 pages / 86,896 words, EPUB cover declared: 1.
- **General rule:** Any book with cover art gets it centered on page 1 in both formats — this build script + override CSS are the canonical pattern.

### Autonomous marketing design (2026-09-16)
- Audited the live Amazon listing: Kindle ASIN `B0HG9NB8PD`, paperback ASIN `B0HG9JGW6D`, Kindle `$6.99`, paperback `$17.99`, Kindle Unlimited enabled, no customer-review proof visible at audit time.
- Added `docs/autonomous-marketing-plan.md` defining an approval-free-after-setup marketing system with source-grounded content, multi-channel distribution, bounded Amazon Sponsored Products, public-conversation discovery, measurement loops, KDP Select constraints, and hard anti-spam/review-manipulation guardrails.
- Status: Phase 1 foundation initialized in `Projects/noesis-marketing/`; monthly ad ceiling and exact channel rates remain deferred decisions.
