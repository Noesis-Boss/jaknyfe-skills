# Idea Desk Assistant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Idea Desk assistant button open a modal that returns a real, idea-specific AI assessment and accepts contextual follow-up questions.

**Architecture:** Add a dedicated Zo Space API route at `/api/idea-desk/ask` that validates selected-idea input, constructs the trusted prompt, and calls the Zo Ask API with the server-side `ZO_API_KEY`. Update the existing private `/idea-desk` page with isolated modal state, request handling, and accessible close/follow-up behavior while preserving all research controls.

**Tech Stack:** Zo Space, React, TypeScript, Hono, Tailwind CSS, Zo Ask API, agent-browser.

## Global Constraints

- Preserve `/idea-desk` as private.
- Preserve scanning, source filters, minimum-score filtering, sorting, selection, and current styling.
- Do not expose `ZO_API_KEY` or trusted prompt text to the browser.
- Do not install packages in Zo Space.
- Require screenshot verification of a rendered AI response before completion.

---

### Task 1: Dedicated assistant API

**Files:**
- Create: Zo Space API route `/api/idea-desk/ask`

**Interfaces:**
- Consumes: `POST { idea: { title, source, score, painPoint, synthesis, audience, reason, angle, url }, question?: string, priorAnswer?: string }`
- Produces: HTTP 200 `{ answer: string }`; HTTP 400/500/502 `{ error: string }`

- [ ] **Step 1: Record the precondition failure**

Run:

```bash
curl -sS -X POST http://localhost:3099/api/idea-desk/ask \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  --data '{"idea":{"title":"Test idea","source":"YouTube"}}'
```

Expected: route-not-found response because `/api/idea-desk/ask` does not exist.

- [ ] **Step 2: Create the API route**

Use `write_space_route` with `route_type="api"`. Implement:

```ts
import type { Context } from "hono";

const limit = (value: unknown, max: number) => String(value ?? "").trim().slice(0, max);

export default async (c: Context) => {
  if (c.req.method !== "POST") return c.json({ error: "Method not allowed." }, 405);
  const body = await c.req.json().catch(() => null);
  const title = limit(body?.idea?.title, 300);
  const source = limit(body?.idea?.source, 40);
  if (!title || !source) return c.json({ error: "A selected idea is required." }, 400);
  const token = process.env.ZO_API_KEY;
  if (!token) return c.json({ error: "Idea Desk AI is not configured." }, 500);

  const idea = {
    title, source,
    score: Number(body?.idea?.score) || 0,
    painPoint: limit(body?.idea?.painPoint, 800),
    synthesis: limit(body?.idea?.synthesis, 800),
    audience: limit(body?.idea?.audience, 300),
    reason: limit(body?.idea?.reason, 800),
    angle: limit(body?.idea?.angle, 800),
    url: limit(body?.idea?.url, 800),
  };
  const question = limit(body?.question, 1000);
  const priorAnswer = limit(body?.priorAnswer, 5000);
  const instruction = question
    ? `Answer this follow-up about the idea: ${question}\nPrior assessment: ${priorAnswer}`
    : "Assess viability, target audience, best content format, differentiation, key risks, and finish with one concrete next action.";
  const prompt = `You are the Idea Desk assistant. Give practical, concise advice grounded only in the supplied idea.\n\nIdea: ${JSON.stringify(idea)}\n\n${instruction}`;

  try {
    const response = await fetch("https://api.zo.computer/zo/ask", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ input: prompt }),
      signal: AbortSignal.timeout(45000),
    });
    const data = await response.json().catch(() => null);
    const answer = typeof data?.output === "string" ? data.output.trim() : "";
    if (!response.ok || !answer) return c.json({ error: "The assistant could not answer. Try again." }, 502);
    return c.json({ answer });
  } catch {
    return c.json({ error: "The assistant timed out. Try again." }, 502);
  }
};
```

- [ ] **Step 3: Verify validation and live generation**

Run the precondition curl again and then a complete request using a real idea from `/api/idea-desk`.

Expected: incomplete input returns HTTP 400; complete input returns HTTP 200 with a non-empty `answer` tied to the idea.

### Task 2: Modal and contextual follow-up

**Files:**
- Modify: Zo Space page route `/idea-desk`

**Interfaces:**
- Consumes: selected `Idea`; `/api/idea-desk/ask` response `{ answer?: string, error?: string }`
- Produces: accessible modal with initial assessment, retry, and follow-up states

- [ ] **Step 1: Add isolated assistant state and request function**

Use `edit_space_route` to add `assistantOpen`, `assistantLoading`, `assistantAnswer`, `assistantError`, and `followUp` state. Add `askAssistant(question = "")`, which opens the modal, clears stale state for an initial request, POSTs the selected idea, question, and prior answer, then stores either `answer` or `error`.

- [ ] **Step 2: Wire the existing button**

Change only the existing **Ask assistant about this idea** button to call `askAssistant()` and disable it when no idea is selected.

- [ ] **Step 3: Render the modal**

Add a fixed backdrop and dialog after the main dashboard section. Include the selected title, `aria-modal="true"`, loading copy, whitespace-preserving answer text, retry button, follow-up form, and close button. Backdrop click closes the dialog; clicks inside stop propagation.

- [ ] **Step 4: Add keyboard behavior**

Add an effect active only while the modal is open that closes it on Escape and restores normal document behavior during cleanup.

- [ ] **Step 5: Check Space runtime errors**

Run `get_space_errors`.

Expected: no new build or runtime error for `/idea-desk` or `/api/idea-desk/ask`.

### Task 3: End-to-end visual verification and documentation

**Files:**
- Modify: `/home/workspace/AGENTS.md`
- Create: `/home/workspace/Media/screenshots/idea-desk-assistant-response.png`

**Interfaces:**
- Consumes: live private Idea Desk page through localhost preview
- Produces: visible proof and durable issue-log entry

- [ ] **Step 1: Exercise the dashboard regression path**

Open `http://localhost:3099/idea-desk`, change source, score, and sort controls, select an idea, and run a scan.

Expected: all existing controls remain operable and the selected synthesis updates.

- [ ] **Step 2: Exercise initial AI response and follow-up**

Click **Ask assistant about this idea**, wait for a substantive response, submit `What is the fastest way to validate this?`, and wait for the contextual reply.

Expected: the modal retains the selected idea title and replaces the answer with a relevant follow-up response.

- [ ] **Step 3: Verify close paths**

Reopen the modal and verify close button, Escape, and backdrop click independently.

Expected: each closes the modal without navigating or changing the selected idea.

- [ ] **Step 4: Capture rendered proof**

Run:

```bash
agent-browser screenshot /home/workspace/Media/screenshots/idea-desk-assistant-response.png --full-page
```

Expected: screenshot visibly shows the selected idea and non-placeholder assistant response.

- [ ] **Step 5: Document the fix**

Append one Issue Log entry to `/home/workspace/AGENTS.md` stating the broken button was wired to `/api/idea-desk/ask`, the modal supports contextual follow-ups, and live screenshot verification passed.

- [ ] **Step 6: Commit documentation artifacts**

Run:

```bash
git add AGENTS.md Media/screenshots/idea-desk-assistant-response.png
git commit -m "Document Idea Desk assistant fix"
```

Expected: commit contains only the Issue Log entry and verification screenshot.
