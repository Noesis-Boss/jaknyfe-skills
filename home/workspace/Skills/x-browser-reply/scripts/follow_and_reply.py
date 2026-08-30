#!/usr/bin/env python3
"""Find follow-back posts, reply, and follow via Playwright headless browser."""

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def find_chrome_binary():
    for path in ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"]:
        if Path(path).exists():
            return path
    return None


QUICK_REPLIES = [
    "Follow you! 🚀",
    "Following now 👍",
    "Done, followed! 🙌",
    "Got it, followed! 🔥",
    "Followed! 💯",
    "On it, followed! ✨",
    "You got it, followed! 🎯",
    "Following! 🤝",
    "Followed back! ⚡",
    "Done! 🚀",
]


def reply_and_follow(page, text, tweet_url, slow_mo=100):
    """Reply to the current tweet and follow its author. Returns True on success."""
    # Click reply
    try:
        reply_btn = page.locator('[data-testid="reply"]').first
        reply_btn.wait_for(state="visible", timeout=10000)
        reply_btn.click()
        time.sleep(1.5)
    except Exception as e:
        print(f"  WARN: Could not click reply: {e}", file=sys.stderr)
        return False

    # Type reply
    try:
        editor = page.locator('[data-testid="tweetTextarea_0"]').first
        editor.wait_for(state="visible", timeout=15000)
        editor.click()
        editor.fill(text)
        time.sleep(1)
    except Exception as e:
        print(f"  WARN: Could not type reply: {e}", file=sys.stderr)
        return False

    # Submit
    try:
        submit = page.locator('[data-testid="tweetButton"]').first
        submit.wait_for(state="visible", timeout=5000)
        submit.click()
        time.sleep(3)
    except Exception as e:
        print(f"  WARN: Could not click Post: {e}", file=sys.stderr)
        return False

    print(f"  Reply posted: {text}")

    # Follow author - navigate to their profile, click Follow
    try:
        # Find author profile link (not the tweet link)
        username = tweet_url.split("/status/")[0].rstrip("/").split("/")[-1]
        
        profile_url = f"https://x.com/{username}"
        print(f"  Navigating to @{username}'s profile...")
        page.goto(profile_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Look for follow button
        follow_btn = page.locator("button[data-testid='follow']").first
        if follow_btn.count() == 0:
            follow_btn = page.get_by_text("Follow", exact=True).first
        
        follow_btn.wait_for(state="visible", timeout=10000)
        follow_btn.click()
        time.sleep(2)
        print(f"  Followed @{username}")
    except Exception as e:
        if "unfollow" in str(e).lower() or "following" in str(e).lower():
            print(f"  Already following @{username}")
        else:
            print(f"  WARN: Follow failed (may already follow): {e}", file=sys.stderr)

    return True


def process_tweet(page, tweet_url, cookies_path):
    """Navigate to a tweet and reply+follow."""
    print(f"Processing: {tweet_url}")
    try:
        page.goto("https://x.com", wait_until="domcontentloaded", timeout=30000)
        time.sleep(1)
        page.goto(tweet_url, wait_until="domcontentloaded", timeout=30000)
    except PlaywrightTimeout:
        print("  WARN: Page load timed out, skipping", file=sys.stderr)
        return False

    time.sleep(2)

    if "login" in page.url or "Log in" in page.title():
        print("  ERROR: Not logged in, cookies expired", file=sys.stderr)
        return "EXPIRED"

    text = random.choice(QUICK_REPLIES)
    return reply_and_follow(page, text, tweet_url)


def main():
    parser = argparse.ArgumentParser(description="Find follow-back posts, reply, and follow")
    parser.add_argument("--cookies", required=True, help="Path to cookies JSON file")
    parser.add_argument("--account", required=True, help="Account label (e.g., zdsentry)")
    parser.add_argument("--max", type=int, default=5, help="Max posts to process per run")
    parser.add_argument("--headless", type=lambda x: x.lower() != "false", default=True)
    parser.add_argument("--slow-mo", type=int, default=100)
    args = parser.parse_args()

    cookies_path = Path(args.cookies)
    if not cookies_path.exists():
        print(f"ERROR: Cookies file not found: {cookies_path}", file=sys.stderr)
        sys.exit(1)

    with open(cookies_path) as f:
        raw = json.load(f)
    if isinstance(raw, dict) and "cookies" in raw:
        cookies = raw["cookies"]
    elif isinstance(raw, list):
        cookies = raw
    else:
        cookies = [raw]

    chrome_path = find_chrome_binary()
    if not chrome_path:
        print("ERROR: No Chrome/Chromium binary found", file=sys.stderr)
        sys.exit(1)

    # Search queries for follow-back posts
    search_queries = [
        '"follow me" "follow back"',
        '"follow back if following"',
        '"F4F" "follow back"',
        '"follow for follow" "follow back"',
        '"follow me back" is:verified',
        '"follow me" lang:en',
    ]

    processed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_path, headless=args.headless, slow_mo=args.slow_mo)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        context.add_cookies(cookies)
        page = context.new_page()

        for query in search_queries:
            if processed >= args.max:
                break

            search_url = f"https://x.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
            print(f"\nSearching: {query}")

            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(4)
            except PlaywrightTimeout:
                print("  WARN: Search timed out, skipping", file=sys.stderr)
                continue

            if "login" in page.url or "Log in" in page.title():
                print("ERROR: Not logged in, cookies expired", file=sys.stderr)
                break

            # Extract tweet links from search results
            tweet_links = []
            try:
                # Look for links to individual tweets
                all_links = page.locator('a[href*="/status/"]')
                for i in range(all_links.count()):
                    href = all_links.nth(i).get_attribute("href")
                    if href and "/status/" in href:
                        # Handle both absolute and relative URLs
                        match = re.search(r'(https?://x\.com)?(/[^/]+/status/\d+)', href)
                        if match:
                            tweet_url = "https://x.com" + match.group(2)
                            if tweet_url not in tweet_links:
                                tweet_links.append(tweet_url)
            except Exception as e:
                print(f"  WARN: Could not extract tweet links: {e}", file=sys.stderr)

            print(f"  Found {len(tweet_links)} tweet links")

            for tweet_url in tweet_links:
                if processed >= args.max:
                    break

                result = process_tweet(page, tweet_url, str(cookies_path))
                if result == "EXPIRED":
                    print("Cookies expired, aborting.")
                    browser.close()
                    sys.exit(1)
                if result:
                    processed += 1
                    print(f"  [{processed}/{args.max}] Done")
                else:
                    print(f"  [{processed}/{args.max}] Failed, continuing...")

                # Random delay between actions to avoid rate limiting
                delay = random.randint(10, 25)
                print(f"  Waiting {delay}s...")
                time.sleep(delay)

        browser.close()

    print(f"\nDone! Processed {processed} posts for @{args.account}.")
    if processed == 0:
        print("No posts found or all failed. Will retry next run.")


if __name__ == "__main__":
    main()
