# The Original Broheim Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a public, responsive vintage-wanderer creative-alter-ego page at `https://jaknyfe.zo.space/broheim`.

**Architecture:** Create one isolated Zo Space React page route with static editorial content and CSS scoped in the component. Add a single homepage showcase entry pointing to `/broheim`; do not alter existing homepage behavior or its other cards.

**Tech Stack:** React, TypeScript, Tailwind CSS, lucide-react, Zo Space page routes.

## Global Constraints

- Preserve the existing public `/` page and all existing Zo Space routes.
- Create `/broheim` as a public page route; use no API route, dependencies, CMS, authentication, commerce, streaming, or social integrations.
- Use the exact palette: cream `#F2E8D5`, tobacco `#3A2618`, rust `#B4512A`, olive `#68734A`, midnight `#152230`.
- Provide keyboard focus, semantic landmarks, responsive single-column behavior, and `prefers-reduced-motion` support.
- Confirm completion with a live-page screenshot, not only a route-save response.

---

## File structure

- Create Zo Space route: `/broheim` — complete public editorial page and scoped styles.
- Modify Zo Space route: `/` — add one Web Showcase project record for The Original Broheim.
- Create: `docs/superpowers/specs/2026-08-21-original-broheim-design.md` — completed design record.

### Task 1: Build the standalone Broheim route

**Files:**
- Create: Zo Space page route `/broheim`
- Test: browser screenshot of `https://jaknyfe.zo.space/broheim`

**Interfaces:**
- Consumes: no API, workspace file, or external asset.
- Produces: public route `/broheim` with anchors `#dispatches`, `#artifacts`, and `#listening`.

- [ ] **Step 1: Save the route with the defined public visibility**

Use `write_space_route` with `path: "/broheim"`, `route_type: "page"`, and `public: "true"`.

- [ ] **Step 2: Implement the page structure and content**

```tsx
import { ArrowDown, ArrowLeft, Compass, Headphones, MapPin, Sparkles } from "lucide-react";

const dispatches = [
  ["01", "The long route", "Notes on leaving room for the detour."],
  ["02", "Field notes", "Small observations collected before they disappear."],
  ["03", "The good kind of lost", "A working philosophy for uncertain maps."],
];

const artifacts = ["A weathered road atlas", "A motel matchbook", "A borrowed camera", "A notebook with no plan"];
const listening = ["Dust on the Needle", "Night Highway", "Sunday in the Rearview"];

export default function Broheim() {
  return <main className="broheim">{/* hero, dispatches, artifacts, listening room, footer */}</main>;
}
```

Populate the hero with `The Original Broheim` and `Notes from the road, the record shelf, and the long way home.`. Build all five approved sections: Hero, Dispatches, Artifacts, Listening Room, and Footer. Use semantic `header`, `nav`, `section`, and `footer` elements. The hero CTA links to `#dispatches`; the footer return control links to `/`.

- [ ] **Step 3: Add the visual system and motion safeguards**

```css
.broheim { background:#F2E8D5; color:#3A2618; }
.broheim a:focus-visible { outline:3px solid #B4512A; outline-offset:4px; }
@media (prefers-reduced-motion: reduce) {
  .broheim *, .broheim *::before, .broheim *::after { animation:none!important; transition:none!important; }
}
```

Use paper-like gradients and subtle grain through CSS only, avoiding external imagery. Use a two-column editorial grid above 768px and a single column below 768px. Keep body text high-contrast against the cream background. Limit animation to a low-opacity grain drift and card lift on hover.

- [ ] **Step 4: Verify desktop and mobile presentation**

Run:

```bash
agent-browser open http://localhost:3099/broheim
agent-browser screenshot /tmp/broheim-desktop.png --full-page
agent-browser resize 390 844
agent-browser screenshot /tmp/broheim-mobile.png --full-page
```

Expected: all five sections are visible, anchors work, content remains readable, and the narrow view is one column.

- [ ] **Step 5: Commit the documentation update if any was made during implementation**

```bash
git add docs/superpowers/specs/2026-08-21-original-broheim-design.md
git commit -m "docs: finalize Original Broheim design"
```

### Task 2: Surface Broheim in the Zo Space Web Showcase

**Files:**
- Modify: Zo Space page route `/`, `webProjects` array
- Test: homepage Web Showcase modal screenshot

**Interfaces:**
- Consumes: public route URL `/broheim` from Task 1.
- Produces: visible external-style showcase card titled `The Original Broheim`.

- [ ] **Step 1: Add a single project entry**

Add this record to the existing `webProjects` array in `/` without changing any existing records:

```tsx
{ icon: Compass, title: "The Original Broheim", description: "Creative notes, artifacts & the long way home", url: "/broheim", color: "bg-amber-700 hover:bg-amber-600" },
```

Also add `Compass` to the existing `lucide-react` import.

- [ ] **Step 2: Verify the modal link**

Run:

```bash
agent-browser open http://localhost:3099/
agent-browser snapshot -i
```

Click `Web Showcase`, then click `The Original Broheim`.

Expected: the Showcase contains the new card and its click opens `/broheim` with no change to other cards.

- [ ] **Step 3: Capture final live proof**

Run:

```bash
agent-browser open https://jaknyfe.zo.space/broheim
agent-browser screenshot /tmp/broheim-live.png --full-page
```

Expected: the public deployed page visibly renders the vintage-wanderer layout.

## Self-review

- Spec coverage: Task 1 implements each approved section, palette, responsive behavior, accessibility, motion constraint, and public visibility. Task 2 fulfills workspace project visibility without changing the existing homepage layout.
- Placeholder scan: passed; all routes, colors, copy, commands, and expected outcomes are named.
- Interface consistency: `/broheim` is created in Task 1 and referenced unchanged by Task 2.
