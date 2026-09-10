"""Load an X cookie file into the agent-browser session.

Accepts Netscape-format or JSON (list of cookie dicts / {cookies:[...]}).
agent-browser has no --curl flag, so we set cookies one by one.
"""
import json
import shlex
import subprocess
import sys


def _ab(*args):
    return subprocess.run(
        [sys.executable, "-c", "pass"],
        capture_output=True, text=True,
    ) if False else subprocess.run(
        ["agent-browser", *args], capture_output=True, text=True, timeout=60
    )


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
        if not line or line.startswith("# ") or line.startswith("# Netscape") or line.startswith("#"):
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


def load(path):
    cookies = parse(path)
    if not cookies:
        return False, "no cookies parsed"
    errs = []
    for c in cookies:
        arg = (
            f'{json.dumps(c["name"])} {json.dumps(c["value"])} '
            f'--domain {shlex.quote(c["domain"])} --path {shlex.quote(c["path"])}'
            + (" --secure" if c["secure"] else "")
            + (" --http-only" if c["httpOnly"] else "")
            + (f" --expires {c['expires']}" if c["expires"] else "")
        )
        r = _ab("cookies", "set", *shlex.split(arg))
        if r.returncode != 0:
            errs.append(f'{c["name"]}: {r.stderr.strip() or r.stdout.strip()}')
    ok = not errs
    return ok, "; ".join(errs)


if __name__ == "__main__":
    ok, msg = load(sys.argv[1])
    print(json.dumps({"ok": ok, "error": msg} if not ok else {"ok": True}))
    sys.exit(0 if ok else 1)
