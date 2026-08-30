#!/usr/bin/env python3
"""
setup.py — one-time Tuskcentral.ai sign-in.

Launches a Playwright Chromium, opens the chat page, and waits for you to
complete the Clerk sign-in. Once the chat interface loads, it saves the
storage state to ~/.tuskcentral/session.json and exits.

Usage:
  python3 setup.py [--headed] [--proxy URL] [--force]

If --headed is passed, the browser window is visible (useful if you want to
watch). Otherwise it runs headless.

--force: overwrite an existing session without prompting.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

sys.path.insert(0, str(Path(__file__).parent))
from tusk_lib import TUSK_DATA_DIR, TUSK_SESSION_FILE, TUSK_ORIGIN


def main() -> int:
    ap = argparse.ArgumentParser(description="Sign in to tuskcentral.ai (one-time).")
    ap.add_argument("--headed", action="store_true", help="Run Chromium with a visible window.")
    ap.add_argument("--proxy", default=None, help="Proxy URL (e.g. http://127.0.0.1:8888).")
    ap.add_argument("--url", default=f"{TUSK_ORIGIN}/?tusk_webview=1",
                    help="URL to open (default: webview chat).")
    ap.add_argument("--timeout", type=int, default=300,
                    help="Max seconds to wait for sign-in (default 300).")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing session without prompting.")
    args = ap.parse_args()

    TUSK_DATA_DIR.mkdir(parents=True, exist_ok=True)
    profile_dir = TUSK_DATA_DIR / "chromium-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)

    if TUSK_SESSION_FILE.exists() and not args.force:
        print(f"Existing session at {TUSK_SESSION_FILE}.")
        print("Re-run with --force to overwrite.")
        return 0

    with sync_playwright() as p:
        launch_kwargs = {
            "headless": not args.headed,
            "user_data_dir": str(profile_dir),
            "viewport": {"width": 1280, "height": 900},
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
        }
        if args.proxy:
            launch_kwargs["proxy"] = {"server": args.proxy}

        print(f"Launching Chromium (headless={not args.headed})...")
        context = p.chromium.launch_persistent_context(**launch_kwargs)

        page = context.pages[0] if context.pages else context.new_page()
        print(f"Opening {args.url} ...")
        page.goto(args.url, wait_until="domcontentloaded")

        print()
        print("=" * 60)
        print("ACTION REQUIRED: complete the Clerk sign-in in the browser.")
        print("Sign in with Google/Apple/email — whichever you prefer.")
        print("Once the chat page loads (you see the prompt textarea),")
        print("this script will save the session and exit automatically.")
        print("=" * 60)
        print()

        signed_in = False
        deadline = time.monotonic() + args.timeout
        while time.monotonic() < deadline:
            try:
                textarea = page.query_selector("textarea, [contenteditable='true']")
                signin_visible = page.query_selector(
                    "button:has-text('Sign in'), button:has-text('Get started'), "
                    "button:has-text('Sign up'), a:has-text('Sign in')"
                )
                try:
                    clerk_jwt = page.evaluate("() => localStorage.getItem('__client')") or ""
                except Exception:
                    clerk_jwt = ""
                has_jwt = len(clerk_jwt) > 20 and "eyJ" in clerk_jwt
                if textarea and not signin_visible and has_jwt:
                    signed_in = True
                    break
            except Exception:
                pass
            time.sleep(2)

        if not signed_in:
            print("Timed out waiting for sign-in. You can re-run this script.")
            try:
                context.close()
            except Exception:
                pass
            return 2

        print("Signed in detected. Saving session...")
        storage = context.storage_state()
        TUSK_SESSION_FILE.write_text(json.dumps(storage, indent=2))
        print(f"Saved session to {TUSK_SESSION_FILE} ({len(storage.get('cookies', []))} cookies).")

        try:
            from tusk_lib import TuskClient
            client = TuskClient()
            models = client.list_models()
            print(f"Verified: {len(models)} models reachable with this session.")
        except Exception as e:
            print(f"WARNING: post-save verification failed: {e}")
            print("Session was saved anyway — try `tusk.py --list-models` to re-check.")

        try:
            context.close()
        except Exception:
            pass

    print("Done. You can now use `tusk.py` to send prompts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
