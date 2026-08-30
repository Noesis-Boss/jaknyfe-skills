# Chapter 10: Design for Portability, Not for Lock-In

Lock-in is not defined by what you can export at the end — it's defined by what you can pick up and move at any moment without losing fidelity. "You're not paying for software anymore. You're paying ransom for your own workflow."

Case: Marcus (copywriter) ran his whole business in one polished AI writing platform for two years. 34% price hike → three days trying to migrate → prompts/chains/version history lived in a proprietary format → he paid the increase. Brandi built a 12-step research chain; platform switched to per-generation pricing, cost quadrupled, intermediate prompts non-exportable.

## Lock-in's hidden architecture

- Front door: generous free tier, clean interface.
- Back door: proprietary formats, closed community, compounding monthly switching cost.
- Every prompt written inside a platform that can't export as plain text is a brick in the wall between you and the exit.

**Quick test:** find your primary tool's export button. Plain text / markdown / JSON that any other tool can read → portable. Proprietary backup file only that platform can restore → rented land.

## Markdown + local files as the substrate

The resilient pattern: store intelligence in formats that predate the tools that created them. Markdown files, JSON configs, plain-text prompts with curly-brace variables — substrate-agnostic.

Reference layout (Dana's pricing-consultancy system — one set of files, three different AI tools by task, none of them load-bearing):

```
~/brain/
  prompts/
    discovery/     01-client-intake.md, 02-market-mapping.md
    analysis/      01-competitive-audit.md, 02-gap-analysis.md
  outputs/2026-Q3/<client-name>/analysis.md
  config/
    system-prompts.md
    variable-glossary.md
```

Each prompt file = system prompt + variable placeholders + one note on intended output format. Local folder synced to a private git repo. If any tool dies: paste the same files into the replacement. Format-dependent beats tool-dependent.

## The weekend migration test

Thought experiment: primary tool hard-shuts down Friday. You have the weekend. Monday, you must be operational.

- "A few hours, tops" → portable.
- "I'd have to rebuild everything" → not portable; you're one pricing email from capture.

The test separates architecture from habit: it's not about whether you *could* export, but whether the export carries the whole system.

## Version-controlled prompts

Prompts in files → version them like code. Git (or any VCS) gives you:
- History of what changed and when
- The ability to revert when a model update breaks a prompt
- Diffable proof of which edit changed the output

Owen's lesson: he overwrote a working sales-page agent 14 months earlier with no version kept; later a client asked "why did the output change?" and there was no trail. After adopting dated commit messages per revision ("added refusal path for thin-source data — was hallucinating competitor revenue figures"), a later regression took one afternoon: pull old version, diff, revert one line.

## The cost of ignoring portability

- Paying the increase because migration is too expensive (Marcus).
- Losing the chain itself when pricing models flip (Brandi).
- Zero audit trail when outputs drift (pre-versioning Owen).

The commitment is small: prompts as markdown files, not platform library entries; outputs as local files, not platform history tabs; folder structure you chose, not one imposed on you. The friction is seconds per run. The freedom it buys is total.
