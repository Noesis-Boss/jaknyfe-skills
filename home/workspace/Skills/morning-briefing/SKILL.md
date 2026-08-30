---
name: morning-briefing
description: Query tasks.db for the morning briefing.

Returns JSON with overdue tasks, tasks due today, and a count of
undated pending tasks. Requires DuckDB and a tasks table with columns:
id, title, source, priority, due_date, status, context.

If the database doesn't exist, prints an empty result and exits cleanly.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  restored: 2026-08-30
---

# morning-briefing

## Overview

Query tasks.db for the morning briefing.

Returns JSON with overdue tasks, tasks due today, and a count of
undated pending tasks. Requires DuckDB and a tasks table with columns:
id, title, source, priority, due_date, status, context.

If the database doesn't exist, prints an empty result and exits cleanly.

## Usage

This skill was restored from backup. The original documentation is unavailable.

### Scripts

- `tasks_query.py`

## Files

```
morning-briefing/
  scripts/
    tasks_query.py
```
