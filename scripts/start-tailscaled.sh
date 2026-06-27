#!/bin/bash
pkill tailscaled 2>/dev/null || true
tailscaled -statedir /var/lib/tailscale -socket /var/run/tailscale/tailscaled.sock -tun userspace-networking &
sleep 2
tailscale up --accept-routes
