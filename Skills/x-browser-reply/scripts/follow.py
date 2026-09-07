#!/usr/bin/env python3
"""Follow an X user via browser automation (agent-browser), NOT the X API.

Usage:
  python3 follow.py --username NAME [--cookies /path/cookies.json] [--restore x-main]

Opens the profile, clicks the Follow button (skips safely if already
following / pending). Exit 2 = not logged in.
"""
import argparse, json, subprocess, sys, time

AB = "agent-browser"
SKIP = ("jak_nyfe", "zdsentry")


def ab(*args, timeout=120):
    r = subprocess.run([AB, *args], capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def js(expr, timeout=60):
    return ab("eval", expr, timeout=timeout)[1]


def logged_in():
    expr = """(() => {
  if (location.pathname.startsWith('/login') || location.pathname.startsWith('/i/flow')) return 'LOGINWALL';
  if (document.querySelector('a[data-testid="loginButton"]')) return 'LOGINWALL';
  if (document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"], a[data-testid="AppTabBar_Profile_Link"]')) return 'OK';
  return 'UNKNOWN';
})()"""
    for _ in range(3):
        out = js(expr)
        if out in ("OK", "LOGINWALL"):
            return out == "OK"
        time.sleep(3)
    return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--username", required=True)
    p.add_argument("--cookies", default="")
    p.add_argument("--restore", default="x-main")
    a = p.parse_args()

    user = a.username.strip().lstrip("@")
    if not user or "/" in user:
        print(json.dumps({"error": f"invalid username: {a.username!r}"}))
        sys.exit(1)
    if user.lower() in SKIP:
        print(json.dumps({"error": f"skipping own account @{user}"}))
        sys.exit(1)

    if a.cookies:
        rc, out, err = ab("cookies", "set", "--curl", a.cookies, "--domain", "x.com", timeout=30)
        if rc != 0:
            print(json.dumps({"error": f"cookie load failed: {err or out}"}))
            sys.exit(2)

    rc, _, err = ab("open", f"https://x.com/{user}", timeout=120)
    if rc != 0:
        print(json.dumps({"error": f"navigation failed: {err}"}))
        sys.exit(1)
    time.sleep(6)

    if not logged_in():
        print(json.dumps({"error": "not logged in to x.com (cookies/session expired)"}))
        sys.exit(2)

    # Detect account state
    state = js("""(() => {
  if (document.querySelector('[data-testid=\"emptyState\"]')) return 'NOTFOUND';
  const b = document.querySelector('[data-testid=\"follow\"], [data-testid=\"unfollow\"], [data-testid=\"pending\"]');
  if (!b) return 'NOBTN';
  if (b.dataset.testid === 'pending') return 'PENDING';
  return b.dataset.testid; // 'follow' or 'unfollow'
})()""")

    if state == "NOTFOUND":
        print(json.dumps({"error": f"profile not found: @{user}"}))
        sys.exit(1)
    if state in ("unfollow", "PENDING"):
        print(json.dumps({"ok": True, "username": user, "result": "already following" if state == "unfollow" else "already pending"}))
        sys.exit(0)
    if state != "follow":
        print(json.dumps({"error": f"follow button not found (state={state})"}))
        sys.exit(1)

    rc, out, err = ab("click", '[data-testid="follow"]', timeout=30)
    if rc != 0:
        print(json.dumps({"error": f"click failed: {err or out}"}))
        sys.exit(1)
    time.sleep(4)

    # Confirm confirm-dialog if present, then verify flip
    ab("click", '[data-testid="confirmationSheetConfirm"]', timeout=15)
    time.sleep(2)

    after = js("""(() => {
  const b = document.querySelector('[data-testid=\"follow\"], [data-testid=\"unfollow\"], [data-testid=\"pending\"]');
  return b ? b.dataset.testid : 'NOBTN';
})()""")
    if after in ("unfollow", "pending"):
        print(json.dumps({"ok": True, "username": user, "result": "followed"}))
        sys.exit(0)

    print(json.dumps({"error": f"follow not verified (state={after})"}))
    sys.exit(1)


if __name__ == "__main__":
    main()
