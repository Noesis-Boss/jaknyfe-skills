# VoxWerx

VoxWerx improves clarity, voice, factual fidelity, continuity, and publication readiness. It does not determine authorship or optimize text to evade AI detectors.

Brand: [voxwerx.com](https://voxwerx.com)

## Install

Copy this directory into the host's skills directory as `voxwerx`, then invoke it by its skill name: `voxwerx`.

## Verification

Run the regression suite from the workspace root:

```bash
python3 Skills/voxwerx/fixtures/run_fixtures.py
```

The fixture suite covers detector boundaries and visible-copy extraction from HTML and Markdown.
