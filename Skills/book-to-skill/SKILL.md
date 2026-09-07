---
name: book-to-skill
description: Extract text from a document file for book-to-skill processing.
Backward-compatible entrypoint wrapper.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  restored: 2026-08-30
---

# book-to-skill

## Overview

Extract text from a document file for book-to-skill processing.
Backward-compatible entrypoint wrapper.

## Usage

This skill was restored from backup. The original documentation is unavailable.

### Scripts

- `extract.py`

## Files

```
book-to-skill/
  scripts/
    banner.txt
    extract.py
  tests/
    test_book_to_skill.py
    test_discovery_tax.py
    test_html_block_boundaries.py
    test_metadata_encoding.py
    test_repo_hygiene.py
    test_rtf_destination_groups.py
    test_sanitize_bidi_controls.py
    test_sanitize_extracted_text.py
    test_scan_generated_skill.py
  .github/
    FUNDING.yml
    PULL_REQUEST_TEMPLATE.md
    dependabot.yml
    ISSUE_TEMPLATE/
      bug_report.md
      feature_request.md
    workflows/
      ci.yml
      codeql.yml
      deploy-docs.yml
  tools/
    discovery_tax.py
    scan_generated_skill.py
    validate_skill.py
  book_to_skill/
    __init__.py
    __main__.py
    cli.py
    config.py
    dependencies.py
    exceptions.py
    sanitize.py
    utils.py
    __pycache__/
      __init__.cpython-312.pyc
      cli.cpython-312.pyc
      config.cpython-312.pyc
      dependencies.cpython-312.pyc
      exceptions.cpython-312.pyc
      sanitize.cpython-312.pyc
      utils.cpython-312.pyc
    parsers/
      __init__.py
      calibre.py
      docx.py
      epub.py
      html.py
      pdf.py
      rtf.py
      text.py
      __pycache__/
        __init__.cpython-312.pyc
        calibre.cpython-312.pyc
        docx.cpython-312.pyc
        epub.cpython-312.pyc
        html.cpython-312.pyc
        pdf.cpython-312.pyc
        rtf.cpython-312.pyc
        text.cpython-312.pyc
  .git/
    HEAD
    config
    description
    index
    packed-refs
    shallow
    branches/
    objects/
      info/
      pack/
        pack-b6857a6f9486dc8c4d6fbe757b3ee2d974afaf3c.idx
        pack-b6857a6f9486dc8c4d6fbe757b3ee2d974afaf3c.pack
    info/
      exclude
    hooks/
      applypatch-msg.sample
      commit-msg.sample
      fsmonitor-watchman.sample
      post-update.sample
      pre-applypatch.sample
      pre-commit.sample
      pre-merge-commit.sample
      pre-push.sample
      pre-rebase.sample
      pre-receive.sample
      prepare-commit-msg.sample
      push-to-checkout.sample
      update.sample
    refs/
      heads/
        master
      tags/
      remotes/
        origin/
          HEAD
    logs/
      HEAD
      refs/
        remotes/
          origin/
            HEAD
        heads/
          master
  overrides/
    main.html
  docs/
    404.md
    CNAME
    architecture.md
    faq.md
    how-it-works.md
    index.md
    install.md
    performance.md
    robots.txt
    usage.md
    assets/
      banner.webp
      booklin-casting.png
      booklin-celebrating.png
      booklin-confused.png
      booklin.png
      logo.png
      og-card.jpg
```
