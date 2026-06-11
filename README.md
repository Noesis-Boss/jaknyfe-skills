# jaknyfe-skills

My personal collection of agent skills for Zo Computer — the ones I wrote or forked and that aren't part of the upstream [zocomputer/skills](https://github.com/zocomputer/skills) registry.

25 skills, ~4.6 MB.

## Install

Each skill lives in `skills/<name>/` and follows the [Agent Skills spec](https://agentskills.io/specification). Drop a folder into your own `Skills/` directory on a Zo Computer.

```bash
# Example: install a single skill
cp -r skills/design-md ~/Skills/

# Or clone the whole repo and cherry-pick
git clone https://github.com/Noesis-Boss/jaknyfe-skills.git
```

## Skills

| Skill | What it does |
| --- | --- |
| caveman-code | Run the caveman-code CLI — token-saving coding agent with multi-provider auth |
| clarion-portfolio-monitor | Fetch live TastyTrade portfolio positions, balances, and daily transactions |
| content360 | Integrate with Content360 (app.content360.io) to create, schedule, and publish social media content |
| coverage-checker | Analyze test coverage and identify untested code |
| dead-code | Find dead/unused code with vulture, knip, and pyright |
| design-md | Create, validate, and manage DESIGN.md design system files for AI agents |
| error-analyzer | Analyze error logs and identify root causes |
| free-models-for-openclaw | Track free LLM models compatible with OpenClaw |
| gog | Google Workspace CLI operations |
| gumroad-product-builder | Build and launch Gumroad products |
| hatch-pet | Tamagotchi-style hatchable pet companion |
| huggingface-hub | Browse and use models, datasets, and spaces on Hugging Face Hub |
| ifixai | AI-powered device repair assistant |
| last30days | Research any topic across 30+ sources from the last 30 days |
| memory | Durable memory management using the four-layer memory model |
| migration-gen | Generate migration scripts between frameworks/formats |
| pr-summarizer | Summarize PRs and their impact |
| psych-tricks | Persuasion and psychology playbooks for marketing copy |
| romantasy-autonovel | Romantasy fiction generation and writing assistant |
| vibe-coding-assistant | Act as a Technical Co-Founder — Discovery → Planning → Building → Polish → Launch |
| x-twitter-by-altf1be | Post tweets to X (Twitter) API |
| zo-google-direct-oauth | Direct OAuth flow for Google APIs |
| zo-persona-creator | Create and manage Zo AI personas |
| zo-twitter | Twitter/X utilities for Zo automations |
| zobodhi-memory | Persistent memory store for the zobodhi system |

## Provenance

These are the skills in `~/Skills/` on my Zo Computer that did not appear in the [zocomputer/skills](https://github.com/zocomputer/skills) registry when this repo was generated. Some may still be forks or community contributions I haven't upstreamed — file an issue if something here shouldn't be.

## License

MIT, unless a specific skill declares otherwise in its folder.