---
name: scholarship-discovery
description: Apply Arizona Masonic scholarship discovery to a given scholarships DB.

Idempotent: enriches known existing AZ Masonic rows and inserts new real
scholarships found via web research (June 2026). Run for both the working
DB and the live site DB so they stay consistent.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  restored: 2026-08-30
---

# scholarship-discovery

## Overview

Apply Arizona Masonic scholarship discovery to a given scholarships DB.

Idempotent: enriches known existing AZ Masonic rows and inserts new real
scholarships found via web research (June 2026). Run for both the working
DB and the live site DB so they stay consistent.

## Usage

This skill was restored from backup. The original documentation is unavailable.

### Scripts

- `apply_az_masonic.py`
- `backfill_hash.py`
- `batch_discover.py`
- `batch_discover2.py`
- `batch_insert_200.py`
- `batch_parse_and_insert.py`
- `clean_discover.py`
- `crawl_directory_sources.py`
- `db_safety.py`
- `deep_discover.py`

## Files

```
scholarship-discovery/
  scripts/
    apply_az_masonic.py
    backfill_hash.py
    batch_discover.py
    batch_discover2.py
    batch_insert_200.py
    batch_parse_and_insert.py
    batch_queue.json
    candidates.json
    candidates2.json
    clean_discover.py
    crawl_directory_sources.py
    db_safety.py
    deep_discover.py
    deep_found.json
    discover.py
    discover2.py
    discover_az_masonic.py
    discover_from_files.py
    discover_from_pages.py
    discover_from_search.py
    ... (27 more files)
    tests/
      test_db_safety.py
      test_discovery_pipeline.py
      test_link_recovery.py
      test_verification.py
      __pycache__/
        test_db_safety.cpython-311.pyc
        test_discovery_pipeline.cpython-311.pyc
        test_link_recovery.cpython-311.pyc
        test_verification.cpython-311.pyc
    __pycache__/
      crawl_directory_sources.cpython-311.pyc
      crawl_directory_sources.cpython-312.pyc
      db_safety.cpython-311.pyc
      deep_discover.cpython-311.pyc
      deep_research.cpython-311.pyc
      discover.cpython-311.pyc
      discovery_pipeline.cpython-311.pyc
      link_recovery.cpython-311.pyc
      run_discovery_batch.cpython-311.pyc
      sitemap_discover.cpython-311.pyc
      university_research.cpython-311.pyc
      verification.cpython-311.pyc
```
