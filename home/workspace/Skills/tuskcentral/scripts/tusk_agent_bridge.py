#!/usr/bin/env python3
"""
tusk_agent_bridge.py — Pipe prompts through tuskcentral.ai and capture output.

Uses the active `tuskcentral` agent-browser session. Returns the assistant reply as plain text.

Usage:
  python3 tusk_agent_bridge.py "Your prompt here"
  python3 tusk_agent_bridge.py "Your prompt here" --model Brainiac
  python3 tusk_agent_bridge.py "Your prompt here" --json
"""

import argparse
import json
import subprocess
import sys
import time

SESSION = "tuskcentral"
TUSK_CHAT_URL = "https://tuskcentral.ai/chat"
DEFAULT_MODEL = "Brainiac"
DEFAULT_TIMEOUT = 120


def run_ab(args, timeout=60):
    cmd = ["agent-browser", "--session", SESSION] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"timeout after {timeout}s"


def eval_js(code, timeout=20):
    rc, out, err = run_ab(["eval", code], timeout=timeout)
    if rc != 0:
        raise RuntimeError(f"agent-browser failed: rc={rc} err={err}")
    out = out.strip()
    if (out.startswith('"') and out.endswith('"')) or (out.startswith("'") and out.endswith("'")):
        out = out[1:-1]
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out


def ensure_chat():
    rc, out, err = run_ab(["get", "url"], timeout=10)
    if rc != 0:
        raise RuntimeError("cannot get browser url")
    if not out.startswith("https://tuskcentral.ai/chat"):
        run_ab(["open", TUSK_CHAT_URL], timeout=15)
        time.sleep(2)


def accept_tos():
    rc, out, err = run_ab(["eval", """
        (() => {
          const cb = document.querySelector('input[type="checkbox"]');
          if (!cb || cb.checked) return 'no_tos';
          cb.checked = true;
          cb.dispatchEvent(new Event('change', { bubbles: true }));
          const btn = document.querySelector('button.dialog-button.primary-button');
          if (btn) btn.click();
          return 'accepted';
        })()
    """], timeout=15)
    if rc != 0:
        raise RuntimeError("tos eval failed")
    time.sleep(1)


def select_model(model):
    model = model or DEFAULT_MODEL
    # Open dropdown via the model picker button with class model-picker-button
    run_ab(["eval", """
        (() => {
          const btn = document.querySelector("button.model-picker-button");
          if (!btn) return 'no_model_btn';
          btn.click();
          return 'opened';
        })()
    """], timeout=10)
    time.sleep(0.5)

    # Search for the model in the dialog list
    escaped_model = model.replace("'", "\\'")
    run_ab(["eval", f"""
        (() => {{
          const items = Array.from(document.querySelectorAll('*'));
          const match = items.find(el => {{
            const text = (el.innerText || el.textContent || '').trim();
            return text === '{escaped_model}';
          }});
          if (!match) return 'model_not_found';
          match.click();
          return 'selected';
        }})()
    """], timeout=10)
    time.sleep(0.3)

    # Confirm
    run_ab(["eval", """
        (() => {
          const btns = Array.from(document.querySelectorAll('button'));
          const confirm = btns.find(b => (b.innerText || b.textContent || '').trim() === 'Confirm');
          if (confirm) confirm.click();
          return 'confirmed';
        })()
    """], timeout=10)
    time.sleep(0.5)


def send_prompt(prompt):
    escaped = prompt.replace("\\", "\\\\").replace("'", "\\'")
    # Fill via agent-browser fill using dynamic selectors (not stale refs)
    fill_selectors = [
        'textarea[aria-label="Your question"]',
        'input[aria-label="Your question"]',
        'textarea',
        'input[type="text"]',
    ]
    filled = False
    for sel in fill_selectors:
        rc, out, err = run_ab(["fill", sel, escaped], timeout=15)
        if rc == 0:
            filled = True
            break
    if not filled:
        raise RuntimeError("failed to fill prompt: no textbox found")

    # Click submit button (Enter key doesn't work on this site)
    rc, out, err = run_ab(["click", "button:has-text('submit')"], timeout=10)
    if rc != 0:
        rc, out, err = run_ab(["eval", """
            (() => {
              const btns = Array.from(document.querySelectorAll('button'));
              const submit = btns.find(b => b.textContent.trim() === 'submit' || b.getAttribute('aria-label') === 'submit');
              if (submit) { submit.click(); return 'clicked'; }
              return 'not_found';
            })()
        """], timeout=10)
        if rc != 0 or out == '"not_found"':
            raise RuntimeError("failed to submit prompt")


def extract_assistant_reply(full_text, prompt):
    # Primary: grab from .ai-response element
    resp_text = eval_js(
        "(() => { const els = document.querySelectorAll('.ai-response');"
        " if (!els.length) return ''; const el = els[els.length - 1];"
        " return (el.innerText || el.textContent || '').trim(); })()"
    )
    if resp_text and resp_text != prompt:
        return resp_text
    # Fallback: parse body text
    lines = [ln.rstrip() for ln in str(full_text).splitlines()]
    user_idx = None
    for i, ln in enumerate(lines):
        if ln.strip() == prompt.strip():
            user_idx = i
            break
    if user_idx is None:
        return str(full_text).strip()
    out = []
    skip_prefixes = (
        "GPT-", "Search", "Central AI", "New Chat", "Recent Chats", "Sign In", "Help",
        "chevron_left", "About", "Models", "Privacy", "Terms", "Contact Us", "©",
        "v0.9.", "AI responses may be inaccurate", "Thought process",
    )
    for ln in lines[user_idx + 1:]:
        if not ln:
            continue
        if any(ln.startswith(p) for p in skip_prefixes):
            continue
        out.append(ln)
    return "\n".join(out).strip() if out else "\n".join(lines[user_idx + 1:]).strip()


def main():
    parser = argparse.ArgumentParser(description="Prompt tuskcentral.ai and capture output")
    parser.add_argument("prompt", help="Prompt to send")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Wait timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    t0 = time.monotonic()
    ensure_chat()
    accept_tos()
    select_model(args.model)
    send_prompt(args.prompt)

    # Wait for response (stable-cycles approach)
    deadline = time.monotonic() + args.timeout
    reply = ""
    last_resp = ""
    stable_cycles = 0
    while time.monotonic() < deadline:
        try:
            text = eval_js("(() => { if (!document.body) return ''; return (document.body.innerText || document.body.textContent || '').trim(); })()", timeout=15)
            resp = extract_assistant_reply(str(text), args.prompt)
            if resp and resp != last_resp:
                last_resp = resp
                stable_cycles = 0
            elif resp == last_resp and resp:
                stable_cycles += 1
                if stable_cycles >= 2:
                    reply = resp
                    break
        except Exception:
            pass
        time.sleep(2)

    elapsed = time.monotonic() - t0
    if args.json:
        print(json.dumps({
            "text": reply,
            "elapsed_sec": round(elapsed, 1),
            "session": SESSION,
        }))
    else:
        print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
