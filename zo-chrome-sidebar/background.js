const DEFAULT_SETTINGS = {
  relayUrl: 'http://127.0.0.1:18720',
  browserControl: false,
  modelName: '',
  personaId: '',
};
const MAX_ROUNDS = 6;

const BROWSER_SYSTEM = `You are controlling the user's web browser through a Chrome extension sidebar. When you want to perform a browser action, output EXACTLY ONE fenced code block like this:
\`\`\`browser
{"action":"<name>","selector":"<css>","value":"<text>","url":"<url>","direction":"up|down","amount":<px>,"code":"<js>"}
\`\`\`
Available actions (include only the relevant fields):
- navigate: {"action":"navigate","url":"https://..."}
- click: {"action":"click","selector":"#id or .class"}
- fill: {"action":"fill","selector":"...","value":"text to type"}
- read: {"action":"read"}
- extract: {"action":"extract","selector":"..."}
- scroll: {"action":"scroll","direction":"down","amount":400}
- screenshot: {"action":"screenshot"}
- execute_js: {"action":"execute_js","code":"<js expression>"}
- page_info: {"action":"page_info"}
Output at most one action block per message. After I report the result you may issue the next action. Do not invent actions. When finished, reply to the user normally.`;

let sidebarPort = null;

function post(obj) { if (sidebarPort) sidebarPort.postMessage(obj); }

async function postAuth() {
  const s = await chrome.storage.local.get('zoToken');
  post({ type: 'auth', hasToken: !!s.zoToken });
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch(() => {});
});

chrome.runtime.onConnect.addListener((port) => {
  if (port.name !== 'sidebar') return;
  sidebarPort = port;
  port.onMessage.addListener((msg) => handlePortMessage(msg));
  port.onDisconnect.addListener(() => { if (sidebarPort === port) sidebarPort = null; });
  postAuth();
});

chrome.runtime.onMessage.addListener((msg) => {
  if (msg && msg.type === 'tokenCaptured' && msg.token) {
    chrome.storage.local.set({ zoToken: msg.token }, () => {
      const lastError = chrome.runtime.lastError;
      if (lastError) {
        console.error('Error saving token:', lastError);
        post({ type: 'error', text: 'Error saving token.' });
      } else {
        console.log('Token saved successfully.');
        post({ type: 'tokenCaptured', token: msg.token });
        postAuth();
      }
    });
  }
});

async function getSettings() {
  const s = await chrome.storage.local.get('settings');
  return { ...DEFAULT_SETTINGS, ...(s.settings || {}) };
}
async function saveSettings(settings) {
  await chrome.storage.local.set({ settings });
}
async function getConvId() {
  const r = await chrome.storage.local.get('conversationId');
  return r.conversationId || null;
}

async function handlePortMessage(msg) {
  switch (msg.type) {
    case 'getSettings':
      post({ type: 'settings', settings: await getSettings() });
      break;
    case 'saveSettings':
      await saveSettings(msg.settings);
      post({ type: 'settings', settings: await getSettings() });
      break;
    case 'login':
      chrome.tabs.create({ url: 'https://zo.computer/?t=settings&s=advanced' });
      break;
    case 'setToken':
      // Ensure token is saved if provided
      if (msg.token) {
        await chrome.storage.local.set({ zoToken: msg.token }, () => {
          const lastError = chrome.runtime.lastError;
          if (lastError) {
            console.error('Error saving token:', lastError);
            post({ type: 'error', text: `Error saving token: ${lastError.message}` });
          } else {
            console.log('Token saved successfully.');
            if (port) port.postMessage({ type: 'tokenCaptured' }); // Signal that token was captured
            if (port) port.postMessage({ type: 'auth', hasToken: true }); // Ensure auth status is updated
          }
        });
      } else {
        // If token is empty or missing, remove it and update auth status
        await chrome.storage.local.remove('zoToken');
        postAuth();
        post({ type: 'error', text: 'Token is empty.' });
      }
      break;
    case 'clearToken':
      await chrome.storage.local.remove('zoToken');
      postAuth();
      break;
    case 'send':
      await runTurn(msg.text);
      break;
    case 'resetChat':
      await chrome.storage.local.remove('conversationId');
      post({ type: 'chatReset' });
      break;
  }
}

async function runTurn(userText) {
  const settings = await getSettings();
  let convId = await getConvId();
  if (!convId) {
    convId = crypto.randomUUID();
    await chrome.storage.local.set({ conversationId: convId });
  }
  post({ type: 'user', text: userText });

  let input = settings.browserControl ? (BROWSER_SYSTEM + '\n\nUSER: ' + userText) : userText;
  let rounds = 0;
  while (true) {
    rounds++;
    if (rounds > MAX_ROUNDS) {
      post({ type: 'notice', text: 'Stopped after ' + MAX_ROUNDS + ' action rounds.' });
      break;
    }
    let full;
    try {
      full = await streamZo(input, settings, convId);
    } catch (e) {
      post({ type: 'error', text: e.message });
      break;
    }
    if (!settings.browserControl) break;
    const actions = parseBrowserBlocks(full);
    if (actions.length === 0) break;
    const results = [];
    for (const act of actions) {
      post({ type: 'actionStart', action: act });
      const r = await executeAction(act);
      post({ type: 'actionEnd', action: act, result: r.result, screenshot: r.screenshot });
      results.push('- ' + act.action + (act.selector ? '(' + act.selector + ')' : '') + ': ' + r.result);
    }
    const feedback = 'SYSTEM: Action results:\n' + results.join('\n') + '\n\nContinue helping the user (issue another action or reply).';
    input = BROWSER_SYSTEM + '\n\n' + feedback;
  }
}

async function streamZo(input, settings, convId) {
  const url = (settings.relayUrl || DEFAULT_SETTINGS.relayUrl).replace(/\/+$/, '') + '/zo/ask';
  const body = { input, conversation_id: convId, stream: true };
  if (settings.modelName) body.model_name = settings.modelName;
  if (settings.personaId) body.persona_id = settings.personaId;

  const { zoToken } = await chrome.storage.local.get('zoToken');
  const headers = { 'Content-Type': 'application/json' };
  if (zoToken) headers['X-Zo-Token'] = zoToken;

  post({ type: 'assistantStart' });
  let full = '';
  let res;
  try {
    res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });
  } catch (e) {
    throw new Error('Relay unreachable at ' + url + ': ' + e.message);
  }
  if (!res.ok) {
    const txt = await res.text().catch(() => '');
    throw new Error('Zo API error ' + res.status + ': ' + txt.slice(0, 300));
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let nl;
    while ((nl = buf.indexOf('\n')) >= 0) {
      const line = buf.slice(0, nl).trim();
      buf = buf.slice(nl + 1);
      if (!line) continue;
      if (line.startsWith('data:')) {
        const data = line.slice(5).trim();
        if (data === '[DONE]') continue;
        try {
          const json = JSON.parse(data);
          const tok =
            json.output ||
            (json.choices && json.choices[0] && json.choices[0].delta && json.choices[0].delta.content) ||
            (json.delta && json.delta.content) ||
            null;
          if (tok) { full += tok; post({ type: 'token', text: tok }); }
          else if (json.error) post({ type: 'error', text: String(json.error) });
        } catch (_) {
          if (data) { full += data; post({ type: 'token', text: data }); }
        }
      }
    }
  }
  post({ type: 'assistantEnd' });
  return full;
}

function parseBrowserBlocks(text) {
  const out = [];
  const re = /```browser\s*([\s\S]*?)```/g;
  let m;
  while ((m = re.exec(text))) {
    try { out.push(JSON.parse(m[1].trim())); } catch (_) { /* ignore bad block */ }
  }
  return out;
}

async function executeAction(act) {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return { result: 'ERROR: no active tab' };
    const tabId = tab.id;
    switch (act.action) {
      case 'navigate':
        if (!act.url) return { result: 'ERROR: navigate requires url' };
        await chrome.tabs.update(tabId, { url: act.url });
        return { result: 'navigated to ' + act.url };
      case 'click': {
        const r = await chrome.scripting.executeScript({ target: { tabId }, func: clickFn, args: [act.selector] });
        return { result: String(r[0] && r[0].result != null ? r[0].result : 'no result') };
      }
      case 'fill': {
        const r = await chrome.scripting.executeScript({ target: { tabId }, func: fillFn, args: [act.selector, act.value != null ? act.value : ''] });
        return { result: String(r[0] && r[0].result != null ? r[0].result : 'no result') };
      }
      case 'read': {
        const r = await chrome.scripting.executeScript({ target: { tabId }, func: readFn });
        return { result: String(r[0] && r[0].result != null ? r[0].result : '').slice(0, 6000) };
      }
      case 'extract': {
        const r = await chrome.scripting.executeScript({ target: { tabId }, func: extractFn, args: [act.selector] });
        const arr = (r[0] && r[0].result) || [];
        return { result: Array.isArray(arr) ? arr.slice(0, 50).join('\n') : String(arr) };
      }
      case 'scroll': {
        const amt = Number(act.amount) || 400;
        const r = await chrome.scripting.executeScript({ target: { tabId }, func: scrollFn, args: [act.direction || 'down', amt] });
        return { result: String(r[0] && r[0].result != null ? r[0].result : 'scrolled') };
      }
      case 'screenshot': {
        const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: 'png' });
        return { result: '[screenshot captured]', screenshot: dataUrl };
      }
      case 'execute_js': {
        const r = await chrome.scripting.executeScript({ target: { tabId }, func: jsFn, args: [act.code != null ? act.code : ''] });
        return { result: String(r[0] && r[0].result != null ? r[0].result : 'no result') };
      }
      case 'page_info': {
        const r = await chrome.scripting.executeScript({ target: { tabId }, func: infoFn });
        const o = (r[0] && r[0].result) || {};
        return { result: (o.url || '') + ' | ' + (o.title || '') };
      }
      default:
        return { result: 'ERROR: unknown action ' + act.action };
    }
  } catch (e) {
    return { result: 'ERROR: ' + e.message };
  }
}

function clickFn(selector) {
  const el = document.querySelector(selector);
  if (!el) return 'ERROR: no element for ' + selector;
  el.click();
  return 'clicked ' + selector;
}
function fillFn(selector, value) {
  const el = document.querySelector(selector);
  if (!el) return 'ERROR: no element for ' + selector;
  const proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
  const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
  setter.call(el, value);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
  return 'filled ' + selector;
}
function readFn() { return document.body.innerText; }
function extractFn(selector) {
  return Array.from(document.querySelectorAll(selector))
    .map((e) => (e.innerText || e.textContent || '').trim())
    .filter(Boolean);
}
function scrollFn(direction, amount) {
  window.scrollBy(0, direction === 'up' ? -amount : amount);
  return 'scrolled ' + direction;
}
function jsFn(code) {
  try { return String(eval(code)); } catch (e) { return 'ERROR: ' + e.message; }
}
function infoFn() { return { url: location.href, title: document.title }; }
