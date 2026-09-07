// Zo Sidebar — talks to the background service worker over a long-lived port.
// The background relays chat to the local relay and runs browser-control actions.

const $ = (id) => document.getElementById(id);

const messages = $('messages');
const composer = $('composer');
const input = $('input');
const sendBtn = $('send');
const newChatBtn = $('newChat');
const settingsBtn = $('settingsBtn');
const settingsPanel = $('settings');
const authStatus = $('authStatus');
const loginBtn = $('loginBtn');
const pasteBtn = $('pasteBtn');
const clearBtn = $('clearBtn');
const pasteWrap = $('pasteWrap');
const pasteToken = $('pasteToken');
const pasteSave = $('pasteSave');
const relayUrlInput = $('relayUrl');
const browserControlInput = $('browserControl');
const modelNameInput = $('modelName');
const personaIdInput = $('personaId');
const saveSettingsBtn = $('saveSettings');

let port = null;
let assistantEl = null;
let assistantBuffer = '';
let busy = false;
let pendingSettings = null;

// ---- Port connection (with auto-reconnect) ----
function connect() {
  port = chrome.runtime.connect({ name: 'sidebar' });
  port.onMessage.addListener(onMessage);
  port.onDisconnect.addListener(() => {
    port = null;
    updateAuth(false);
    addSystem('Lost connection to extension. Retrying…');
    setTimeout(connect, 1000);
  });
  // Ask background for current auth + settings.
  port.postMessage({ type: 'getSettings' });
}

// ---- Rendering helpers ----
function scrollToBottom() {
  messages.scrollTop = messages.scrollHeight;
}

function addMessage(role, text) {
  const el = document.createElement('div');
  el.className = 'msg ' + role;
  el.textContent = text;
  messages.appendChild(el);
  scrollToBottom();
  return el;
}

function addUser(text) {
  return addMessage('user', text);
}

function addAssistantChunk(text) {
  if (!assistantEl) {
    assistantEl = document.createElement('div');
    assistantEl.className = 'msg zo';
    messages.appendChild(assistantEl);
  }
  assistantBuffer += text;
  assistantEl.textContent = assistantBuffer;
  scrollToBottom();
}

function finishAssistant() {
  assistantEl = null;
  assistantBuffer = '';
}

function addSystem(text) {
  return addMessage('system', text);
}

function addError(text) {
  return addMessage('error', 'Error: ' + text);
}

function updateAuth(isLoggedIn) {
  if (isLoggedIn) {
    authStatus.textContent = '✓ Connected';
    authStatus.classList.add('ok');
    authStatus.classList.remove('warn');
    composer.classList.remove('hidden');
    pasteWrap.classList.add('hidden');
    clearBtn.classList.remove('hidden');
  } else {
    authStatus.textContent = 'Not connected';
    authStatus.classList.remove('ok');
    authStatus.classList.add('warn');
    composer.classList.add('hidden');
    pasteWrap.classList.remove('hidden');
    clearBtn.classList.add('hidden');
  }
}

// ---- Incoming messages from the background ----
function onMessage(msg) {
  switch (msg.type) {
    case 'auth':
      updateAuth(!!msg.hasToken);
      break;
    case 'settings':
      pendingSettings = msg.settings || null;
      applySettingsToForm(msg.settings);
      break;
    case 'tokenCaptured':
      updateAuth(true);
      addSystem('Token captured. You are connected.');
      break;
    case 'user':
      addUser(msg.text);
      break;
    case 'assistantStart':
      assistantEl = null;
      assistantBuffer = '';
      busy = true;
      setBusy(true);
      break;
    case 'token':
      addAssistantChunk(msg.text);
      break;
    case 'assistantEnd':
      finishAssistant();
      busy = false;
      setBusy(false);
      break;
    case 'actionStart': {
      const a = msg.action || {};
      addSystem('▶ ' + (a.action || 'action') + (a.selector ? ' ' + a.selector : ''));
      break;
    }
    case 'actionEnd':
      if (msg.screenshot) {
        const img = document.createElement('img');
        img.src = msg.screenshot;
        img.className = 'shot';
        messages.appendChild(img);
        scrollToBottom();
      }
      if (msg.result) addSystem('↳ ' + msg.result);
      break;
    case 'notice':
      addSystem(msg.text);
      break;
    case 'error':
      finishAssistant();
      addError(msg.text);
      busy = false;
      setBusy(false);
      break;
    case 'chatReset':
      messages.innerHTML = '';
      addSystem('New chat started.');
      break;
  }
}

function setBusy(isBusy) {
  sendBtn.disabled = isBusy;
  input.disabled = isBusy;
}

function applySettingsToForm(s) {
  if (!s) return;
  relayUrlInput.value = s.relayUrl || '';
  browserControlInput.checked = !!s.browserControl;
  modelNameInput.value = s.modelName || '';
  personaIdInput.value = s.personaId || '';
}

// ---- Outgoing actions ----
function sendPrompt() {
  const text = input.value.trim();
  if (!text || busy || !port) return;
  input.value = '';
  port.postMessage({ type: 'send', text });
}

function saveSettingsFromForm() {
  if (!port) return;
  const merged = Object.assign({}, pendingSettings || {}, {
    relayUrl: relayUrlInput.value.trim(),
    browserControl: browserControlInput.checked,
    modelName: modelNameInput.value.trim(),
    personaId: personaIdInput.value.trim(),
  });
  port.postMessage({ type: 'saveSettings', settings: merged });
  addSystem('Settings saved.');
}

// ---- Wire up UI ----
sendBtn.addEventListener('click', sendPrompt);
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendPrompt();
  }
});

newChatBtn.addEventListener('click', () => {
  if (port) port.postMessage({ type: 'resetChat' });
  messages.innerHTML = '';
  addSystem('New chat started.');
});

settingsBtn.addEventListener('click', () => {
  settingsPanel.classList.toggle('hidden');
});

loginBtn.addEventListener('click', () => {
  if (port) port.postMessage({ type: 'login' });
});

pasteBtn.addEventListener('click', () => {
  pasteWrap.classList.remove('hidden');
  pasteToken.focus();
});

pasteSave.addEventListener('click', () => {
  const token = (pasteToken.value || '').trim();
  if (!token) {
    addError('Token is empty.');
    return;
  }
  if (port) port.postMessage({ type: 'setToken', token });
  pasteToken.value = '';
  pasteWrap.classList.add('hidden');
  updateAuth(true);
  addSystem('Token saved. You are connected.');
});

clearBtn.addEventListener('click', () => {
  if (port) port.postMessage({ type: 'clearToken' });
  updateAuth(false);
  addSystem('Token cleared.');
});

saveSettingsBtn.addEventListener('click', saveSettingsFromForm);

// Start hidden until auth state is known.
composer.classList.add('hidden');
connect();
