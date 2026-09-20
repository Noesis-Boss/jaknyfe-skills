# Secret scanning policy

This repository uses Gitleaks in two places:

- The global Git `pre-push` hook scans every outgoing commit before Git contacts the remote.
- GitHub Actions scans the complete repository history on every push and pull request.

## False positives

Do not bypass a finding casually. First confirm that the value is not a live credential, remove or rotate it if necessary, and check the relevant commit history.

For a confirmed non-secret fixture or historical false positive, add the narrowest possible entry to `.gitleaksignore`. Prefer a specific fingerprint or path and rule combination. Do not disable a detector globally.

Document why the entry is safe in the commit message or an adjacent security note. Never use `git push --no-verify` to bypass a suspected real secret.

## If a real secret is found

Stop the push, revoke or rotate the credential, remove it from the working tree, and purge it from Git history when it was committed. Treat a secret that was pushed as compromised even if the repository is private.
