# ScholarSearch: 5,000 verified production scholarships

## Objective

Raise the production search inventory to at least 5,000 globally unique, active, verified scholarships. Every published record must have an active direct application endpoint controlled by the sponsor, school, government body, or authorized administrator. Aggregators and installer destinations remain discovery-only.

## Execution

1. Establish a baseline for both production databases and preserve timestamped backups.
2. Build a source registry across official university directories, government agencies, foundations, professional associations, employers, nonprofits, and international scholarship offices.
3. Crawl source indexes, follow individual opportunity pages, extract structured fields, and retain provenance.
4. Resolve failed or indirect links by bounded same-domain crawling and official-domain search.
5. Verify status, redirect destination, page identity, application language, deadline state, and disallowed-host rules.
6. Deduplicate against both databases before atomic insertion into both.
7. Run in bounded batches, emit counters, and stop publishing on any invariant failure.
8. Repeat until the site mirror has at least 5,000 active verified records; then run the strict release report and a browser verification.

## Quality gates

- `active = 1` and `url_status = 'verified'`
- direct application or official submission instructions present
- no known aggregator, app store, installer, social, generic, or dead URL
- unique scholarship identity and sponsor
- source, recovery, and verification evidence retained
- both databases agree on the published verified inventory

## Operational target

The system will measure verified additions, not pages crawled. Initial batches are calibration runs; sustained throughput is reported separately from the final 5,000-record gate.
