# Humanizer regression fixtures

These fixtures are the baseline corpus for a future detector. Each case records the expected result for one pattern and a nearby human passage that should remain clean. A detector runner should load `cases.json`, score both passages, and fail when the expected labels diverge.

Keep fixtures short, concrete, and independent. Add a case when a detector rule changes; rerun every case after changing thresholds or pattern lists.

Run the baseline detector with `python3 Skills/humanizer/fixtures/run_fixtures.py`. Extend `RULES` when adding a detector rule, then add its matching fixture before changing thresholds.

Extract visible copy from a file with `python3 Skills/humanizer/fixtures/run_fixtures.py --file path/to/page.html` or `--file path/to/post.md`. Use `--format html`, `--format markdown`, or `--format plain` to override suffix detection. HTML ignores scripts, styles, metadata, comments, and hidden elements. Markdown keeps fenced code and link destinations while removing presentation syntax.
