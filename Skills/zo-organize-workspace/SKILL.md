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

2. **Identify and validate projects**
   - Find likely project roots using evidence such as a Git root, `zosite.json`, `package.json`, language/build manifests, project-specific `README.md` or `AGENTS.md`, and established workspace project paths. Do not label every directory or repository as a Zo project automatically.
   - For each likely standalone Zo project, report its path, evidence, whether it has its own Git repository, and whether it appears frontend-based.
   - Check its structure against `Skills/zo-project-template/`: `README.md`, `AGENTS.md`, `SOUL.md`, `src/`, `tests/`, `scripts/`, `docs/`, `.env.example`, and its own `.git/`. Frontend projects also require `DESIGN.md`.
   - Use `Skills/zo-project-template/scripts/validate_project.py <path>` or `validate_projects.py <paths...>` for validation. Use `--frontend` only for confirmed frontend projects. Report missing items and validator failures separately from workspace organization findings.
   - Validation is read-only. Do not scaffold, initialize Git, create missing files, or move files to make a project pass. Offer those as separate follow-up work requiring explicit approval.

3. **Protect existing structures**
   - Do not move, rename, or reorganize any directory containing `zosite.json`, or any directory named `Articles` or `Prompts`.
   - Preserve project roots, Git repositories, submodules, datasets with their own documentation, and directories with clear existing purpose.
   - Never move credentials, secrets, session files, databases, logs, runtime state, or unknown files based only on extension. Flag uncertain items for review.

4. **Check impact before proposing moves**
   - For each candidate, inspect Git status and search for path references in scripts, configs, documentation, workflows, and manifests.
   - Keep files beside the project or workflow that uses them, even if their file type suggests a generic destination.
   - Detect destination collisions and propose a distinct destination; never overwrite or merge files automatically.
   - Do not create generic `Projects/`, `Research/`, `Data/`, `Documents/`, or `Archive/` folders unless the inventory shows a concrete need.

5. **Produce a reviewable plan; do not execute it automatically**
   - List each proposed source and destination, reason, reference-check result, and any uncertainty.
   - Exclude any item whose ownership, purpose, references, or destination is unclear; ask a focused question for those items.
   - Moving files across projects or outside a single project requires explicit user approval of the exact move list. Workspace-wide moves require explicit approval before execution, even if the user asked to organize the workspace generally.
   - After approval, execute only approved moves. Use reversible moves, preserve directory structure where practical, and never delete source files or directories as cleanup. Do not use bulk shell moves that include unreviewed paths.

6. **Verify approved moves**
   - Confirm each destination exists and matches its source, check that no collision occurred, and rerun targeted reference searches for affected paths.
   - Report moved-file count and destinations, skipped/manual-review items, and verification results. If a move breaks a reference, restore the original location and report the cause.

7. **Document only completed changes**
   - Create or update `WORKSPACE_STRUCTURE.md` only when the user asks for durable documentation or approved moves materially change the structure.
   - Document current paths and purpose; do not claim proposed moves as completed.

# Output

For an audit-only request, report project roots identified, template validation results, current organization, key risks, and recommended next action. For a reorganization request, first return the exact proposed move list and wait for approval before executing any workspace-wide changes. After execution, summarize completed moves, destinations, skipped decisions, and verification. Keep project-conformance fixes as a separate approved task; do not imply that organizing files automatically makes a project conform to the template.
