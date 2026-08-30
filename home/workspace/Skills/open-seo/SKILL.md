---
name: open-seo
description: Use OpenSEO's MCP and bundled SEO workflows for keyword research, competitor analysis, SERP and backlink research, site audits, local SEO, rank tracking, and Search Console analysis. Trigger when the user asks for data-backed SEO research or wants to use OpenSEO.
metadata:
  author: jaknyfe.zo.computer
---

# OpenSEO

Use the OpenSEO MCP server at `https://app.openseo.so/mcp` for live SEO data. The hosted service requires OpenSEO authorization; API-key access is appropriate for headless use.

## Connection

If OpenSEO is not connected, tell the user to add the MCP endpoint in Zo's MCP integrations or configure it in the active Codex client. Do not invent or request a DataForSEO key unless the user chooses self-hosting. For API-key use, the user creates the key in OpenSEO Settings and stores it in Zo Settings → Advanced; never place secrets in this skill.

## Workflow selection

- Keyword discovery and metrics: `open-seo-keyword-research`
- Competitor domain: `open-seo-competitor-analysis`
- Market-wide competitor landscape: `open-seo-competitive-landscape`
- Keyword-to-page mapping: `open-seo-keyword-clustering`
- Link opportunities: `open-seo-link-prospecting`
- Local search: `open-seo-local-seo`
- Technical/content audit: `open-seo-seo-audit`
- Ongoing SEO guidance: `open-seo-seo-coach`
- New project setup: `open-seo-seo-project-setup`

## Guardrails

Use project context before paid research when available. Check recent research logs to avoid duplicate spend. Treat third-party estimates as estimates, distinguish Search Console first-party data from modeled data, and ask before saving keywords or changing project context.

Report the query set, filters, date range, source, and limitations. Do not claim rankings, traffic, or backlink facts without an OpenSEO result supporting them.
