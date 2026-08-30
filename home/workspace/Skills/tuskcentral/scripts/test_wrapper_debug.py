#!/usr/bin/env python3
"""Debug wrapper steps one at a time."""
import subprocess, time

SESSION = "tuskcentral"

def run_ab(args, timeout=15):
    cmd = ["agent-browser", "--session", SESSION] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    print(f"CMD: agent-browser {' '.join(args)}")
    print(f"RC={p.returncode} STDOUT={p.stdout.strip()!r} STDERR={p.stderr.strip()!r}")
    return p.returncode, p.stdout, p.stderr

# 1. Check current URL
run_ab(["get", "url"])

# 2. Fill textbox
run_ab(["fill", 'textarea[aria-label="Your question"], input[aria-label="Your question"], textarea, input[type="text"]', "debug_test_789"], timeout=10)

# 3. Check value
rc, out, _ = run_ab(["eval", '(() => { const ta = document.querySelector("textarea[aria-label=\\"Your question\\"]"); return ta ? ta.value : "not found"; })()'])
print(f"Textbox value after fill: {out.strip()}")

# 4. Click submit
run_ab(["click", "button:has-text('submit')"], timeout=10)

# 5. Wait and poll response
for i in range(6):
    time.sleep(5)
    rc, out, _ = run_ab(["eval", """
        (() => {
          const main = document.querySelector('main');
          if (!main) return '';
          const paras = Array.from(main.querySelectorAll('p, [role="paragraph"]'));
          const texts = paras.map(p => (p.innerText || p.textContent || '').trim()).filter(Boolean);
          return texts.length ? texts[texts.length - 1] : '';
        })()
    """])
    print(f"Poll {i+1}: {out.strip()}")
