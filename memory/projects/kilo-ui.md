---
name: kilo-ui-project
description: Kilo TUI backend + React/Vite frontend deployed as a public Zo HTTP service
type: project
---

# Kilo UI

## Overview
`kilo` as a public Zo HTTP service with a React/Vite frontend (`kilo-ui`) that calls the `kilo` backend.

## Key Paths
- Frontend: `/home/workspace/kilo-ui/`
- Config: `kilo-ui/zosite.json`, `kilo-ui/vite.config.ts`
- Env: `kilo-ui/.env`, `kilo-ui/.env.production`
- API client: `kilo-ui/src/api/kilo.ts`
- UI: `kilo-ui/src/App.tsx`, `kilo-ui/src/main.tsx`

## Issue History
- Build/publishing issues (base paths, routing, `zosite.json`) — iteratively fixed
- Public URL obtained after correct configuration

## Status
Deployed. Public URL: https://kilo-jaknyfe.zocomputer.io/

## Note
Kilo and OpenCode output CLI to a master terminal. CLI web client display behavior needs verification — confirm it opens on the correct terminal.