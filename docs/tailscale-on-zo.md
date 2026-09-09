# Install Tailscale on a Zo Computer Sandbox

Zo sandboxes run under gVisor with **no `/dev/net/tun`**, so the standard Tailscale install won't work as a system daemon. The fix: run `tailscaled` in **userspace-networking mode** and register it with Zo's user-supervisor so it survives reboots.

Works on: Zo Computer sandbox (Debian, root, gVisor). Verified with Tailscale 1.98.2 (2026-09).

**Persistence:** register tailscaled as a **Zo user service** (Websites → Services), not a supervisor config edit — Zo regenerates `/etc/zo/supervisord-user.conf` on each boot, so hand edits there are lost. A registered user service survives restarts.

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

## 3. Make it persistent: register a Zo user service

**Do not edit `/etc/zo/supervisord-user.conf` by hand** — Zo regenerates that file on every boot and your block disappears. Register tailscaled as a managed user service instead. It's supervised (auto-restart on crash), auto-starts on boot, persists across restarts, and `mode=process` doesn't count against your public service slots.

Register it (ask Zo in chat, or use the Services page):

- **Label:** `tailscale`
- **Mode:** `process` (no public endpoint — omit the port)
- **Entrypoint:**

```bash
bash -c 'tailscaled -statedir /var/lib/tailscale -socket /var/run/tailscale/tailscaled.sock -tun userspace-networking & sleep 2 && tailscale up --accept-routes; exec sleep infinity'
```

Or the one-shot equivalent:

```text
register_user_service(
  label="tailscale",
  mode="process",
  entrypoint="bash -c 'tailscaled -statedir /var/lib/tailscale -socket /var/run/tailscale/tailscaled.sock -tun userspace-networking & sleep 2 && tailscale up --accept-routes; exec sleep infinity'"
)
```

Notes:

- The `bash -c '... & sleep 2 && tailscale up; exec sleep infinity'` wrapper keeps both the daemon and the `tailscale up` state alive in one supervised process. Without it, the supervisor thinks the daemon exited.
- If you already logged in (step 2), `tailscale up` re-joins silently using saved state.
- Replace `--accept-routes` with your own flags if needed.
- Logs land in `/dev/shm/tailscale.log` (stdout) and `/dev/shm/tailscale_err.log` (stderr), and are indexed by the built-in Loki instance.

## 4. Verify

```bash
tailscale status        # BackendState: Running, your node + peers listed
tailscale ip            # should print your 100.x.y.z address
tail /dev/shm/tailscale.log   # service log — should show tailscaled startup
```

The `tailscale` service should show as running on the Services page too.

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
| Node shows offline after sandbox reboot | Service not running. Check the Services page — restart `tailscale` if stopped, and check `/dev/shm/tailscale_err.log`. |
| `tailscale up` asks to authenticate again | State dir got wiped (`/var/lib/tailscale`). Log in again; consider `--authkey` from a reusable key for unattended recovery. |
| No outbound connectivity through tailnet | Userspace mode has no kernel routing. Reach other nodes by their 100.x IPs or MagicDNS names; for subnet routing use `tailscale up --accept-routes` and SOCKS/HTTP proxies via `tailscale serve`/`nc`-style proxies. |
| Logs | `tail -f /dev/shm/tailscale.log /dev/shm/tailscale_err.log` |

## Gotchas

- **Don't install via apt on this platform** — the apt package assumes systemd + TUN.
- **Userspace networking means no transparent subnet routing** — this node reaches tailnet nodes by IP/DNS, but other LANs can't route *through* it like a normal exit node unless you use the userspace SOCKS5 proxy (`--outbound-http-proxy-listen`).
- **Don't hand-edit `/etc/zo/supervisord-user.conf`** — Zo regenerates it on every boot. Use a registered user service for persistence.
