#!/usr/bin/env bash
# x-reply: Reply to an X/Twitter post using agent-browser (threaded reply)
# Usage: bash x-reply.sh <tweet-url> "<reply text>"
# Requires: agent-browser, X credentials saved as auth profile "x-main" (or env X_USER/X_PASS)
set -e

TWEET_URL="${1:?Usage: bash x-reply.sh <tweet-url> \"<reply text>\"}"
REPLY_TEXT="${2:?Usage: bash x-reply.sh <tweet-url> \"<reply text>\"}"
X_USER="${X_USER:-jak_nyfe}"
X_PASS="${X_PASS:-}"

FILL_JS='(() => {
  function setNativeValue(el, value) {
    const proto = Object.getPrototypeOf(el);
    const desc = Object.getOwnPropertyDescriptor(proto, "value");
    desc.set.call(el, value);
    el.dispatchEvent(new Event("input", { bubbles: true }));
  }
  const inps = Array.from(document.querySelectorAll("input"));
  const user = inps.find(i => i.type === "text") || inps[0];
  const pw = inps.find(i => i.type === "password") || inps[1];
  if (!user) return "no-input";
  setNativeValue(user, USER_VAL);
  if (pw) setNativeValue(pw, PASS_VAL);
  return "filled";
})()'

click_btn() { # click_btn <label>
  agent-browser eval "(() => { const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.trim() === '$1'); if (b) { b.click(); return 'clicked'; } return 'not-found'; })()"
}

echo "[x-reply] Opening $TWEET_URL"
agent-browser open "$TWEET_URL"
sleep 4

echo "[x-reply] Checking login state"
LOGIN_STATE=$(agent-browser eval "JSON.stringify({url: location.href, onb: location.href.includes('onboarding') || location.href.includes('/login'), limited: document.body.innerText.includes('temporarily limited')})" 2>/dev/null || echo "{}")
echo "[x-reply] $LOGIN_STATE"
if echo "$LOGIN_STATE" | grep -q '"onb":true'; then
  echo "[x-reply] Login required"
  if echo "$LOGIN_STATE" | grep -q '"limited":true'; then
    echo "[x-reply] ERROR: X login rate-limited (temporarily limited). Wait and retry later."
    exit 2
  fi
  FILL_JS_TMP="${FILL_JS//USER_VAL/$X_USER}"
  FILL_JS_TMP="${FILL_JS_TMP//PASS_VAL/$X_PASS}"
  agent-browser eval "$FILL_JS_TMP"
  sleep 2
  agent-browser eval "(() => { const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.trim() === 'Continue'); if (b) { b.click(); return 'continue-clicked'; } return 'no-continue'; })()"
  sleep 4
  # Second step: password already filled; click Log in if present
  agent-browser eval "(() => { const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.trim() === 'Log in'); if (b) { b.click(); return 'login-clicked'; } return 'no-login-btn'; })()"
  sleep 6
  STATE2=$(agent-browser eval "JSON.stringify({onb: location.href.includes('onboarding') || location.href.includes('/login'), limited: document.body.innerText.includes('temporarily limited')})" 2>/dev/null || echo "{}")
  echo "[x-reply] Post-login: $STATE2"
  if echo "$STATE2" | grep -q '"onb":true'; then
    echo "[x-reply] ERROR: still on login page after attempt"
    exit 2
  fi
fi

echo "[x-reply] Locating reply button on tweet"
agent-browser snapshot -i > /tmp/x-reply-snapshot.txt
REPLY_REF=$(grep -i 'button "Reply"' /tmp/x-reply-snapshot.txt | head -1 | grep -oP '\[ref=\K[^\]]+' | head -1)
if [ -z "$REPLY_REF" ]; then
  REPLY_REF=$(grep -iE '"Reply"' /tmp/x-reply-snapshot.txt | head -1 | grep -oP '\[ref=\K[^\]]+' | head -1)
fi
if [ -z "$REPLY_REF" ]; then
  echo "[x-reply] ERROR: reply button not found; dumping snapshot"
  grep -iE "reply|button" /tmp/x-reply-snapshot.txt | head -20
  exit 1
fi
echo "[x-reply] Reply button: $REPLY_REF"
agent-browser click "$REPLY_REF"
sleep 2

echo "[x-reply] Typing reply"
agent-browser snapshot -i > /tmp/x-reply-snapshot2.txt
COMPOSER_REF=$(grep -iE 'textbox|contenteditable' /tmp/x-reply-snapshot2.txt | grep -viE 'search|username|password' | head -1 | grep -oP '\[ref=\K[^\]]+' | head -1)
if [ -n "$COMPOSER_REF" ]; then
  agent-browser click "$COMPOSER_REF"
fi
agent-browser keyboard type "$REPLY_TEXT"
sleep 2

echo "[x-reply] Submitting"
agent-browser snapshot -i > /tmp/x-reply-snapshot3.txt
POST_REF=$(grep -iE 'button "(Post|Reply)"' /tmp/x-reply-snapshot3.txt | head -1 | grep -oP '\[ref=\K[^\]]+' | head -1)
if [ -n "$POST_REF" ]; then
  agent-browser click "$POST_REF"
else
  agent-browser press Tab
  agent-browser press Enter
fi
sleep 3

echo "[x-reply] Verifying"
agent-browser screenshot /tmp/x-reply-result.png
echo "[x-reply] Screenshot: /tmp/x-reply-result.png"
