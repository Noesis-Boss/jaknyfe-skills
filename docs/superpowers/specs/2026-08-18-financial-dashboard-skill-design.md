# Financial Dashboard Skill Design

## Goal

Create `Skills/financial-dashboard/`, a hybrid workflow for turning financial data into either spreadsheet dashboards, standalone web dashboards, or both. The skill must support repeatable FP&A analysis while preserving source data, exposing assumptions, and validating user-facing outputs.

## Scope

Supported inputs: CSV, XLSX, JSON, SQLite, and pasted tabular data.

Supported outputs:

- Spreadsheet dashboard when the user requests Excel or Google Sheets.
- Standalone web dashboard when the user requests a web interface.
- Both when requested or when the data and task benefit from both formats.

The workflow covers planning, cleaning, executive overview, P&L, cash flow, expense analysis, receivables, forecasting, alerts, and unified dashboard assembly.

## Workflow

1. Inspect files and ask for business type, revenue sources, goals, date range, currency, categories, budgets, thresholds, and output preference.
2. Produce a dashboard plan with eight KPIs, calculations, charts, filters, sections, weekly/monthly decisions, and missing-data findings. Stop for approval before building.
3. Clean data without silent deletion. Preserve the source, create a cleaned copy, and produce a Data Issues table containing row, issue, suggested correction, and confidence.
4. Build the requested analysis views using explicit formulas and assumptions.
5. Combine views into the final spreadsheet and/or web dashboard.
6. Validate calculations, filters, empty states, date and currency formatting, assumptions, exports, and mobile readability. Web output requires screenshot verification before completion.

## Required analysis

Executive KPIs: revenue, expenses, gross profit, net profit, profit margin, cash balance, accounts receivable, and monthly burn rate, each compared with the selected prior period or budget.

P&L: monthly revenue, COGS, gross profit, operating expenses, EBITDA, taxes, net profit, actual-versus-budget variance, year-over-year change, and revenue-to-net-profit waterfall.

Cash flow: operating, investing, and financing flows; opening cash; receipts; payments; closing cash; net movement; burn rate; runway; and a 13-week forecast with assumptions and minimum-cash flags.

Expenses: category, vendor, department, month, recurring charges, sudden increases, possible duplicates, growth versus revenue, and five ranked savings opportunities with annual impact estimates.

Receivables: outstanding and overdue totals, average collection time, 0–30/31–60/61–90/90+ aging, ten priority invoices, and projected collections for 30/60/90 days.

Forecasting: six- or twelve-month conservative, expected, and optimistic scenarios with editable growth, pricing, volume, inflation, and churn assumptions.

Alerts: margin, budget, runway, revenue-decline, and overdue-invoice rules. Each alert includes severity, metric, likely cause, recommended action, and triggering data.

## Architecture

`SKILL.md` contains routing, workflow, safety rules, output selection, and validation gates. `references/` contains concise finance metric and spreadsheet/web output guidance. `scripts/` contains deterministic data inspection and calculation helpers only where repeatability materially improves accuracy. The skill must not require a particular frontend framework or spreadsheet provider.

## Safety and quality rules

- Never overwrite source data or silently drop rows.
- Mark estimates, forecasts, inferred categories, and missing inputs.
- State currency, date format, timezone, forecast method, and assumptions.
- Do not invent budgets, thresholds, customer history, or payment behavior.
- Use green/amber/red statuses only with a visible rule behind each status.
- Keep calculations reproducible and test edge cases such as empty data, negative values, duplicate IDs, and partial periods.
- For web dashboards, do not declare completion from a build or HTTP response alone; capture and inspect a rendered screenshot.

## Success criteria

The installed skill has valid frontmatter, stays under the skill context budget, routes correctly for spreadsheet/web/both requests, preserves source data, exposes data issues and assumptions, supports all ten analysis stages, and provides explicit validation instructions for both output types.
