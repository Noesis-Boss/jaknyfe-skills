---
name: shadcn-best-practices
description: Use when working with shadcn/ui in a Zo project — components.json present, or the task mentions shadcn init, shadcn add, a component registry, a --preset code, or customizing shadcn theme tokens. Covers CLI usage (init/add/search/view/docs/info/build), component composition, base-ui vs Radix, forms, icons, and styling rules.
compatibility: Created for Zo Computer. Bundled body is vendored from openai/plugins (build-web-apps), which ships no LICENSE — do not redistribute.
metadata:
  author: jaknyfe.zo.computer
---

# shadcn/ui best practices (Zo)

Full upstream guidance is vendored read-only at `plugin/`. Read the file that matches the task, then act. Do not guess flags — the CLI reference explicitly warns that undocumented flags do not exist.

## Routing

| Task | Read |
| --- | --- |
| init, add, search, view, docs, info, build, presets | `plugin/cli.md` |
| Choosing between Base UI and Radix | `plugin/rules/base-vs-radix.md` |
| Building a new component on top of existing ones | `plugin/rules/composition.md` |
| React Hook Form + zod wiring, field components | `plugin/rules/forms.md` |
| Icon library choice inside a shadcn project | `plugin/rules/icons.md` |
| Theme tokens, `cn()`, Tailwind v4 setup | `plugin/rules/styling.md` |
| Theming a project by hand rather than via the CLI | `plugin/customization.md` |
| MCP server integration for registries | `plugin/mcp.md` |

`plugin/SKILL.md` is the upstream entry point and is kept intact for provenance. It is not a separate skill — do not treat it as one.

## Rules that matter on this host

1. **No inline shell execution.** Zo does not expand `` !`cmd` `` directives. Upstream's "Current Project Context" block was rewritten to a plain `bash` block you run yourself. Never re-add a backtick-exec directive.
2. **Use the project's package runner.** Bun projects: `bunx --bun shadcn@latest`. npm: `npx shadcn@latest`. pnpm: `pnpm dlx shadcn@latest`. The CLI auto-detects from the lockfile; there is no `--package-manager` flag.
3. **Do not install into zo.space routes.** `bun add` / `shadcn add` break space route syncs. For a Space, either use the installed package set or pin via `esm.sh`; for real dependencies, use a Zo Site.
4. **Token edits beat hand-written CSS.** If the project has `src/theme.json`, that file is the source of truth for light/dark shadcn tokens — edit it, don't hand-edit CSS custom properties.
5. **Network calls are user-initiated only.** Every shadcn command hits the npm registry. Run it because the current task needs it, never on skill load, and never in a loop.

## Provenance and license

Vendored from `openai/plugins` → `plugins/build-web-apps/skills/shadcn-best-practices`. That repo ships **no LICENSE file**, and this bundle's `plugin/` directory is gitignored in `jaknyfe-skills` as a result. Use locally; do not fork, mirror, or publish it.
