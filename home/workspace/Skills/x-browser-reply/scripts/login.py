#!/usr/bin/env python3
"""Log into X and save cookies for future headless use."""

import argparse
import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright


def find_chrome_binary():
    for path in ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"]:
        if Path(path).exists():
            return path
    return None


def wait_for_element(page, selectors, timeout=10000, label="element"):
    """Wait for any of the selectors to appear and return the first match."""
    for sel in selectors:
        try:
            el = page.locator(sel).first
            el.wait_for(state="visible", timeout=timeout // len(selectors))
            return el
        except:
            continue
    raise Exception(f"Could not find {label} with selectors: {selectors}")


def login(username, password, cookies_path, headless=True):
    chrome_path = find_chrome_binary()
    if not chrome_path:
        print("ERROR: No Chrome/Chromium binary found", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=headless,
            slow_mo=100,
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        print("Navigating to X login...")
        page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Step 1: Enter username
        print("Entering username...")
        try:
            username_input = wait_for_element(page, [
                'input[name="username_or_email"]',
                'input[autocomplete="username"]',
                'input[type="text"]',
            ], timeout=10000, label="username input")
            username_input.fill(username)
            time.sleep(0.5)

            next_btn = wait_for_element(page, [
                'button:has-text("Continue")',
                '[role="button"]:has-text("Continue")',
                'button:has-text("Next")',
                '[role="button"]:has-text("Next")',
                'span:has-text("Next")',
            ], timeout=5000, label="Next button")
            next_btn.click()
            time.sleep(2)
        except Exception as e:
            print(f"ERROR at username step: {e}", file=sys.stderr)
            page.screenshot(path="/tmp/x_login_error.png")
            browser.close()
            sys.exit(1)

        # Step 2: Handle phone/email verification
        print("Checking for phone verification...")
        try:
            verify_input = wait_for_element(page, [
                'input[name="text"]',
                'input[autocomplete="on"]',
                'input[type="tel"]',
                'input[placeholder*="phone"]',
                'input[placeholder*="code"]',
            ], timeout=5000, label="verification input")
            
            if verify_input:
                print("Phone/email verification required.")
                print("Waiting for verification code in /tmp/x_verification_code.txt...")
                
                # Wait for user to provide verification code
                code_file = Path("/tmp/x_verification_code.txt")
                max_wait = 120  # 2 minutes
                waited = 0
                while not code_file.exists() and waited < max_wait:
                    time.sleep(2)
                    waited += 2
                    print(f"  Waiting... {waited}s")
                
                if not code_file.exists():
                    print("ERROR: No verification code provided within 2 minutes", file=sys.stderr)
                    page.screenshot(path="/tmp/x_login_timeout.png")
                    browser.close()
                    sys.exit(1)
                
                code = code_file.read_text().strip()
                code_file.unlink()  # Clean up
                print(f"Entering verification code: {code}")
                verify_input.fill(code)
                time.sleep(0.5)
                
                next_btn = wait_for_element(page, [
                    'button:has-text("Next")',
                    '[role="button"]:has-text("Next")',
                ], timeout=5000, label="Next button")
                next_btn.click()
                time.sleep(2)
        except Exception as e:
            print(f"Verification step note: {e}")
            # Continue anyway - verification might not be required

        # Step 3: Enter password
        print("Entering password...")
        try:
            time.sleep(1)
            password_input = wait_for_element(page, [
                'input[name="password"]',
                'input[type="password"]',
            ], timeout=10000, label="password input")
            password_input.fill(password)
            time.sleep(0.5)
        except Exception as e:
            print(f"ERROR at password step: {e}", file=sys.stderr)
            page.screenshot(path="/tmp/x_login_error.png")
            browser.close()
            sys.exit(1)

        # Step 4: Click Log in
        print("Clicking Log in...")
        try:
            login_btn = wait_for_element(page, [
                'button[data-testid="LoginForm_Login_Button"]',
                'button:has-text("Log in")',
                '[role="button"]:has-text("Log in")',
            ], timeout=5000, label="Log in button")
            login_btn.click(force=True)
            time.sleep(3)
        except Exception as e:
            print(f"ERROR at login button: {e}", file=sys.stderr)
            page.screenshot(path="/tmp/x_login_error.png")
            browser.close()
            sys.exit(1)

        # Wait for redirect to home
        print("Waiting for login to complete...")
        try:
            page.wait_for_url("**/home**", timeout=15000)
            time.sleep(2)
        except:
            pass

        current_url = page.url
        print(f"Current URL: {current_url}")

        if "login" in current_url or "flow" in current_url:
            print("WARNING: Login may not have succeeded. Check screenshot.", file=sys.stderr)
            page.screenshot(path="/tmp/x_login_result.png")
        else:
            print("Login appears successful.")
            page.screenshot(path="/tmp/x_login_success.png")

        # Save cookies
        cookies = context.cookies()
        if cookies:
            with open(cookies_path, "w") as f:
                json.dump(cookies, f, indent=2)
            print(f"Saved {len(cookies)} cookies to {cookies_path}")
        else:
            print("ERROR: No cookies captured", file=sys.stderr)

        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Log into X and save cookies")
    parser.add_argument("--username", required=True, help="X username or email")
    parser.add_argument("--password", required=True, help="X password")
    parser.add_argument("--cookies", default="/home/workspace/Skills/x-browser-reply/cookies.json", help="Output cookies path")
    parser.add_argument("--headless", type=lambda x: x.lower() != "false", default=True, help="Run headless")
    args = parser.parse_args()

    login(args.username, args.password, args.cookies, args.headless)


if __name__ == "__main__":
    main()
