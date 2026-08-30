#!/usr/bin/env python3
"""Reply to X/Twitter tweets via Playwright headless browser."""

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def find_chrome_binary():
    """Find system Chrome/Chromium binary."""
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


def reply_to_tweet(tweet_id: str, text: str, cookies_path: str, headless: bool = True, slow_mo: int = 100):
    """Reply to a tweet using browser automation."""
    
    cookies_path = Path(cookies_path)
    if not cookies_path.exists():
        print(f"ERROR: Cookies file not found: {cookies_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(cookies_path) as f:
        raw = json.load(f)
    
    # Handle both {cookies: [...]} and bare [...] formats
    if isinstance(raw, dict) and "cookies" in raw:
        cookies = raw["cookies"]
    elif isinstance(raw, list):
        cookies = raw
    elif isinstance(raw, dict):
        cookies = [raw]
    else:
        cookies = []
    
    if not cookies:
        print("ERROR: Cookies file is empty", file=sys.stderr)
        sys.exit(1)
    
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
        
        tweet_url = f"https://x.com/i/status/{tweet_id}"
        print(f"Navigating to {tweet_url}...")
        
        try:
            # Navigate to x.com first to establish session context
            page.goto("https://x.com", wait_until="domcontentloaded", timeout=30000)
            time.sleep(1)
            page.goto(tweet_url, wait_until="domcontentloaded", timeout=30000)
        except PlaywrightTimeout:
            print("ERROR: Page load timed out", file=sys.stderr)
            browser.close()
            sys.exit(1)
        
        time.sleep(2)
        
        if "login" in page.url or "Log in" in page.title():
            print("ERROR: Not logged in. Cookies may be expired.", file=sys.stderr)
            browser.close()
            sys.exit(1)
        
        print("Looking for reply button...")
        try:
            reply_button = page.locator('[data-testid="reply"]').first
            reply_button.wait_for(state="visible", timeout=10000)
            reply_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Could not find reply button: {e}", file=sys.stderr)
            page.screenshot(path="/tmp/x_reply_error.png")
            browser.close()
            sys.exit(1)

        print("Waiting for reply modal...")
        time.sleep(3)

        print("Looking for tweet text area...")
        try:
            editor = page.locator('[data-testid="tweetTextarea_0"]').first
            editor.wait_for(state="visible", timeout=15000)
            editor.click()
            editor.fill(text)
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Could not type reply: {e}", file=sys.stderr)
            page.screenshot(path="/tmp/x_reply_error.png")
            with open("/tmp/x_page.html", "w") as f:
                f.write(page.content())
            browser.close()
            sys.exit(1)

        print("Looking for post button...")
        try:
            submit_button = page.locator('[data-testid="tweetButton"]').first
            submit_button.wait_for(state="visible", timeout=5000)
            submit_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"ERROR: Could not post reply: {e}", file=sys.stderr)
            page.screenshot(path="/tmp/x_reply_error.png")
            browser.close()
            sys.exit(1)

        print(f"Reply posted successfully to {tweet_url}")
        page.screenshot(path="/tmp/x_reply_success.png")
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Reply to X tweet via browser")
    parser.add_argument("--tweet-id", help="Tweet ID to reply to")
    parser.add_argument("--url", help="Full tweet URL")
    parser.add_argument("--text", required=True, help="Reply text")
    parser.add_argument("--cookies", required=True, help="Path to cookies JSON file")
    parser.add_argument("--headless", type=lambda x: x.lower() != "false", default=True, help="Run headless")
    parser.add_argument("--slow-mo", type=int, default=100, help="Slow motion ms")
    
    args = parser.parse_args()
    
    if args.url:
        tweet_id = args.url.split("/status/")[-1].split("?")[0].split("/")[0]
    elif args.tweet_id:
        tweet_id = args.tweet_id
    else:
        print("ERROR: Provide --tweet-id or --url", file=sys.stderr)
        sys.exit(1)
    
    reply_to_tweet(
        tweet_id=tweet_id,
        text=args.text,
        cookies_path=args.cookies,
        headless=args.headless,
        slow_mo=args.slow_mo,
    )


if __name__ == "__main__":
    main()
