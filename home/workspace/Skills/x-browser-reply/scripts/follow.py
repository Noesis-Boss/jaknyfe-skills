#!/usr/bin/env python3
"""Follow an X/Twitter user via Playwright headless browser."""
import argparse
import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def find_chrome_binary():
    candidates = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return None


def follow_user(username: str, cookies_path: str, headless: bool = True, slow_mo: int = 100):
    cookies_path = Path(cookies_path)
    if not cookies_path.exists():
        print(f"ERROR: Cookies file not found: {cookies_path}", file=sys.stderr)
        sys.exit(1)

    with open(cookies_path) as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "cookies" in raw:
        cookies = raw["cookies"]
    elif isinstance(raw, list):
        cookies = raw
    elif isinstance(raw, dict):
        cookies = [raw]
    else:
        cookies = []

    chrome_path = find_chrome_binary()
    if not chrome_path:
        print("ERROR: No Chrome/Chromium binary found", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=headless,
            slow_mo=slow_mo,
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        context.add_cookies(cookies)
        page = context.new_page()

        profile_url = f"https://x.com/{username}"
        print(f"Navigating to {profile_url}...")
        try:
            page.goto("https://x.com", wait_until="domcontentloaded", timeout=30000)
            time.sleep(1)
            page.goto(profile_url, wait_until="domcontentloaded", timeout=30000)
        except PlaywrightTimeout:
            print("ERROR: Page load timed out", file=sys.stderr)
            browser.close()
            sys.exit(1)

        time.sleep(2)

        if "login" in page.url or "Log in" in page.title():
            print("ERROR: Not logged in. Cookies may be expired.", file=sys.stderr)
            browser.close()
            sys.exit(1)

        print("Looking for follow button...")
        try:
            # Try multiple selectors for the follow button
            follow_selectors = [
                '[data-testid="follow"]',
                '[data-testid~="follow"]',
                'button[aria-label*="Follow"]',
            ]
            follow_btn = None
            for sel in follow_selectors:
                try:
                    loc = page.locator(sel).first
                    loc.wait_for(state="visible", timeout=5000)
                    follow_btn = loc
                    break
                except Exception:
                    continue

            if not follow_btn:
                # Try finding by text
                follow_btn = page.get_by_role("button", name="Follow").first
                follow_btn.wait_for(state="visible", timeout=5000)

            follow_btn.click()
            time.sleep(2)
            print(f"Followed @{username}")
        except Exception as e:
            print(f"ERROR: Could not find follow button: {e}", file=sys.stderr)
            page.screenshot(path="/tmp/x_follow_error.png")
            with open("/tmp/x_follow_page.html", "w") as f:
                f.write(page.content())
            browser.close()
            sys.exit(1)

        page.screenshot(path="/tmp/x_follow_success.png")
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Follow X user via browser")
    parser.add_argument("--username", required=True, help="Username to follow (without @)")
    parser.add_argument("--cookies", required=True, help="Path to cookies JSON file")
    parser.add_argument("--headless", type=lambda x: x.lower() != "false", default=True)
    parser.add_argument("--slow-mo", type=int, default=100)
    args = parser.parse_args()

    follow_user(
        username=args.username,
        cookies_path=args.cookies,
        headless=args.headless,
        slow_mo=args.slow_mo,
    )


if __name__ == "__main__":
    main()
