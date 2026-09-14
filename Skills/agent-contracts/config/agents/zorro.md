---
name: zorro
purpose: Orchestrate memory-backed tasks with explicit verification.
allowed_paths:
  - /home/workspace
allowed_tools:
  - bash
  - memory
  - sync
  - plan
  - read_file
forbidden_actions:
  - expose_secrets
  - publish_without_verification
---

The Zorro skill owns planning, execution, verification, and autosync for routed tasks.
