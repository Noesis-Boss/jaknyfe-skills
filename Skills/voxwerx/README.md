# Voxwerx

Voxwerx is the workspace writing-quality skill for removing AI-patterns while preserving the writer's facts, voice, and judgment.

Brand: [voxwerx.com](https://voxwerx.com)

## Install

Copy this directory into the host's skills directory as `voxwerx`, then invoke it by its skill name: `voxwerx`.

## Verification

Run the regression suite from the workspace root:

```bash
python3 Skills/voxwerx/fixtures/run_fixtures.py
```

The fixture suite covers detector boundaries and visible-copy extraction from HTML and Markdown.
