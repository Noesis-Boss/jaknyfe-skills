---
name: etsy-clipart-workflow
description: "Build recurring, trend-informed Etsy digital-clipart collections: research opportunities, generate and validate transparent PNG assets, package downloads and previews, create Etsy draft listings, and maintain an approval queue. Use when planning or running an Etsy clipart shop workflow, especially on a schedule."
metadata:
  author: jaknyfe.zo.computer
---

# Etsy Clipart Workflow

Run this workflow in approval-gated mode. Generate and prepare artifacts automatically; never activate or publish an Etsy listing without explicit per-collection approval.

## Commands

Use `scripts/workflow.ts` from this skill directory. State defaults to `memory/etsy-clipart-workflow.json`.

- `init` — create state and print setup requirements.
- `queue --topic <topic>` — create a collection work item with prompts and checks.
- `package --dir <collection-dir>` — validate assets, create a ZIP, and write a manifest.
- `etsy-draft --dir <collection-dir> --shop <shop-id> --taxonomy <id>` — create an Etsy draft, upload previews and the digital ZIP, and record IDs.
- `approve --id <id>` — mark prepared work ready for owner review; it does not activate the listing.
- `status` — show current work items.

## Workflow

1. Research a niche using current marketplace signals. Record evidence and date; treat trend signals as hypotheses.
2. Select a narrow buyer and coherent collection. Avoid trademarks, copyrighted characters, living artists' signature styles, celebrity likenesses, and copied competitor artwork.
3. Draft original prompts. Generate transparent PNG assets at consistent dimensions. Inspect every file for artifacts, accidental text, clipped edges, halos, and inconsistent style.
4. Package the asset set with a README, license terms, preview sheet, deterministic filenames, and manifest. The package command must pass before Etsy work begins.
5. Create an Etsy draft listing with supplied facts only. Upload preview images and the ZIP as a digital file. Leave the listing in draft state.
6. Present a review packet with the collection directory, manifest, listing copy, tags, price, Etsy draft ID, and originality/policy checks. Activation is a separate explicit action.

## Guardrails

- Keep API keys and OAuth refresh tokens in Zo Settings > Advanced environment variables. Never write secrets to state, logs, source, or Git.
- Request only `listings_r` and `listings_w` scopes unless a different scope is explicitly needed.
- Do not infer ownership, licensing, trend strength, or trademark safety. Flag uncertainty for human review.
- Recurring automations may research, generate, validate, package, and create drafts. They must stop at the approval queue.
- Retain prompts, model/tool metadata when available, input references, file hashes, validation results, and Etsy IDs.

See `references/api_reference.md` for Etsy API details. Use `scripts/workflow.ts --help` for the executable interface.
