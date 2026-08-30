---
name: error-analyzer
description: Analyze error logs and identify root causes. Filters noise from large log files, groups errors by pattern, and returns prioritized findings with suggested fixes. Use when asked to "analyze the logs", "what's causing these errors", "check error logs", or when debugging server issues.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Error Log Analyzer

Filter noise from large log files and surface root causes.

## Workflow

1. Identify the log source — check common locations:
   - Zo services: `/dev/shm/<service>.log` and `/dev/shm/<service>_err.log`
   - System logs: `/var/log/`, `journalctl`
   - Application logs: any path the user provides
2. Filter to errors and warnings only:
   ```
   grep -n 'ERROR\|WARN\|Exception\|FATAL\|panic\|CRITICAL' <logfile> | head -200
   ```
3. Group errors by type and pattern (stack trace signature, message template).
4. For each group, determine:
   - Frequency and timing (first/last occurrence)
   - Relevant stack trace frames
   - Likely root cause
   - Suggested fix

## Output Format

```
## Error Summary
Total errors: [N] | Unique patterns: [N] | Time span: [range]

## Pattern 1: [Error Type] (occurred [N] times)
First seen: [timestamp]
Last seen: [timestamp]
Stack: [key frames — max 5 lines]
Likely cause: [explanation]
Suggested fix: [actionable fix]

## Pattern 2: ...
```

## Rules
- Prioritize by frequency × severity. Frequent critical errors first.
- Never dump raw logs into the output — always summarize.
- If a log file exceeds 10MB, use `tail -n 5000` to sample recent entries.
- For Zo services, also check Loki via `/loki/api/v1/query_range` when available.
- Suggest concrete, actionable fixes — not vague "investigate further."
