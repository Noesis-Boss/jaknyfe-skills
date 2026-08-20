# Millionaire Maker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a standalone React prompt builder and a reusable seven-phase wealth-planning skill.

**Architecture:** A local-first Vite/React app stores form state in memory and generates a Markdown prompt. The skill is a standalone `SKILL.md` with structured intake, analysis, output, and safety rules.

**Tech Stack:** Vite, React, TypeScript, CSS, Bun.

## Global Constraints

- No backend or API keys.
- No financial guarantees or personalized regulated advice claims.
- Preserve all seven prompt phases in order.
- Touch only the new `millionaire-maker` project and skill.

### Task 1: Create the reusable skill

**Files:**
- Create: `Skills/millionaire-maker/SKILL.md`

- [ ] Write the skill with frontmatter, intake variables, seven phases, output contract, and safety boundaries.
- [ ] Confirm all seven phases and required variables are present with `rg`.

### Task 2: Create the frontend shell

**Files:**
- Create: `millionaire-maker/package.json`
- Create: `millionaire-maker/index.html`
- Create: `millionaire-maker/src/main.tsx`
- Create: `millionaire-maker/src/styles.css`

- [ ] Add the minimal Vite React setup.
- [ ] Add responsive dark-gold visual styling.

### Task 3: Build prompt generation and UI

**Files:**
- Create: `millionaire-maker/src/App.tsx`

- [ ] Add all input variables and validation.
- [ ] Generate the seven-phase prompt deterministically.
- [ ] Add sample, reset, copy, download, and generated-prompt preview actions.

### Task 4: Verify

- [ ] Run `bun install` and `bun run build` in `millionaire-maker`.
- [ ] Start the dev server through the project tooling.
- [ ] Capture a browser screenshot showing the rendered form and generated output.
- [ ] Test sample data, copy/download controls, and required-field validation.
