# Contributing

## Canonical branch

`master` is the default and protected branch. Use it for pull requests and repository links.

## Before pushing

Run the relevant validation for the files you changed. Every push is checked by the global pre-push hook with Gitleaks, and pushes containing detected secrets are blocked. The repository also runs the `Gitleaks / scan` workflow on pushes and pull requests.

Never commit API keys, tokens, passwords, private keys, or `.env` files. Store local credentials in environment variables or Zo Settings > Advanced.

## Pull requests

Keep changes focused. Describe the behavior changed, validation performed, and any known limitations. Do not bypass the secret scan to force a push. If Gitleaks reports a confirmed false positive, document the exact fixture or path and update `.gitleaksignore` narrowly before opening the pull request.

## Review expectations

Review findings are advisory until validated against the code and tests. Keep deterministic checks such as tests, linters, dependency audits, and Gitleaks separate from AI-assisted review.
