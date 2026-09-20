# Voxwerx regression fixtures

These fixtures are the baseline corpus for a future detector. Each case records the expected result for one pattern and a nearby human passage that should remain clean. Extraction cases in `extraction_cases.json` verify that visible-copy preprocessing does not score hidden markup or discard useful Markdown content.

Keep fixtures short, concrete, and independent. Add a case when a detector rule or extraction behavior changes; rerun every case after changing thresholds, pattern lists, or parsing logic.

The fabricated-personal-authority case is intentionally narrow. It catches explicit claims of broad personal authority while leaving ordinary first-person reporting clean; unsupported experience still requires source comparison and fact-integrity review.

The unsupported-credentials-results case is also intentionally narrow. It catches quantified credentials or client outcomes presented without support; concrete results attributed to a named client or source remain clean.

The fabricated-citation-statistic case catches a polished study attribution paired with an unsupported percentage. A bounded result from a clearly described local survey remains clean.

The invented-quote-or-source-link case is intentionally narrow. It catches obviously fake domains and quote-plus-publication claims that need source verification; real links and attributed claims remain clean.

The AI-citation-artifact case is intentionally narrow. It catches pasted model markup such as `[cite: 1]` and `contentReference`; ordinary prose citations remain clean.

The unsupported-date-or-timeline case is intentionally narrow. It catches first-person history claims with an unverified year; dates tied to a named record or source remain clean.

Run the baseline detector with `python3 Skills/voxwerx/fixtures/run_fixtures.py`. Extend `RULES` when adding a detector rule, then add its matching fixture before changing thresholds.

Extract visible copy from a file with `python3 Skills/voxwerx/fixtures/run_fixtures.py --file path/to/page.html` or `--file path/to/post.md`. Use `--format html`, `--format markdown`, or `--format plain` to override suffix detection. HTML ignores scripts, styles, metadata, comments, and hidden elements. Markdown keeps fenced code and link destinations while removing presentation syntax.
