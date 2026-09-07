const TOKEN_RE = /zo_sk_[A-Za-z0-9_-]{16,}/;
let lastSent = '';

function scan() {
  try {
    const candidates = [document.body ? document.body.innerText : ''];
    document.querySelectorAll('input, textarea').forEach((e) => candidates.push(e.value || ''));
    document.querySelectorAll('code, pre').forEach((e) => candidates.push(e.textContent || ''));
    const text = candidates.join('\n');
    const m = text.match(TOKEN_RE);
    if (m && m[0] !== lastSent) {
      lastSent = m[0];
      try { chrome.runtime.sendMessage({ type: 'tokenCaptured', token: m[0] }); } catch (_) {}
    }
  } catch (e) {
    console.error('Error during scan:', e); // Log the error for debugging
    // Optionally add a user-facing message if the error is critical
    // addSystem(`Could not scan page for tokens: ${e.message}`);
  }
}

scan();
const obs = new MutationObserver(() => scan());
obs.observe(document.documentElement, { childList: true, subtree: true, characterData: true });
let n = 0;
const iv = setInterval(() => {
  scan();
  if (++n > 20) clearInterval(iv);
}, 500);
