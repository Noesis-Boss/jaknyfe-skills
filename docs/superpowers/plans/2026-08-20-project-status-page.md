# Project Status Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a private Zo Space `/project-status` page showing curated current state for seven projects with summary counts, filters, links, and responsive cards.

**Architecture:** Preserve the existing `/status` service-health page and add a separate page route. Keep the project registry local to the page route so private project notes are not exposed through a public API. React state derives summary counts and filtered cards from typed registry data.

**Tech Stack:** Zo Space page route, React, TypeScript/TSX, Tailwind CSS utility classes, browser verification with agent-browser.

## Global Constraints

- Route path: `/project-status`.
- Visibility: private.
- Do not modify `/status` or `/api/status/check`.
- Do not add an API route for project metadata.
- Do not install npm packages in Zo Space.
- Use semantic accessible labels and visible text for status; color cannot be the only status signal.
- Verify the rendered page with a browser screenshot before declaring completion.
- Initial registry contains exactly seven projects from the approved spec.

---

### Task 1: Create the private project-status route

**Files:**
- Create: Zo Space page route `/project-status` using `write_space_route`.

**Interfaces:**
- Produces a private page route exporting a default React component.
- Registry record shape:

```ts
type Status = "Active" | "Blocked" | "Maintenance" | "Parked" | "Complete";
type Priority = "High" | "Medium" | "Low";

type Project = {
  name: string;
  status: Status;
  priority: Priority;
  category: string;
  phase: string;
  objective: string;
  nextAction: string;
  path?: string;
  liveUrl?: string;
  lastActivity: string;
  notes: string;
};
```

- [ ] **Step 1: Confirm the existing route boundary**

Run `get_space_route("/status")` and confirm the existing service-health page remains untouched.

Expected: existing `/status` code is returned; no edit is made to it.

- [ ] **Step 2: Define the seven-project registry**

Add a `const projects: Project[]` registry for:

```ts
const projectNames = [
  "Robinhood Trading Bot",
  "Joke Workshop",
  "Noesis Privacy Documentary",
  "ScholarSearch",
  "Scottish Rite and KSA Websites",
  "Zo Memory",
  "Zo Skills and Automation",
] as const;
```

Each record must include a truthful status, priority, phase, objective, next action, path, live URL when available, last activity, and notes based on current workspace guidance. Do not invent links or project facts; omit unavailable links.

- [ ] **Step 3: Add the route shell and registry**

Create the private page with:

```tsx
import { useMemo, useState } from "react";

export default function ProjectStatus() {
  const [statusFilter, setStatusFilter] = useState<"All" | Status>("All");
  const [priorityFilter, setPriorityFilter] = useState<"All" | Priority>("All");
  const [categoryFilter, setCategoryFilter] = useState("All");

  const filteredProjects = useMemo(
    () => projects.filter((project) =>
      (statusFilter === "All" || project.status === statusFilter) &&
      (priorityFilter === "All" || project.priority === priorityFilter) &&
      (categoryFilter === "All" || project.category === categoryFilter)
    ),
    [statusFilter, priorityFilter, categoryFilter]
  );

  return <main>{/* dashboard UI added in later tasks */}</main>;
}
```

- [ ] **Step 4: Sync the route as private**

Call `write_space_route` with `path="/project-status"`, `route_type="page"`, `public="false"`, and the complete valid TSX route code.

Expected: route metadata reports `public=False`.

---

### Task 2: Build the dashboard summary and project cards

**Files:**
- Modify: Zo Space route `/project-status`.

**Interfaces:**
- Consumes the `Project` type, `projects` registry, and `filteredProjects` from Task 1.
- Produces visible summary cards and project cards.

- [ ] **Step 1: Add derived summary counts**

Use the fixed status order and derive counts from the registry:

```ts
const statusOrder: Status[] = ["Active", "Blocked", "Maintenance", "Parked", "Complete"];

const counts = statusOrder.reduce<Record<Status, number>>((result, status) => {
  result[status] = projects.filter((project) => project.status === status).length;
  return result;
}, {
  Active: 0,
  Blocked: 0,
  Maintenance: 0,
  Parked: 0,
  Complete: 0,
});
```

- [ ] **Step 2: Add the header and summary strip**

Render:

```tsx
<header>
  <p>Private operator dashboard</p>
  <h1>Project Status</h1>
  <p>Current state, next actions, and active delivery context.</p>
  <time dateTime={lastUpdatedIso}>Last refreshed: {lastUpdatedLabel}</time>
</header>
<section aria-label="Project status summary">
  {statusOrder.map((status) => (
    <button key={status} onClick={() => setStatusFilter(status)}>
      <span>{status}</span>
      <strong>{counts[status]}</strong>
    </button>
  ))}
</section>
```

Status summary buttons must update the status filter and provide visible active styling.

- [ ] **Step 3: Add project cards**

Each card must include:

```tsx
<article aria-labelledby={projectId}>
  <div>
    <span>{project.status}</span>
    <span>{project.priority} priority</span>
  </div>
  <h2 id={projectId}>{project.name}</h2>
  <p>{project.objective}</p>
  <p><strong>Phase:</strong> {project.phase}</p>
  <p><strong>Next:</strong> {project.nextAction}</p>
  <p><strong>Last activity:</strong> {project.lastActivity}</p>
  <p>{project.notes}</p>
  {project.path && <span>{project.path}</span>}
  {project.liveUrl && <a href={project.liveUrl} target="_blank" rel="noopener noreferrer">Open project</a>}
</article>
```

Use semantic headings, readable labels, and status text in addition to accent colors.

- [ ] **Step 4: Add no-project and no-match states**

Render `No projects configured` when the registry is empty. Render `No projects match these filters` and a `Reset filters` button when filtering returns zero records.

---

### Task 3: Add filters and responsive styling

**Files:**
- Modify: Zo Space route `/project-status`.

**Interfaces:**
- Consumes the existing filter state and `filteredProjects`.
- Produces immediately responsive filtering and mobile-readable layout.

- [ ] **Step 1: Add labeled native filter controls**

Render labeled `select` controls for:

```tsx
<label>
  Status
  <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value as "All" | Status)}>
    <option value="All">All statuses</option>
    {statusOrder.map((status) => <option key={status}>{status}</option>)}
  </select>
</label>
```

Repeat the same pattern for priority and category. Build category options from the registry and include `All categories`.

- [ ] **Step 2: Add reset behavior**

Implement:

```ts
function resetFilters() {
  setStatusFilter("All");
  setPriorityFilter("All");
  setCategoryFilter("All");
}
```

Connect it to the reset button and ensure all seven cards return.

- [ ] **Step 3: Add responsive layout**

Use a dark neutral page shell, high-contrast text, compact status accents, and a responsive grid:

```tsx
<div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
  {filteredProjects.map((project) => (
    <ProjectCard key={project.name} project={project} />
  ))}
</div>
```

Use `min-w-0`, readable line lengths, visible focus states, and a one-column layout below the medium breakpoint.

- [ ] **Step 4: Preserve motion accessibility**

Do not require animation. If transitions are used, add a reduced-motion media rule or omit transitions entirely.

---

### Task 4: Verify the route and commit the implementation

**Files:**
- Verify: Zo Space route `/project-status`.
- Verify unchanged: Zo Space route `/status`.

- [ ] **Step 1: Confirm route metadata**

Run `list_space_routes()`.

Expected: `/project-status` exists as a private page route and `/status` remains present.

- [ ] **Step 2: Open the local route**

Run:

```bash
agent-browser open http://localhost:3099/project-status
sleep 3
agent-browser screenshot /tmp/project-status-desktop.png --full-page
```

Expected: page renders without a blank screen or runtime error.

- [ ] **Step 3: Verify visible behavior**

Use `agent-browser snapshot -i` and test:

- All seven project cards appear initially.
- A status summary button filters the cards.
- Status, priority, and category selects filter cards.
- Reset filters restores all cards.
- A filter with no matches shows the empty state.
- Live project links have valid target URLs.

- [ ] **Step 4: Verify mobile layout**

Run an agent-browser viewport or mobile-sized browser check and capture:

```bash
agent-browser screenshot /tmp/project-status-mobile.png --full-page
```

Expected: cards are one column, text remains readable, and controls do not overflow horizontally.

- [ ] **Step 5: Check runtime errors**

Call `get_space_errors()`.

Expected: no new errors attributable to `/project-status`.

- [ ] **Step 6: Commit the route change**

After screenshot verification succeeds, commit the route change with:

```bash
git add docs/superpowers/specs/2026-08-20-project-status-page-design.md
git commit -m "Add private project status page"
```

The route itself is managed by Zo Space; the repository commit records the accompanying project specification and implementation handoff.

