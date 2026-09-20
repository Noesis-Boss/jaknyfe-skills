---
name: presenton
description: Use Presenton to generate editable PowerPoint presentations, PDFs, and slide images from frontend applications, agent workflows, Markdown, documents, or structured content. Trigger whenever a task asks to add presentation generation, export a report to PPTX/PDF, connect an app to Presenton, or build a presentation workflow.
compatibility: Requires a reachable Presenton self-hosted instance or Presenton API and curl. Keep API credentials in environment variables.
metadata:
  author: jaknyfe.zo.computer
---

# Presenton

Presenton is an open-source presentation generator and API. Use it as a separate presentation service; do not copy its application into the consuming frontend.

## Integration rules

1. Read the consuming project's `README.md`, `AGENTS.md`, and `DESIGN.md` before changing frontend code.
2. Use `PRESENTON_URL` for the base URL and `PRESENTON_API_KEY` for the bearer token. Never hardcode credentials or place them in browser bundles.
3. Call Presenton from a server-side route, backend action, or trusted worker. A browser must not call the Presenton API directly when that would expose credentials.
4. Validate the response, save generated files outside the public web root, and expose downloads through an authenticated or signed route.
5. Pin the Presenton image or service version in deployment configuration. Avoid `latest` for production.
6. Keep MCP access bound to localhost or behind authentication. Treat uploaded documents and generated decks as sensitive data.

## API workflow

Use `scripts/presenton.ts` for a repeatable request. It accepts Markdown or plain text, requests a PPTX export by default, and prints the resulting JSON. Set `PRESENTON_URL` and `PRESENTON_API_KEY` in the environment before running it.

```bash
bun run Skills/presenton/scripts/presenton.ts --content report.md --slides 8 --output pptx
```

The exact API contract can vary by Presenton release. If the request fails with a schema or authentication error, inspect the running instance's OpenAPI documentation and update the request fields for that pinned version rather than guessing.

## Frontend pattern

The frontend submits a job to its own backend. The backend validates input size and file type, calls Presenton, stores the result, and returns a job or download identifier. Show progress and a clear failure state. Verify the downloaded PPTX opens and contains the expected slide count before marking the feature complete.

## Quality gate

For every integration, test authentication failure, provider failure, oversized input, successful PPTX generation, and PDF or PNG export when those formats are exposed. Visually inspect at least one rendered deck; successful HTTP status alone is insufficient.

