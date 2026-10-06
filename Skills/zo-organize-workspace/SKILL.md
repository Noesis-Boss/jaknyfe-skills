---
name: organize-workspace
description: Audits workspace organization and prepares a safe, reviewable file-move plan
metadata:
  author: Zo
  category: Official
  display-name: Organize my files
  emoji: 🗂️
---
Audit workspace organization and improve discoverability without disrupting projects or losing data.

# Protocol

1. **Inventory before proposing changes**
   - Identify root-level loose files, existing folder conventions, project boundaries, and meaningful semantic groupings.
   - Report counts and representative paths. Do not dump huge inventories into chat; save a complete proposal only if useful and requested.
   - Exclude `.git`, dependency/build caches, runtime state, and `Trash` from broad inventory walks unless the user specifically asks to include them.

2. **Protect existing structures**
   - Do not move, rename, or reorganize any directory containing `zosite.json`, or any directory named `Articles` or `Prompts`.
   - Preserve project roots, Git repositories, submodules, datasets with their own documentation, and directories with clear existing purpose.
   - Never move credentials, secrets, session files, databases, logs, runtime state, or unknown files based only on extension. Flag uncertain items for review.

3. **Check impact before proposing moves**
   - For each candidate, inspect Git status and search for path references in scripts, configs, documentation, workflows, and manifests.
   - Keep files beside the project or workflow that uses them, even if their file type suggests a generic destination.
   - Detect destination collisions and propose a distinct destination; never overwrite or merge files automatically.
   - Do not create generic `Projects/`, `Research/`, `Data/`, `Documents/`, or `Archive/` folders unless the inventory shows a concrete need.

4. **Produce a reviewable plan; do not execute it automatically**
   - List each proposed source and destination, reason, reference-check result, and any uncertainty.
   - Exclude any item whose ownership, purpose, references, or destination is unclear; ask a focused question for those items.
   - Moving files across projects or outside a single project requires explicit user approval of the exact move list. Workspace-wide moves require explicit approval before execution, even if the user asked to organize the workspace generally.
   - After approval, execute only approved moves. Use reversible moves, preserve directory structure where practical, and never delete source files or directories as cleanup. Do not use bulk shell moves that include unreviewed paths.

5. **Verify approved moves**
   - Confirm each destination exists and matches its source, check that no collision occurred, and rerun targeted reference searches for affected paths.
   - Report moved-file count and destinations, skipped/manual-review items, and verification results. If a move breaks a reference, restore the original location and report the cause.

6. **Document only completed changes**
   - Create or update `WORKSPACE_STRUCTURE.md` only when the user asks for durable documentation or approved moves materially change the structure.
   - Document current paths and purpose; do not claim proposed moves as completed.

# Output

For an audit-only request, report the current state, key risks, and recommended next action. For a reorganization request, first return the exact proposed move list and wait for approval before executing any workspace-wide changes. After execution, summarize completed moves, destinations, skipped decisions, and verification.
