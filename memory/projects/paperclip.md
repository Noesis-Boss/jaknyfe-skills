---
name: paperclip-project
description: Paperclip — hosted AI service on Zo Computer with Postgres backend and Hermes/OpenClaw integration
type: project
---

# Paperclip

## Overview
AI service hosted on Zo Computer. Has been restored and configured after service runtime failures tied to Postgres connectivity.

## Key Paths
- Config: `/root/.paperclip/instances/default/config.json`
- Start script: `/home/workspace/paperclip/start-server.sh`
- Source: `/home/workspace/paperclip/packages/mcp-server/` and `/home/workspace/paperclip/server/src/`

## Issues Resolved
- Postgres connectivity causing service failures
- Service entrypoint and supervisor configuration tuned
- Model/provider configuration through Hermes/OpenClaw workflows

## Verification
Health check at `/api/health` endpoint. Service proxying when hosting breaks.

## Status
Operational. Monitor for Postgres connectivity issues.