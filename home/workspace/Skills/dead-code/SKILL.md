---
name: dead-code
description: Find unused code, unreachable exports, and orphaned files across a codebase. Recursively scans exports, traces imports, and generates a cleanup hitlist. Use when asked to "find dead code", "clean up unused code", "sweep for orphans", or "what can I delete".
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Dead Code Sweeper

Scan a codebase for unused exports, orphaned files, and cleanup candidates.

## Workflow

1. Discover all exported functions, classes, constants, and types across the codebase.
2. For each export, search for imports and usages in all other project files.
3. Identify three categories:
   - **Unused Exports**: exported but never imported anywhere
   - **Orphaned Files**: files never imported by any other project file
   - **Unreachable Code**: functions defined but never called (within their own file)

## Output Format

```
## Unused Exports
[file]: `[export name]` — not imported anywhere

## Orphaned Files
[file path] — never imported by any other file in the project

## Cleanup Candidates
[file]: [description of what can be removed and why]

## Summary
- [N] unused exports found
- [N] orphaned files found
- [N] cleanup candidates (estimated [N] lines removable)
```

## Rules
- Be conservative. If uncertain about an export, mark it as `⚠ verify before removing`.
- Skip well-known entry points (main.tsx, index.ts, App.tsx, server entrypoints).
- Skip exports used only in test files unless the test file is also orphaned.
- Exclude `node_modules/`, `dist/`, `build/`, `.git/` from scanning.
- For TypeScript, also flag unused type-only exports.
