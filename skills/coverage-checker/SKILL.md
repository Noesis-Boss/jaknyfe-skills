---
name: coverage-checker
description: Analyze test coverage and identify untested code. Runs the test suite with coverage, parses reports, and surfaces specific untested functions and branches with prioritized fix recommendations. Use when asked to "check coverage", "find untested code", "analyze test gaps", or "what needs tests".
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Coverage Checker

Analyze test coverage gaps and prioritize what needs tests.

## Workflow

1. Detect the test runner and coverage tool used in the project (jest, vitest, pytest, etc.).
2. Run the test suite with coverage enabled.
3. Parse the coverage report output.
4. Identify files with the lowest coverage percentages.
5. For each low-coverage file, read the source and identify:
   - Untested functions
   - Untested branches/conditionals
   - Missing edge cases

## Output Format

```
## Coverage Summary
Total: [X]% | Statements: [X]% | Branches: [X]% | Functions: [X]%

## Lowest Coverage Files
[file path]: [X]% — missing tests for [specific functions]

## Recommended Next Tests
Priority 1: [file] → [function] (handles [critical path])
Priority 2: [file] → [function] (handles [error case])
Priority 3: [file] → [function] (edge case: [description])
```

## Rules
- Auto-detect the test framework — do not ask the user.
- Keep recommendations specific and actionable.
- If coverage tooling is not configured, suggest setting it up and stop.
- Sort by risk: critical paths first, error handling second, edge cases last.
