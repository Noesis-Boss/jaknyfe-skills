---
name: automation
purpose: Run a scheduled workflow with observable status and bounded side effects.
allowed_paths:
  - /home/workspace
allowed_tools:
  - bash
  - read_file
forbidden_actions:
  - trade_real_money
  - publish_without_verification
---

Automations must log start, meaningful tool events, failures, and final artifacts.
