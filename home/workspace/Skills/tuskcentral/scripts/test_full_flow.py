#!/usr/bin/env python3
import subprocess, sys, time, json

SESSION = "tuskcentral"
TUSK_CHAT_URL = "https://tuskcentral.ai/chat"

def run_ab(args, timeout=60):
    cmd = ["agent-browser", "--session", SESSION] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        print(f"TIMEOUT after {timeout}s", file=sys.stderr)
        return -1, "", f"timeout: {e}"

def log(step, rc, out, err):
    print(f"[{step}] rc={rc}, out={repr(out.strip()[:200])}, err={repr(err.strip()[:200])}", file=sys.stderr)

# Step 1: get url
rc, out, err = run_ab(["get", "url"], timeout=10)
log("get_url", rc, out, err)

# Step 2: handle tos
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
log("handle_tos", rc, out, err)
time.sleep(1)

# Step 3: select model Brainiac
rc, out, err = run_ab(["eval", """
    (() => {
      const triggers = Array.from(document.querySelectorAll('button, [role="button"]'));
      const btn = triggers.find(b => (b.innerText || b.textContent || '').includes('GPT-5'));
      if (!btn) return 'no_model_btn';
      btn.click();
      return 'opened';
    })()
"""], timeout=10)
log("open_model_dropdown", rc, out, err)
time.sleep(0.5)

# Step 4: select Brainiac
rc, out, err = run_ab(["eval", """
    (() => {
      const cards = Array.from(document.querySelectorAll('*'));
      const match = cards.find(el => (el.innerText || el.textContent || '').trim() === 'Brainiac');
      if (!match) return 'model_not_found';
      match.click();
      return 'selected';
    })()
"""], timeout=10)
log("select_brainiac", rc, out, err)
time.sleep(0.3)

# Step 5: confirm
rc, out, err = run_ab(["eval", """
    (() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const confirm = btns.find(b => (b.innerText || b.textContent || '').trim() === 'Confirm');
      if (confirm) confirm.click();
      return 'confirmed';
    })()
"""], timeout=10)
log("confirm_model", rc, out, err)
time.sleep(0.5)

# Step 6: type prompt
rc, out, err = run_ab(["eval", """
    (() => {
      const selectors = [
        'textarea[aria-label="Your question"]',
        'input[aria-label="Your question"]',
        'textarea',
        'input[type="text"]'
      ];
      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
          el.value = 'Reply with pong only.';
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          return 'typed';
        }
      }
      return 'not_found';
    })()
"""], timeout=10)
log("type_prompt", rc, out, err)
time.sleep(0.3)

# Step 7: send
rc, out, err = run_ab(["eval", """
    (() => {
      const selectors = [
        'textarea[aria-label="Your question"]',
        'input[aria-label="Your question"]',
        'textarea',
        'input[type="text"]'
      ];
      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
          el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
          el.dispatchEvent(new KeyboardEvent('keypress', { key: 'Enter', keyCode: 13, bubbles: true }));
          el.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', keyCode: 13, bubbles: true }));
          return 'sent';
        }
      }
      return 'not_found';
    })()
"""], timeout=10)
log("send_prompt", rc, out, err)

# Step 8: wait and get text
print("Waiting 60s for response...", file=sys.stderr)
time.sleep(60)
rc, out, err = run_ab(["eval", "(() => { if (!document.body) return ''; return (document.body.innerText || document.body.textContent || '').trim(); })()"], timeout=15)
log("get_text", rc, out, err)
