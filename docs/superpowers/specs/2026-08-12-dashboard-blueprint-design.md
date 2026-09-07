# Dashboard Blueprint Skill Design

Date: 2026-08-12

## Goal

Create a reusable skill that turns a dashboard request into a complete premium UI blueprint and, when code is requested, production-ready implementation snippets.

## Scope

The skill covers seven connected concerns: layout, data visualizations, dark mode, collapsible navigation, empty states, loading skeletons, and a realistic premium-quality assessment.

## Behavior

1. Extract the product, audience, metrics, data shape, framework, and constraints.
2. State assumptions when details are missing; ask only questions that materially affect the result.
3. Produce the 30-minute build map before implementation details.
4. Select chart types based on the metric's meaning and data shape.
5. Provide exact tokens, interaction states, copy, accessibility requirements, and responsive behavior.
6. Provide complete code only when code is requested or clearly useful, matching the detected stack.
7. End with an honest outcome assessment and the next highest-value polish step.

## Output Contract

Use these sections when applicable: Product assumptions, Premium direction, Layout map, Visualization map, Component specifications, 30-minute build sequence, Implementation code, Accessibility and responsive checks, Honest outcome.

## Guardrails

Do not invent business metrics, data, brand colors, or package dependencies without labeling assumptions. Do not use animation that harms readability or accessibility. Respect existing project instructions, DESIGN.md tokens, and framework conventions when editing a real project.

