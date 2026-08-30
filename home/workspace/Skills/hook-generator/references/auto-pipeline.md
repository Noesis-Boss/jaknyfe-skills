# Auto-pipeline integration

If you're wiring this skill into a bot/agent that auto-posts to X, generates article
intros, or fires off cold emails on a cron, the simplest contract is:

1. Generate the hooks however you like (this skill's instructions, a script call,
   or an LLM call against this SKILL.md).
2. Extract the recommended one.
3. Use it as the opener of the post/article/subject.

## Pattern A — from a script

```python
import subprocess, json, re, os

def get_recommended_hook(topic: str, surface: str = "x") -> str:
    out = subprocess.run(
        ["python3", "/home/workspace/Skills/hook-generator/scripts/generate_hooks.py",
         topic, "--surface", surface, "--json"],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    return data["recommendation"]["text"]
```

## Pattern B — from an LLM call (better)

For real quality, don't use the script's templated output. Pass the SKILL.md
into the LLM's system prompt and ask for hooks directly:

```
SYSTEM:  <contents of SKILL.md>
USER:    Topic: "<the post's topic>"
         Surface: x
         Audience: <one phrase>
         Goal: <share | click | agree | act>
         Produce 5 hooks + recommendation. No preamble, no commentary.
```

This gives you real, on-topic hooks instead of the templated stubs in the
script. The script is for non-LLM contexts (cron jobs, dry runs, schema
validation); the LLM call is for actual production copy.

## What to extract for auto-posting

From the LLM's response, pull:

- The line starting with `RECOMMENDED: #N` — that's your auto-posted opener.
- The line under `SECOND LINE:` — that's the follow-up sentence if the surface
  has room (X threads, LinkedIn, articles). For subjects, ignore it.

Strip the surrounding quotes and you're done.

## When to skip the skill

- The post is a reply / quote-tweet (the original post IS the hook).
- The user has already written the hook and just wants the body.
- The post is a one-shot breaking-news item (the news IS the hook).
