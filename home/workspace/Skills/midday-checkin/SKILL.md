---
name: midday-checkin
description: Pattern detection for midday check-in.

Scans tasks.db, recent meeting records, and commitments for patterns
worth surfacing. Outputs JSON with categorized findings.

Usage:
    python3 patterns.py [--state-file PATH] [--db PATH] [--records-dir PATH]

The state file tracks what was seen last run for delta detection.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  restored: 2026-08-30
---

# midday-checkin

## Overview

Pattern detection for midday check-in.

Scans tasks.db, recent meeting records, and commitments for patterns
worth surfacing. Outputs JSON with categorized findings.

Usage:
    python3 patterns.py [--state-file PATH] [--db PATH] [--records-dir PATH]

The state file tracks what was seen last run for delta detection.

## Usage

This skill was restored from backup. The original documentation is unavailable.

### Scripts

- `patterns.py`

## Files

```
midday-checkin/
  scripts/
    patterns.py
```
