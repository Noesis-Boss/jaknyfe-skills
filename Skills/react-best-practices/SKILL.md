---
name: react-best-practices
description: React and Next.js performance rules from Vercel Engineering. Use when writing, reviewing, or refactoring React components, hooks, data fetching, or bundle code — especially when a component re-renders too often, a bundle is large, or a page feels sluggish. Triggers on React components, hooks, useMemo/useEffect, Server Components, Suspense, dynamic import, bundle size.
compatibility: Created for Zo Computer
metadata:
  author: vercel
  version: "1.0.0-zo"
  upstream: openai/plugins build-web-apps/react-best-practices
---

# React best practices (Vercel)

66 discrete performance rules, one file per rule, vendored under `plugin/rules/`.
Source: Vercel Engineering. This `SKILL.md` is a Zo router — it tells you **which** rules
to read, not what they say. Do not answer from memory; read the rule file.

## How to use

1. Find the rule by symptom in the table below.
2. Read that one file in `plugin/rules/`. Each is short and self-contained.
3. Apply it to the actual component in this workspace.

Never paste a whole category into context. One rule file is the unit of work.

## Routing by symptom

| Symptom | Read |
| --- | --- |
| Component re-renders on every keystroke or parent render | `rerender-derived-state-no-effect`, `rerender-no-inline-components`, `rerender-split-combined-hooks`, `rerender-simple-expression-in-memo` |
| `useMemo` / `useCallback` that never helps | `rerender-memo`, `rerender-memo-with-default-value` (default-value trap), `rerender-defer-reads` |
| Expensive computation on every render | `js-cache-function-results`, `js-cache-property-access`, `js-set-map-lookups` |
| `useEffect` used for derived state instead of computing during render | `rerender-derived-state` |
| Value stored in `useState` that should be a ref | `rerender-use-ref-transient-values`, `rerender-lazy-state-init` |
| Manual `isPending` boolean around a transition | `rerender-transitions`, `rendering-usetransition-loading` |
| State update inside an effect handler | `rerender-functional-setstate`, `rerender-move-effect-to-event` |
| Long task blocks interaction | `js-batch-dom-css`, `js-early-exit`, `js-min-max-loop`, `js-hoist-regexp`, `js-flatmap-filter`, `js-index-maps`, `js-combine-iterations`, `js-length-check-first`, `js-tosorted-immutable` |
| Large bundle / heavy dependency | `bundle-dynamic-imports`, `bundle-barrel-imports`, `bundle-conditional`, `bundle-defer-third-party`, `bundle-preload` |
| Waterfall of sequential awaits | `async-parallel`, `async-dependencies`, `async-defer-await`, `async-suspense-boundaries` |
| Layout shift or content flash on load | `rendering-hydration-no-flicker`, `rendering-resource-hints`, `rendering-script-defer-async`, `rendering-content-visibility` |
| Slow server component / duplicate data fetch | `server-parallel-fetching`, `server-dedup-props`, `server-hoist-static-io`, `server-cache-react`, `server-cache-lru`, `server-serialization` |
| `onclick` instead of `onClick` | `advanced-event-handler-refs` |

## Applicability on this workspace

Zo runs **Vite + React**, mostly not Next.js. Read the rules as follows:

- **Apply as-is:** every `js-*`, `rerender-*`, `client-*`, `rendering-*`, and most `bundle-*`
  and `async-*` rules. These are framework-agnostic React.
- **Apply the intent, not the code:** the `server-*` rules describe RSC data fetching,
  `cache()`, and `after()`. There is no App Router here. The underlying ideas — parallel
  fetching, dedup, hoisting static work out of the request — still apply to API routes and
  to any future RSC work.
- **Skip:** rules that are purely App-Router navigation or server-action mechanics.

## Relationship to other skills

- `Skills/frontend-design/` — aesthetic direction, taste, visual hierarchy. This skill is
  performance. They do not overlap and do not compete; use both when building a UI.
- `Skills/zo-project-template/` — project scaffolding and the release gate. Independent.
- Standing workspace rule: a change is not done until it is screenshot-verified. These rules
  do not replace that; they are what you apply before the screenshot.

## What was deliberately left out

The upstream skill also shipped `AGENTS.md` (a flat dump of all 66 rules, 2,200 lines) and an
`agents/openai.yaml` Codex-plugin declaration. Both were dropped: the router table above
replaces the flat dump, and Codex-plugin routing does not exist on Zo. `_template.md` and
`_sections.md` are upstream scaffolding for generating new rules — keep them if you extend
this skill.

## Safety posture

66 markdown files, zero scripts, zero executables. SkillSpector scored 23/100 MEDIUM; both
HIGH "Output Handling" findings are false positives — the word "injecting" in
`rendering-hydration-no-flicker` refers to inserting a synchronous `<script>` before
hydration, and `dangerouslySetInnerHTML` appears only inside a fenced code sample.

## Licensing

Vendored from `openai/plugins` for local reference. That bundle ships **no LICENSE file**.
Do not redistribute, fork, or publish this directory. The rule text is Vercel Engineering's.

## Not in the table above

These are still in the bundle and apply when the trigger fits — read the file, do not guess:

- **Lifecycles:** `advanced-init-once`, `advanced-use-latest`, `advanced-event-handler-refs`
- **Async & data:** `async-api-routes`, `async-suspense-boundaries`, `client-swr-dedup`, `server-after-nonblocking`, `server-auth-actions`, `server-cache-react`, `server-serialization`
- **Client storage:** `client-localstorage-schema`, `client-passive-event-listeners`, `client-event-listeners`
- **Re-render:** `rerender-dependencies`, `rerender-use-deferred-value`, `rendering-hydration-suppress-warning`
- **Rendering:** `rendering-activity`, `rendering-animate-svg-wrapper`, `rendering-conditional-render`, `rendering-hoist-jsx`, `rendering-svg-precision`
- **JS micro:** `js-cache-storage`
