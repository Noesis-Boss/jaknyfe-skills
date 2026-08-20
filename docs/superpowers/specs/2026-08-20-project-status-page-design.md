---
name: project-status-page
description: Private Zo Space dashboard showing the current state of Don's projects.
type: design-spec
date: 2026-08-20
status: approved-for-spec-review
---

# Project Status Page

## Objective

Create a private Zo Space route at `/project-status` that gives Don a fast, scannable view of the current state of each active or relevant project without changing the existing `/status` service-health page.

## Scope

The first version includes:

- A private page route at `/project-status`.
- Curated project metadata embedded in the route.
- Status summary counts.
- Project cards grouped and filterable by status.
- Priority and category filters.
- Links to workspace paths and live project URLs where available.
- Responsive layout for desktop and mobile.
- Explicit empty states for filters with no matches.

The first version does not include:

- A public API for project metadata.
- Automatic file-system or Git scanning.
- Editing project status from the UI.
- Changes to the existing `/status` route or `/api/status/check`.

## Status model

Each project record contains:

- `name`
- `status`: Active, Blocked, Maintenance, Parked, or Complete
- `priority`: High, Medium, or Low
- `category`
- `phase`
- `objective`
- `nextAction`
- `path`
- `liveUrl`
- `lastActivity`
- `notes`

The curated registry initially covers:

- Robinhood Trading Bot
- Joke Workshop
- Noesis Privacy Documentary
- ScholarSearch
- Scottish Rite and KSA Websites
- Zo Memory
- Zo Skills and Automation

Project status, priority, phase, objective, next action, and notes remain manually curated. Last-activity text and links are explicit registry fields in this first version; automatic derivation is deferred to a later change.

## Page structure

1. Header with page title, private dashboard context, and refresh timestamp.
2. Summary strip showing counts for Active, Blocked, Maintenance, Parked, and Complete.
3. Filter controls for status, priority, and category.
4. Responsive project-card grid.
5. Empty state when the selected filters return no projects.

Each card displays the project name, status badge, priority, phase, objective, next action, last activity, workspace path, and live link when present.

## Interaction and accessibility

- Filters update the visible card set immediately.
- Filter controls use native accessible labels.
- Cards use semantic headings and readable status text, not color alone.
- External links open in a new tab with `noopener noreferrer`.
- Missing paths or links are omitted cleanly.
- The grid collapses to one column on narrow screens.
- Focus-visible states remain clear for controls and links.
- Reduced-motion preferences are respected; no required interaction depends on animation.

## Visual direction

Use a focused operator dashboard: dark neutral background, high-contrast typography, restrained accent colors for status, compact cards, and clear hierarchy. Avoid decorative animation and avoid duplicating the existing homepage aesthetic. The page should prioritize rapid scanning and next-action visibility.

## Data flow

The route contains a local typed project registry and derives:

- Summary counts from the registry.
- Filter options from the registry.
- Visible cards from the selected filters.

No API route is needed in the first version, which keeps the private project information out of a public network endpoint.

## Error and edge handling

- Empty registry: show a clear “No projects configured” state.
- No filter matches: show a clear reset-filters action.
- Missing live URL: render the card without a live-link control.
- Missing workspace path: render the card without a path control.
- Unknown status or priority: prevent invalid values through typed registry definitions.
- Long notes or next actions: clamp visually without removing the full accessible text.

## Verification

Completion requires:

- The private `/project-status` route loads successfully.
- All seven initial project cards render.
- Summary counts match the registry.
- Status, priority, and category filters work.
- Resetting filters restores all cards.
- Workspace and live links point to the intended destinations.
- Empty states render correctly.
- The layout remains readable at mobile width.
- A browser screenshot confirms the rendered result.
- Existing `/status` behavior remains unchanged.

## Future extension

A later version may add a safe server-side or authenticated update workflow for automatic last-activity detection and status editing. That is intentionally outside this implementation.
