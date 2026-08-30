# Template for generated skills

Copy this into `/home/workspace/Skills/<new-slug>/SKILL.md`, fill the `{{placeholders}}`, delete the template note. Create `references/` and `references/approved-examples.md` (empty stub) in the same folder.

---

```markdown
---
name: {{slug}}
description: {{One sentence of what it does}}. Use when the user says "{{trigger phrase 1}}", "{{trigger phrase 2}}", or {{trigger situation}}. Do not use for {{near-miss case}}.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zocomputer.com
---

# {{Skill Name}}

## Objective

{{One-sentence goal of what this skill achieves.}}

## Process

0. Before generating anything, read these reference files (skip any that don't exist yet):
   - references/style-guide.md
   - references/approved-examples.md
   {{- additional reference files (brand voice, ICP, format guides)}}
1. Parse the request: {{what to extract}}.
2. {{Gather step — search, read files, call tools}}.
3. {{Transform/format step}}.
4. Present 2-3 distinct variations and let the user pick or mix. Never deliver a single take-it-or-leave-it output.

## Output

- Always multiple variations (minimum 2, maximum 3), labeled by angle/style.
- Human-in-the-loop: wait for the user's choice before finalizing.
- {{Formatting constraints from reference files}}.

## Self-Learning Rule (non-negotiable)

If the user approves a final output:
1. Append the approved output plus the request that produced it to `references/approved-examples.md` (date-stamped).
2. Add one line to the Rules section below capturing what worked.
Read approved examples before every generation and bias toward patterns found there.

## Rules

- {{Hard constraints — tone, forbidden phrases, required sections}}.
{{- learned rules accumulate here}}
```
