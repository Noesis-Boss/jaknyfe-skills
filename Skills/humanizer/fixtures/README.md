# Humanizer regression fixtures

These fixtures are the baseline corpus for a future detector. Each case records the expected result for one pattern and a nearby human passage that should remain clean. A detector runner should load `cases.json`, score both passages, and fail when the expected labels diverge.

Keep fixtures short, concrete, and independent. Add a case when a detector rule changes; rerun every case after changing thresholds or pattern lists.
