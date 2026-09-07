# Financial Dashboard Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a hybrid financial-dashboard skill with repeatable FP&A workflow, deterministic data checks, and spreadsheet/web output guidance.

**Architecture:** Keep the skill body concise and route detailed rules to references. Add one dependency-free Python helper for tabular inspection and issue reporting; calculations remain explicit in the workflow so outputs can be adapted to Excel, Sheets, or web apps.

**Tech Stack:** Markdown skill package, Python 3.12 standard library, JSON/CSV outputs.

## Global Constraints

- Never overwrite source data or silently drop rows.
- Mark estimates, forecasts, inferred categories, and missing inputs.
- State currency, date format, timezone, forecast method, and assumptions.
- Web dashboards require screenshot verification before completion.
- No required frontend framework or spreadsheet provider.

### Task 1: Scaffold the skill

**Files:**
- Create: `Skills/financial-dashboard/SKILL.md`
- Create: `Skills/financial-dashboard/references/metrics.md`
- Create: `Skills/financial-dashboard/references/output-guidance.md`

- [ ] Create the package with `init_skill.py`.
- [ ] Write frontmatter and concise routing instructions.
- [ ] Add metric definitions and output-specific guidance.

### Task 2: Add deterministic inspection

**Files:**
- Create: `Skills/financial-dashboard/scripts/inspect_financial_data.py`
- Create: `Skills/financial-dashboard/scripts/test_inspect_financial_data.py`

- [ ] Implement CSV/JSON inspection using only the standard library.
- [ ] Detect missing values, duplicate rows, date/number inconsistencies, blank categories, and unusual numeric entries.
- [ ] Emit JSON containing summary, normalized rows, and a Data Issues table without dropping source rows.
- [ ] Test clean data, duplicates, blanks, invalid dates, and mixed numbers.

### Task 3: Validate and package

**Files:**
- Modify: `Skills/financial-dashboard/SKILL.md`

- [ ] Run the helper tests.
- [ ] Run skill quick validation.
- [ ] Run package validation and inspect the archive contents.
- [ ] Confirm the skill body stays under 500 lines and contains all ten workflow stages.
