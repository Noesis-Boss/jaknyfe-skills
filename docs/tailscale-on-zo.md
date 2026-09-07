# Install Tailscale on a Zo Computer Sandbox

Zo sandboxes run under gVisor with **no `/dev/net/tun`**, so the standard Tailscale install won't work as a system daemon. The fix: run `tailscaled` in **userspace-networking mode** and register it with Zo's user-supervisor so it survives reboots.

Works on: Zo Computer sandbox (Debian, root, gVisor). Verified with Tailscale 1.98.2 (2026-09).

---

## 1. Install Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

Do **not** run `systemctl enable tailscaled` — there is no systemd here. It will fail.

## 2. Log in (first time only)

```bash
tailscaled -tun userspace-networking -statedir /var/lib/tailscale &
sleep 2
tailscale up --accept-routes
```

- `--accept-routes` pulls subnet routes advertised by your other nodes (optional, drop if unwanted).
- This prints a login URL. Open it, approve the node, name it (e.g. `zoltan`).
- State persists in `/var/lib/tailscale`, so login is one-time — after reboot the node rejoins automatically.

**No authkey?** Log in to your tailnet normally via the browser URL. **Have an authkey?** Use `tailscale up --authkey=<KEY> --accept-routes` instead (non-interactive, good for scripts).

## 3. Make it persistent via Zo's supervisor

Zo runs a user-supervisor at `/etc/zo/supervisord-user.conf`. Append this block:

```ini
[program:tailscaled]
command=bash -c 'tailscaled -statedir /var/lib/tailscale -socket /var/run/tailscale/tailscaled.sock -tun userspace-networking & sleep 2 && tailscale up --accept-routes; exec sleep infinity'
directory=/home/workspace
environment=
autostart=true
autorestart=true
stopsignal=TERM
stopasgroup=true
stdout_logfile=/dev/shm/tailscaled.log
stderr_logfile=/dev/shm/tailscaled_err.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=5
killasgroup=true
stopwaitsecs=4
```

Notes:

- The `bash -c '... & sleep 2 && tailscale up; exec sleep infinity'` wrapper keeps both the daemon and the `tailscale up` state alive in one supervised process. Without it, supervisor thinks the daemon exited.
- If you already logged in (step 2), `tailscale up` re-joins silently using saved state.
- Replace `--accept-routes` with your own flags if needed.

Then reload the supervisor so it picks up the block:

```bash
supervisorctl -c /etc/zo/supervisord-user.conf reread
supervisorctl -c /etc/zo/supervisord-user.conf update
```

Or, on the next full sandbox reboot, it auto-starts.

## 4. Verify

```bash
tailscale status        # BackendState: Running, your node + peers listed
tailscale ip            # should print your 100.x.y.z address
supervisorctl -c /etc/zo/supervisord-user.conf status   # tailscaled should be RUNNING
```

End-to-end check (from another node on your tailnet, e.g. a laptop also running Tailscale):

```bash
tailscale ping zoltan
```

If the sandbox reboots, confirm it came back:

```bash
tailscale status && echo OK
```

---

## Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `tailscaled cannot open /dev/net/tun` or `operation not permitted` | You're not using `-tun userspace-networking`. Add that flag. |
| Node shows offline after sandbox reboot | Supervisor block missing or not reloaded. Recheck `/etc/zo/supervisord-user.conf` and run `reread`/`update`. |
| `tailscale up` asks to authenticate again | State dir got wiped (`/var/lib/tailscale`). Log in again; consider `--authkey` from a reusable key for unattended recovery. |
| No outbound connectivity through tailnet | Userspace mode has no kernel routing. Reach other nodes by their 100.x IPs or MagicDNS names; for subnet routing use `tailscale up --accept-routes` and SOCKS/HTTP proxies via `tailscale serve`/`nc`-style proxies. |
| Logs | `tail -f /dev/shm/tailscaled.log /dev/shm/tailscaled_err.log` |

## Gotchas

- **Don't install via apt on this platform** — the apt package assumes systemd + TUN.
- **Userspace networking means no transparent subnet routing** — this node reaches tailnet nodes by IP/DNS, but other LANs can't route *through* it like a normal exit node unless you use the userspace SOCKS5 proxy (`--outbound-http-proxy-listen`).
- `/etc/zo/supervisord-user.conf` may be regenerated on platform updates — re-check the block after major Zo platform changes.
