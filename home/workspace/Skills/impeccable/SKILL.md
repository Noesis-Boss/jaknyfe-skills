---
name: impeccable
description: Browser-side DOM helpers for Impeccable live mode.  Kept separate from live-browser.js so future browser script parts can share chrome mounting, lookup, focus, and picker helpers without depending on the full overlay UI bundle.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  restored: 2026-08-30
---

# impeccable

## Overview

Browser-side DOM helpers for Impeccable live mode.  Kept separate from live-browser.js so future browser script parts can share chrome mounting, lookup, focus, and picker helpers without depending on the full overlay UI bundle.

## Usage

This skill was restored from backup. The original documentation is unavailable.

### Scripts

- `live-browser-dom.js`
- `live-browser-session.js`
- `live-browser.js`
- `modern-screenshot.umd.js`

## Files

```
impeccable/
  reference/
    adapt.md
    adapt.native.md
    android.md
    animate.md
    audit.md
    audit.native.md
    bolder.md
    brand.md
    clarify.md
    codex.md
    colorize.md
    craft.md
    critique.md
    delight.md
    distill.md
    document.md
    extract.md
    harden.md
    hooks.md
    init.md
    ... (12 more files)
  scripts/
    command-metadata.json
    context-signals.mjs
    context.mjs
    critique-storage.mjs
    detect-csp.mjs
    detect.mjs
    hook-admin.mjs
    hook-before-edit.mjs
    hook-lib.mjs
    hook.mjs
    live-accept.mjs
    live-browser-dom.js
    live-browser-session.js
    live-browser.js
    live-commit-manual-edits.mjs
    live-complete.mjs
    live-copy-edit-agent.mjs
    live-discard-manual-edits.mjs
    live-inject.mjs
    live-insert.mjs
    ... (11 more files)
    detector/
      design-system.mjs
      detect-antipatterns-browser.js
      detect-antipatterns.mjs
      findings.mjs
      browser/
        injected/
          index.mjs
      rules/
        checks.mjs
      cli/
        main.mjs
      registry/
        antipatterns.mjs
      node/
        file-system.mjs
      engines/
        regex/
          detect-text.mjs
        visual/
          screenshot-contrast.mjs
        browser/
          detect-url.mjs
        static-html/
          css-cascade.mjs
          detect-html.mjs
      shared/
        color.mjs
        constants.mjs
        fonts.mjs
        inline-ignores.mjs
        page.mjs
      profile/
        profiler.mjs
    lib/
      design-parser.mjs
      impeccable-config.mjs
      impeccable-paths.mjs
      is-generated.mjs
      provider.mjs
      target-args.mjs
    live/
      browser-script-parts.mjs
      completion.mjs
      event-validation.mjs
      insert-ui.mjs
      manual-apply.mjs
      manual-edit-routes.mjs
      manual-edits-buffer.mjs
      session-store.mjs
      svelte-component.mjs
      sveltekit-adapter.mjs
      ui-core.mjs
      vocabulary.mjs
```
