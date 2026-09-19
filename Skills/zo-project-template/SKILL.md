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
2. Run `scripts/scaffold_project.py <path> --name "Project Name"` before substantive implementation.
3. Review the generated `README.md`, `AGENTS.md`, and `SOUL.md`; add `DESIGN.md` for frontend work.
4. Run `scripts/validate_project.py <path>` before the first commit and after structural changes.
5. Initialize the project as its own Git repository if `.git` is absent.

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
