---
name: skill
purpose: Execute one repeatable workflow inside its declared scope.
allowed_paths:
  - /home/workspace/Skills
allowed_tools:
  - bash
  - read_file
  - write_file
forbidden_actions:
  - access_undeclared_projects
  - send_external_messages
---

Skills may write only declared outputs and must record verification results.
