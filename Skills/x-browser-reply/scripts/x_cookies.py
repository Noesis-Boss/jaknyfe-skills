"""Load an X cookie file into the agent-browser session.

Accepts Netscape-format or JSON (list of cookie dicts / {cookies:[...]}).
agent-browser has no --curl flag, so we set cookies one by one.

Robustness: individual `cookies set` calls can hang when the browser daemon
is busy. On TimeoutExpired we restart the daemon and retry the whole batch
once, so a transient stall never aborts the run.
"""
import json
import shlex
import subprocess
import sys
import time

SET_TIMEOUT = 25


def _ab(*args, timeout=SET_TIMEOUT):
    return subprocess.run(
        ["agent-browser", *args], capture_output=True, text=True, timeout=timeout
    )


def restart_daemon():
    """Best-effort daemon restart so a stuck CDP socket unblocks."""
    subprocess.run(["agent-browser", "close", "--all"],
                   capture_output=True, text=True, timeout=20)
    time.sleep(3)
    # warm up: a trivial eval proves the daemon is back
    for _ in range(5):
        r = subprocess.run(["agent-browser", "eval", "1"],
                           capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            return True
        time.sleep(3)
    return False


def parse(path):
    text = open(path).read().strip()
    if text.startswith(("[", "{")):
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("cookies", [])
        out = []
        for c in data:
            out.append({
                "name": c.get("name"),
                "value": c.get("value"),
                "domain": c.get("domain", ".x.com"),
                "path": c.get("path", "/"),
                "secure": bool(c.get("secure", True)),
                "httpOnly": bool(c.get("httpOnly", False)),
                "expires": int(c.get("expires", 0) or 0),
            })
        return [c for c in out if c["name"]]
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 7:
            continue
        dom, _, p, sec, exp, name, val = parts
        out.append({
            "name": name, "value": val, "domain": dom, "path": p,
            "secure": sec.upper() == "TRUE", "httpOnly": False,
            "expires": int(exp) if exp.isdigit() else 0,
        })
    return out


def load(path, retries=2):
    cookies = parse(path)
    if not cookies:
        return False, "no cookies parsed"

    attempt = 0
    while True:
        attempt += 1
        errs = []
        for c in cookies:
            arg = (
                f'{json.dumps(c["name"])} {json.dumps(c["value"])} '
                f'--url https://x.com'
                + (f" --domain {shlex.quote(c['domain'])}" if c["domain"] else "")
                + (f" --path {shlex.quote(c['path'])}" if c["path"] else "")
                + (" --secure" if c["secure"] else "")
                + (" --http-only" if c["httpOnly"] else "")
                + (f" --expires {c['expires']}" if c["expires"] else "")
            )
            try:
                r = _ab("cookies", "set", *shlex.split(arg))
            except subprocess.TimeoutExpired:
                errs.append(f'{c["name"]}: timed out after {SET_TIMEOUT}s')
                continue
            if r.returncode != 0:
                errs.append(f'{c["name"]}: {r.stderr.strip() or r.stdout.strip()}')

        if not errs:
            return True, ""
        if attempt > retries:
            return False, "; ".join(errs)
        # daemon stalled — restart and retry the whole batch
        restart_daemon()


if __name__ == "__main__":
    ok, msg = load(sys.argv[1])
    print(json.dumps({"ok": ok, "error": msg} if not ok else {"ok": True}))
    sys.exit(0 if ok else 1)