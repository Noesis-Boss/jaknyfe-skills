---
name: migration-gen
description: Generate database migrations following project conventions. Reads existing migrations to learn naming, tooling, and structure, then creates UP and DOWN migrations. Use when asked to "create a migration", "generate migration for [table]", "add migration", or when adding tables or changing schema.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Database Migration Generator

Generate safe, reversible database migrations that follow project conventions.

## Workflow

1. Read existing migration files to detect:
   - Migration tool (Prisma, Drizzle, Knex, Alembic, etc.)
   - Naming conventions (timestamp, sequential, descriptive)
   - File structure and patterns used in the project
2. Read the current schema or models to understand the starting state.
3. Generate the migration file with both UP and DOWN paths.

## Rules

- Always include both UP (apply) and DOWN (revert) migrations.
- Add indexes for all foreign keys and frequently queried columns.
- Never add `NOT NULL` without a `DEFAULT` value.
- Wrap in a transaction where the tool supports it.
- Match the exact file naming pattern from existing migrations.
- After creating the file, run the migration locally to verify it applies cleanly.
- If the migration fails, fix and re-verify before reporting success.

## Output

State the migration file created, the tool used, and the verification result.
