# Tailscale Setup

## Problem
Tailscaled fails to run in container due to missing TUN kernel module.

## Solution
- Uses userspace networking mode: `-tun userspace-networking`
- Registered as process service `svc_F2cgJQCFxWQ`
- Auto-restarts on failure via Zo supervisor

## Task Worker Improvements
- `/api/tailscale/health` endpoint added for health checks
- Check Tailscale before task polling (every 10s)
- Auto-restart tailscaled service via API on failure
- Log downtime and trigger alerts if > 30s