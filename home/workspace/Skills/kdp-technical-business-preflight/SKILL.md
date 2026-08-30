---
name: kdp-technical-business-preflight
description: Conservative Amazon KDP approval-risk preflight for technical, professional, and business books. Use whenever a user asks to review, proof, audit, preflight, or assess a nonfiction book before publication. Prioritize issues that could hinder KDP acceptance or publication readiness, then assess factual and technical integrity, structure, line editing, audience fit, deliverables, rights, and AI-content disclosure. Produce evidence-based fixes; never promise Amazon approval.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# KDP Technical and Business Preflight

Review the supplied technical, professional, or business manuscript and any accompanying front matter, back matter, references, figures, code, worksheets, links, blurb, metadata, or publication notes with potential KDP acceptance and publication readiness as the primary decision lens. Use editorial, technical, and business analysis to identify and fix risks that could interfere with that goal. This is not legal advice, a plagiarism certification, a technical audit of every external system, investment or professional advice, or an Amazon approval prediction.

## Operating rules

1. Read the complete supplied manuscript and supporting materials when feasible. If input is truncated, missing, image-only, or incomplete, state exactly what was not reviewed and reduce confidence.
2. Build a review ledger covering chapter/section, claims, definitions, terminology, examples, procedures, code or formulas, citations, links, version/date assumptions, audience, promised outcomes, and unresolved threads.
3. Check for plagiarism-like passages, duplicate chapters, unfinished sections, placeholders, broken links, unsupported quotations, missing attribution, copyright/trademark concerns, and AI-disclosure questions. Treat similarity as a review risk, never a definitive legal conclusion.
4. For technical content, check internal consistency, reproducibility, code syntax by inspection where possible, deprecated or version-sensitive instructions, unsafe commands, missing prerequisites, incorrect formulas, undefined variables, and examples that contradict the stated method. Do not claim to have executed code or verified an external service unless that was actually done.
5. For business content, check unsupported certainty, stale market or financial claims, arithmetic, assumptions, projections, legal/tax/regulatory claims, risk disclosures, conflicts of interest, and whether recommendations are clearly framed as context-dependent. Do not present editorial findings as professional advice.
6. Distinguish verified findings from author confirmations. For AI disclosure, identify what the materials show and what requires confirmation about the author's actual process and current KDP requirements.
7. Prefer minimally invasive revisions. Quote the smallest excerpt that proves the issue and propose a targeted correction, clarification, citation, warning, or replacement.
8. Classify every finding as exactly one of: `Blocker`, `High`, `Medium`, or `Low`. Use `Blocker` only for a publication-stopping defect or unresolved legal, safety, rights, or compliance risk. If a category has no findings, say `None found in the supplied materials`.

## Required report

Use this structure:

# Amazon KDP Technical and Business Book Preflight Report

## Scope and confidence

State the files and materials reviewed, whether the manuscript was complete, what was not checked, and important limitations. State that the report does not predict Amazon approval.

## Executive decision

Give one of: `Not ready`, `Conditionally ready after fixes`, or `Editorially ready for final production checks`. Summarize the top three risks and the reason for the decision.

## 1. KDP approval-risk assessment

Lead with the issues most likely to hinder KDP acceptance or publication readiness: plagiarism-like passages, unfinished sections, duplicate chapters, broken or suspicious links, placeholder text, unsupported quotations, attribution, copyright/trademark or permissions concerns, unsafe instructions, misleading metadata, legal/regulatory claims, and AI-disclosure questions. Clearly separate confirmed risks from items requiring author confirmation.

## 2. Content and technical/business readiness

Check structure and learning progression; definitions and terminology; factual and internal consistency; claims and evidence; citations and source quality; code, formulas, tables, examples, and reproducibility where applicable; version/date sensitivity; arithmetic and assumptions; risk/disclaimer language; audience fit; promised outcomes; and unresolved sections or recommendations.

## 3. Line-edit findings

Check repeated wording, grammar, punctuation, unclear antecedents, jargon, undefined acronyms, passive construction, excessive adverbs, filter words, sentence fragments, awkward transitions, inconsistent capitalization, inconsistent terminology, and unnatural or machine-like prose. Report representative patterns instead of flooding the report with trivial edits.

## 4. Audience and market fit

Assess the opening problem statement, reader promise, positioning, authority and credibility signals, practical usefulness, progression from problem to solution, examples and case studies, accessibility to the stated audience, emotional or intellectual payoff, actionability, conclusion, and any call to action. Frame this as editorial and market-readiness judgment, not a sales guarantee.

## 5. KDP deliverable and acceptance-readiness checklist

Use a status table with `Pass`, `Needs review`, or `Missing` for front matter, title page, copyright page, table of contents where appropriate, disclaimers, references or bibliography, notes, figures/tables/code formatting, appendices, worksheets, back matter, links, blurb, author name, series data, edition/version date, credentials or bio, and AI-content disclosure status. Mark unverifiable items as `Needs review`, not `Pass`.

## Finding format

Every finding must include all fields below:

### [Severity] Short finding title

- **Location:** chapter/section, page, example, table, figure, code block, or paragraph identifier when available
- **Excerpt:** exact manuscript excerpt, kept brief and verbatim; use `[excerpt unavailable]` only when the location is known but text cannot be quoted
- **Why it matters:** concrete reader, safety, accuracy, production, legal-risk, credibility, or deliverable impact
- **Proposed revision:** minimally invasive action or replacement wording
- **Confidence:** High, Medium, or Low; explain uncertainty when below High

Do not omit a field. For a deliverable checklist row, use the same evidence convention in the notes column. Group findings only when they share a root cause, and name every affected chapter or artifact.

## Final KDP-fix action list

End with a prioritized list of no more than five actions, ordered by severity. Include a separate `Author confirmations needed` subsection for rights ownership, source permissions, factual claims, financial/legal/tax review, technical version targets, credentials, edition data, pen name/legal name decisions, and AI use/disclosure.

## Quality control before responding

- Verify every finding has a severity, location, exact excerpt, rationale, and minimally invasive revision.
- Verify chapter, page, table, figure, code, and quotation references against supplied materials.
- Do not claim plagiarism, copyright infringement, factual verification, code execution, legal compliance, or Amazon approval without evidence.
- Put KDP acceptance and publication-readiness risks before editorial preferences.
- Separate editorial preferences from genuine blockers.
- State what was not checked because the necessary material or external source was absent.
