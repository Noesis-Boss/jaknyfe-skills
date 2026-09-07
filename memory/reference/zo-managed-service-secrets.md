---
name: zo-managed-service-secrets
description: Reliable secret loading for Zo managed services
type: reference
---

Zo managed-service `env_vars` values are passed literally. They do not expand `$NAME` references and do not automatically read Settings secrets. For any service needing Zo secrets, use an entrypoint such as `bash -c 'source ~/.zo_secrets 2>/dev/null; exec <command>'`, and remove secret `$NAME` entries from the service `env_vars` so the sourced values are authoritative. Restart and verify with `service_doctor`; inspect logs without printing secret values.
