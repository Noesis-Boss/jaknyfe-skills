#!/usr/bin/env python3
"""
tusk_wrapper.py - Interactive wrapper for tuskcentral.ai

Detects sign-in state from the live browser session, handles the sign-in flow,
and runs CLI commands (chat, list-models, status) by replaying them through
the tuskcentral.ai UI, returning parsed output.
"""

import shutil
import subprocess
import sys
import time


def run(cmd: str) -> tuple[int, str, str]:
    """Run shell command, return (rc, stdout, stderr)."""
    r = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return r.returncode, r.stdout, r.stderr


def browser(*args: str) -> tuple[int, str, str]:
    """Run agent-browser with the tuskcentral session."""
    cmd = "agent-browser --session tuskcentral " + " ".join(args)
    return run(cmd)


def ensure_page() -> bool:
    """Make sure we're on the tuskcentral.ai chat page."""
    # Open the chat page (non-blocking)
    run("agent-browser --session tuskcentral open https://tuskcentral.ai/chat")
    time.sleep(2)
    rc, out, _ = browser("get url")
    return "tuskcentral.ai/chat" in out


def is_signed_in() -> bool:
    """Check if we have an active TuskCentral session."""
    rc, out, _ = browser("snapshot -c")
    if rc != 0:
        return False
    # If "Sign in" button is present, we're NOT signed in
    if "sign in" in out.lower():
        return False
    # Check for chat textbox as a positive signal
    if "textbox" in out:
        return True
    return False


def handle_sign_in() -> bool:
    """Guide user through sign-in flow. Returns True when signed in."""
    print("=" * 60)
    print("TUSKCENTRAL SIGN-IN REQUIRED")
    print("=" * 60)
    print()
    print("You are not signed in to TuskCentral.")
    print()
    print("Sign-in options:")
    print("  1. Google OAuth")
    print("  2. Email magic link")
    print()
    print("I will click the Sign In button now.")
    print("Complete the sign-in flow in the browser window.")
    print()
    print("After signing in, run your command again.")
    print("=" * 60)
    print()

    # Click the Sign In button
    rc, out, err = browser('find role button click --name "Sign in"')
    if "Done" not in out:
        # Fallback: try text selector
        rc, out, err = browser('click "Sign in"')
    if rc != 0:
        print(f"Could not click Sign In button: {err}")
        return False

    time.sleep(2)

    # Take a screenshot so the user can see the sign-in page
    rc, out, _ = browser("screenshot /tmp/tusk_signin.png")
    if rc == 0:
        print("Screenshot saved to /tmp/tusk_signin.png")
        print("Check the screenshot to see the sign-in options.")
        print()

    return False  # User needs to complete sign-in manually


def wait_for_sign_in(timeout: int = 120) -> bool:
    """Poll for sign-in completion. Returns True if signed in within timeout."""
    print("Waiting for sign-in...")
    start = time.time()
    while time.time() - start < timeout:
        if is_signed_in():
            print("✓ Signed in successfully!")
            return True
        time.sleep(3)
    print("✗ Sign-in timeout. Please try again.")
    return False


def run_chat(message: str, model: str | None = None) -> bool:
    """Send a chat message and print the reply."""
    if not ensure_page():
        print("Error: Could not open tuskcentral.ai/chat")
        return False

    # Note: Guest usage works on tuskcentral. Sign-in is optional for most models.
    # If a sign-in dialog appears, dismiss it or sign in manually.

    # Ensure page is loaded
    time.sleep(1)

    # Select model if specified
    if model:
        rc, out, err = browser('click "GPT-5 N"')
        if rc != 0:
            print(f"Warning: Could not open model selector: {err}")
        else:
            time.sleep(1)
            # Try to find and click the model in the dropdown
            rc, out, err = browser(f'click "button:has-text(\"{model}\")')
            if rc != 0:
                print(f"Warning: Could not select model '{model}': {err}")
            else:
                print(f"Selected model: {model}")
            time.sleep(1)

    # Type the message
    rc, out, err = browser('fill "textbox" "' + message.replace('"', '\\"') + '"')
    if rc != 0:
        print(f"Error: Could not find chat input: {err}")
        return False

    # Click submit
    rc, out, err = browser('click "submit"')
    if rc != 0:
        print(f"Error: Could not click submit: {err}")
        return False

    # Wait for response (simple polling)
    print("Waiting for response...", end="", flush=True)
    start = time.time()
    last_text = ""
    while time.time() - start < 120:
        rc, out, _ = browser("snapshot -c")
        if rc != 0:
            time.sleep(2)
            continue

        # Extract text from the snapshot
        import re
        texts = re.findall(r'text="([^"]+)"', out)
        current = " ".join(texts)

        # If text has changed since last check, keep waiting
        if current != last_text:
            last_text = current
            print(".", end="", flush=True)
            time.sleep(3)
        else:
            # Text hasn't changed for a bit, assume done
            print()
            print("Reply:", current.strip())
            return True

    print("\nError: Response timeout")
    return False


def list_models() -> bool:
    """List available models."""
    if not ensure_page():
        print("Error: Could not open tuskcentral.ai/chat")
        return False

    if not is_signed_in():
        if not handle_sign_in():
            return False
        if not wait_for_sign_in():
            return False

    # Click the model selector
    rc, out, err = browser('click "GPT-5 N"')
    if rc != 0:
        print(f"Error: Could not open model selector: {err}")
        return False

    time.sleep(1)

    # Get the snapshot to find model names
    rc, out, _ = browser("snapshot -c")
    if rc != 0:
        print("Error: Could not get model list")
        return False

    # Extract model names from the snapshot
    import re
    # Look for buttons with model names
    models = re.findall(r'button "([^"]*(?:GPT|Claude|Gemini|Llama|Mistral)[^"]*)"', out)
    if models:
        print("Available models:")
        for m in models:
            print(f"  - {m}")
    else:
        # Fallback: print the relevant part of the snapshot
        print("Available models (raw):")
        for line in out.split("\n"):
            if "GPT" in line or "Claude" in line or "Gemini" in line or "Llama" in line:
                print(f"  {line.strip()}")

    return True


def show_status() -> bool:
    """Show wrapper and session status."""
    # Check if agent-browser is available
    rc, _, err = run("which agent-browser")
    if rc != 0:
        print("Error: agent-browser not found in PATH")
        return False

    # Check if session exists
    rc, out, _ = browser("session")
    if rc != 0:
        print("Error: Could not connect to tuskcentral session")
        return False

    # Check sign-in status
    signed_in = is_signed_in()

    print("TuskCentral Wrapper Status")
    print("-" * 40)
    print(f"agent-browser: available")
    print(f"Session: tuskcentral")
    print(f"Signed in: {'Yes' if signed_in else 'No'}")
    print()
    print("Commands:")
    print("  chat <message> [--model MODEL]  Send a chat message")
    print("  list-models                     List available models")
    print("  status                          Show this status")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: tusk <command> [args]")
        print()
        print("Commands:")
        print("  chat <message> [--model MODEL]  Send a chat message")
        print("  list-models                     List available models")
        print("  status                          Show wrapper status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "chat":
        if len(sys.argv) < 3:
            print("Usage: tusk chat <message> [--model MODEL]")
            sys.exit(1)

        message = sys.argv[2]
        model = None

        # Parse --model flag
        if "--model" in sys.argv:
            idx = sys.argv.index("--model")
            if idx + 1 < len(sys.argv):
                model = sys.argv[idx + 1]

        success = run_chat(message, model)
        sys.exit(0 if success else 1)

    elif command == "list-models":
        success = list_models()
        sys.exit(0 if success else 1)

    elif command == "status":
        success = show_status()
        sys.exit(0 if success else 1)

    else:
        print(f"Unknown command: {command}")
        print("Usage: tusk <chat|list-models|status>")
        sys.exit(1)


if __name__ == "__main__":
    main()
