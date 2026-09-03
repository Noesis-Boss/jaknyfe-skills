# Zo Support Bug Report: Managed-Service Secret References Are Not Expanded

## Summary

Zo managed services do not expand environment-variable references in `env_vars`. A service configured with a value such as `$CREDENTIAL_ENCRYPTION_KEY` receives that literal string instead of the secret's value.

## Affected service

- Service: `saas-mailer-worker`
- Service ID: `svc_DJ86bGpettQ`
- Mode: private process worker
- Impacted setting: `CREDENTIAL_ENCRYPTION_KEY`

## Expected behavior

When a managed service environment variable is configured as `$CREDENTIAL_ENCRYPTION_KEY`, Zo should resolve the reference to the current secret value before starting the service, or clearly document that references are unsupported and reject the configuration during validation.

## Actual behavior

The managed service receives the literal text `$CREDENTIAL_ENCRYPTION_KEY`. The worker then fails startup because the value does not decode to the required 32-byte encryption key.

The main Zo shell has the correctly configured secret: present, 64 hexadecimal characters, representing 32 bytes. Re-saving the secret, restarting the service, disabling/enabling it, and recreating the service did not change the managed-service value.

## Reproduction

1. Add a valid secret named `CREDENTIAL_ENCRYPTION_KEY` in Zo Settings → Advanced.
2. Configure a managed process service with an environment variable whose value is `$CREDENTIAL_ENCRYPTION_KEY`.
3. Start or restart the service.
4. Observe that the application receives the literal reference rather than the secret value.

## Evidence

- The worker fails before normal application startup with the encryption-key validation error.
- The same key is valid in the main Zo shell.
- Full service restart and service recreation reproduce the failure.
- Other secret references, including `$DATABASE_URL`, show the same behavior.

## Security considerations

Please do not request or require the secret value in a support reply. The issue can be diagnosed using redacted metadata such as variable names, whether expansion occurred, and resolved value length/type.

## Requested resolution

Please either:

1. Fix managed-service `env_vars` expansion for secret references; or
2. Provide the supported mechanism for binding Zo secrets to managed services without exposing secret values in service definitions.

Also please clarify whether service environment variables are intended to support `$NAME` references and whether updates to Settings → Advanced automatically propagate to existing services.

## Workaround status

The service remains managed but cannot start safely until it receives the actual 32-byte key value or a supported secret-binding mechanism.
