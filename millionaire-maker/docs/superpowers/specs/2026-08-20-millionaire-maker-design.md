# Millionaire Maker Design

## Goal

Create a reusable `Millionaire Maker` skill and standalone frontend that collect a user's financial and personal context, then produce a complete seven-phase wealth-planning prompt for an AI assistant.

## Audience and constraints

- Audience: individuals seeking a practical, ethical, legal, sustainable wealth plan.
- The frontend must work locally without an API key or backend.
- User data stays in the browser unless the user explicitly copies or downloads it.
- The UI must distinguish educational planning from regulated financial advice.
- The workflow must preserve the seven phases extracted from the supplied images.

## Design

The frontend is a Vite/React single-page form with sections for identity, financial position, risk and constraints, skills, goals, and planning preferences. On submit it renders a deterministic prompt containing the user's values and the full seven-phase instructions. It supports copy-to-clipboard, download as Markdown, reset, and sample data.

The skill is a portable `SKILL.md` that tells the agent how to use the collected variables, apply the seven phases, label assumptions and estimates, avoid guarantees, and return a prioritized action plan.

## Success criteria

1. All required variables from the images are inputtable.
2. Generated output includes all seven phases in order.
3. Copy, download, sample data, reset, and validation work.
4. The standalone site builds and renders in a browser screenshot.
5. The skill is usable independently of the frontend.
