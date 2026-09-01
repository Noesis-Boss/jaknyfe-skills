# Scholarship Discovery

## Current discovery model

The multi-channel runner uses university, sponsor, professional-association, and government/nonprofit source classes. Each source page is crawled for scholarship-specific detail pages, then detail pages are crawled one level deeper before endpoint verification. Aggregator and installer sites remain discovery-only and cannot be inserted. The runner reports landing-vs-detail yield and the query-pattern families used for future source expansion.

## Issue Log

- 2026-09-01: Canonical global batch (`discover.py --limit 200`) completed with validated backups and atomic insertion safeguards. It added 5 verified new records per database (10 records reported across both), with 48 duplicates, 3 failed links, and 144 rejected candidates. The batch fell 195 short of the 200-record target; the main causes were generic/page-level candidates and unreachable or TLS/DNS-blocked queued sources. Both databases remained intact at 11,690 total / 2,841 active records.

- 2026-08-31: Reviewed all 8,338 remaining active primary-database rows that were not marked verified. Using guarded 500-row transactions and live endpoint checks, 2,472 passed the publication criteria and 5,866 were deactivated across two resumable passes; cumulative final state is 2,836 active records, all 2,836 marked verified. SQLite integrity check passed. Backup: `scholarsearch/data/link-audit-backups/scholarships-20260831-190144-8920.db`.

- 2026-08-31: Reviewed all 712 active records marked `verified` in the primary database against live URL reachability, direct-application destination rules, aggregate/installer rejection rules, and scholarship-specific destination checks. Results: 364 remained verified/active; 154 broken, 40 suspicious, and 154 rejected records were deactivated. SQLite integrity check passed. Backup: `scholarsearch-site/data/link-audit-backups/scholarships-2026-08-31T18-33-39-957Z.db`.

- 2026-08-31: Canonical global batch (`discover.py --limit 200`) completed with validated backups and atomic insertion safeguards. It added 2 records per database, with 52 duplicates, 1 failed link, and 146 rejected candidates; only 1 candidate passed URL verification. The batch fell 198 short because source pages yielded mostly generic/category/navigation pages and several queued sources were unreachable or TLS/DNS blocked. Database integrity remained intact.
