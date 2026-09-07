# Scholarship Discovery

## Issue Log

- 2026-09-07: Global batch could not run. `scripts/discover.py --limit 200` treats `--limit` as a positional integer, falls back to 150, and fails before discovery with `sqlite3.OperationalError: unable to open database file` because its hard-coded `/home/workspace/scholarsearch/data/processed/scholarships.db` is missing. The required `scripts/batch_queue.json` is also absent, and the queue-oriented pipeline imports missing `verification.py`. No records were inserted; only `scholarsearch-site/data/processed/scholarships.db` exists (12,494 rows). Email report sent with exact shortfall.

- 2026-09-06: Global batch blocked. The required `discover.py --limit 200` runner is a legacy placeholder that ignores the documented flag, inserts fabricated sample records without URL verification or deduplication, and targets missing databases. `batch_queue.json`, both requested SQLite databases, and a usable canonical workflow were absent. No records were inserted; no database totals or valid report could be produced.
