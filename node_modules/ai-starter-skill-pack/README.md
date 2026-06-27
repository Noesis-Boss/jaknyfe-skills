# AI Starter Skill Pack

![AI Starter Skill Pack — five beginner-friendly AI Agent Skills for onboarding, prompt debugging, learning, project ideas, and career proof](https://raw.githubusercontent.com/Jeff-Kazzee/ai-starter-skill-pack/dev/assets/ai-starter-skill-pack-social.png)

Five small Agent Skills for getting unstuck, learning by doing, building useful proof, and making honest career progress with AI.

This is not an AI masterclass, a list of fifty tools, or a promise that prompt tricks will produce a job. It is a starter operating system for beginners who need a sensible next action.

## What is included

| Skill | Use it when someone needs | Main result |
|---|---|---|
| `ai-beginner-onboarding` | A calm place to start | A tiny tool stack, seven-day plan, first workflow, and practice project |
| `prompt-debugger` | Help fixing a prompt or model mismatch | A diagnosis, rewritten prompt, variants, and test cases |
| `personal-ai-tutor` | A realistic learning path | Milestones, practice, proof artifacts, and review checkpoints |
| `ai-project-idea` | A small project worth building | Ranked ideas, one scoped MVP, and a seven-day build plan |
| `no-bs-ai-career` | A path from learning to credible work proof | Honest claims, gap analysis, portfolio work, and a 30-day plan |

Recommended order:

1. Start with onboarding when the user is overwhelmed.
2. Use the tutor for sustained learning.
3. Use the prompt debugger whenever a specific interaction fails.
4. Use the project skill to turn learning into something visible.
5. Use the career skill to connect proof to work, freelancing, or workplace value.

The skills deliberately overlap at the handoff points, not at the center. Onboarding chooses a first step. The tutor teaches. The project skill scopes a build. The career skill evaluates evidence. The prompt debugger repairs one model interaction.

## Design choices

- Each `SKILL.md` is compact and procedural.
- Detailed methods live in `references/`.
- Reusable worksheets live in `assets/`.
- Trigger evals live in `tests/`.
- No scripts are included. These skills depend mainly on judgment and conversation; a deterministic script would add maintenance without improving the core work.
- Critical safety and boundary rules are repeated inside each skill so an individual skill remains usable when installed alone.
- Shared references are for maintainers and runtimes that expose the whole pack. An individual skill does not depend on cross-directory access.

## Beginner-safe defaults

Unless the user says otherwise, the skills:

- Prefer one general-purpose AI assistant the user can already access.
- Avoid paid APIs, complex agents, and multi-tool automation as a first step.
- Work with 20–30 minutes a day and provide a low-energy fallback.
- Use sample or redacted data before real personal, client, school, or employer data.
- Separate model output from verified fact.
- Prefer a small completed artifact over a giant unfinished curriculum.
- Treat accessibility, fatigue, device limits, budget, and inconsistent schedules as design constraints rather than character flaws.

## Generic installation

A compatible Agent Skills runtime generally expects one folder per skill with a `SKILL.md` file at its root. Copy the desired folder from `skills/` into the runtime's recognized skills directory or import it through the runtime's Skills interface. Preserve the files inside that skill folder.

The pack is also installable as an npm-compatible data package directly from GitHub:

```sh
npm install github:Jeff-Kazzee/ai-starter-skill-pack
```

Package installs expose the skill folders under `node_modules/ai-starter-skill-pack/skills/` and the shared material under `node_modules/ai-starter-skill-pack/shared/`. The package allowlist only ships `skills/` and `shared/` plus normal package metadata.

The open Agent Skills specification defines `SKILL.md` plus optional `references/`, `assets/`, and `scripts/`, but exact discovery paths and interfaces are runtime-specific and can change:

- **Codex:** current documentation lists repository skills under `.agents/skills/` and user skills under `$HOME/.agents/skills/`.
- **Claude Code:** current documentation lists project skills under `.claude/skills/` and personal skills under `~/.claude/skills/`.
- **OpenAI API:** current documentation supports versioned skill bundles uploaded for use with supported tool runtimes. Follow the current API guide rather than hard-coding an endpoint from this repository.
- **Zo Computer:** Zo publicly describes support for the industry-standard Skill format, but the exact import interface and placement should be checked in its current Skills UI or documentation.
- **ChatGPT and other assistants:** a product may not expose a generic folder-based skill loader. Pasting a `SKILL.md` into project instructions can approximate its behavior, but that is not identical to native skill discovery, resource loading, or trigger routing.

See the current official documentation before deploying:

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills best practices: https://agentskills.io/skill-creation/best-practices
- Codex skills: https://developers.openai.com/codex/skills
- OpenAI API skills: https://developers.openai.com/api/docs/guides/tools-skills
- Claude Code skills: https://code.claude.com/docs/en/skills
- Zo Skills: https://www.zo.computer/skills

## Using the pack

Ask naturally. Native skill runtimes should select a skill from its description. Many runtimes also support explicit invocation; syntax varies.

Examples:

```text
I want to get into AI, but I am overwhelmed and only have twenty minutes a day.
```

```text
Fix this prompt for Claude. It keeps returning a generic essay instead of a table.
```

```text
Teach me enough AI automation to improve one process at my small business.
```

```text
Give me a portfolio project I can finish without paying for APIs.
```

```text
What can I honestly say about AI on my resume right now?
```

A good result should be useful even when the user answers only part of the intake. The skills use clearly labeled assumptions rather than turning the interaction into an interview.

## Testing

Each skill contains:

- `tests/eval_queries.json` with positive, negative, implicit, and boundary cases.
- `tests/README.md` with a simple manual evaluation method.

Test discovery separately from output quality. A skill can produce excellent output after explicit invocation and still have a weak description that does not trigger reliably.

## Privacy and current information

Do not paste secrets or unredacted sensitive records into an AI product merely because a skill asks for context. Use placeholders, synthetic examples, or the minimum necessary excerpt.

Product capabilities, data controls, model behavior, labor-market conditions, and installation steps change quickly. The skills require fresh verification when a recommendation depends on current facts. The research snapshot in this release was reviewed on **2026-06-23**.

## Repository map

```text
skills/   Individual installable skills
shared/   Pack-wide references and reusable worksheets
```

## License

MIT. See `LICENSE`.
