import subprocess, json, sys
SESSION = 'tuskcentral'
text = 'Reply with pong only.'
js_type = """
    (() => {
      const selectors = [
        \"textarea[aria-label=\\\"Your question\\\"]\",
        \"input[aria-label=\\\"Your question\\\"]\",
        \"textarea\",
        \"input[type=\\\"text\\\"]\"
      ];
      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
          el.value = """ + json.dumps(text) + """;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          return 'typed';
        }
      }
      return 'not_found';
    })()
"""
cmd = ['agent-browser', '--session', SESSION, 'eval', js_type]
print('Running agent-browser eval...')
p = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print('rc:', p.returncode)
print('stdout:', repr(p.stdout))
print('stderr:', repr(p.stderr))
