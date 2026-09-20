---
name: zo-project-template
description: Scaffold and validate isolated Zo projects using README.md, AGENTS.md, SOUL.md, DESIGN.md when applicable, src/, tests/, scripts/, docs/, and .env.example.
metadata:
  author: jaknyfe.zo.computer
---

# Zo Project Template

Use this skill when starting a new project or checking whether an existing project follows the workspace convention.

## Workflow

1. Choose an isolated project directory under `/home/workspace`.
2. Run `scripts/scaffold_project.py <path> --name "Project Name"` before substantive implementation. Add `--manifest` when the project has multiple capabilities or entrypoints. Add repeatable `--publish ID:TYPE:PATH` options to generate declared publish surfaces (`skill`, `agent`, `command`, or `plugin`). The scaffold initializes the isolated Git repository and validates it immediately.
3. Review the generated `README.md`, `AGENTS.md`, and `SOUL.md`; add `DESIGN.md` for frontend work.
4. Optionally add `project.manifest.json` when the project has multiple capabilities or entrypoints. It uses version `1`, may declare supported `harnesses` (`zo`, `codex`, `claude-code`, `cursor`, `gemini`, or `opencode`), and declares each capability's `id`, `description`, `entrypoints`, and `checks`. The validator rejects unknown harness names so cross-harness support stays explicit.
   It may also declare `publish` surfaces with an `id`, `type` (`skill`, `agent`, `command`, or `plugin`), and `path`; validation fails when a declared surface is malformed or its path is missing.
5. Run `scripts/validate_project.py <path>` before the first commit and after structural changes.
6. Keep the generated repository isolated; do not add it to another repository.
7. Install the tracked pre-commit hook with `scripts/install_hooks.py <path>`.
8. Verify the hook installation with `scripts/install_hooks.py <path> --check` after setup or repository migration.
9. Run `scripts/release_gate.py <path>` before declaring a project release-ready. It requires a valid structure, valid manifest paths when present, and a clean Git worktree. Use `--allow-dirty` only for local pre-commit checks.
10. Run `scripts/verify_artifacts.py <path>` to check that declared publish surfaces exist and are non-empty. The release gate runs this check automatically.

For a batch check, run `scripts/validate_projects.py <path>...`; add `--frontend` when every supplied project is a frontend project.

The scaffold creates only the reusable structure. It does not create application code or install dependencies. Existing projects should be validated in place; do not move or rewrite files to satisfy the convention without explicit scope.

## Required structure

- `README.md`
- `AGENTS.md`
- `SOUL.md`
- `src/`
- `tests/`
- `scripts/`
- `docs/`
- `.env.example`
- `.git/`

`DESIGN.md` is required for frontend projects and optional otherwise.
