"""
tusk_lib.py — internal library for the tuskcentral skill.

Drives https://tuskcentral.ai from Python. There is no public API, so we
authenticate via Clerk and then talk directly to the same internal endpoints
the Angular SPA uses (/api/v2/chat/providers and /api/V2/Chat), using the
cookies/session captured by setup.py.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import uuid
import html
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

log = logging.getLogger("tusk")

TUSK_ORIGIN = "https://tuskcentral.ai"
TUSK_DATA_DIR = Path(os.path.expanduser("~/.tuskcentral"))
TUSK_SESSION_FILE = TUSK_DATA_DIR / "cookies.json"
TUSK_LAST_CHAT_FILE = TUSK_DATA_DIR / "last-chat.json"

DEFAULT_TIMEOUT = 120
DEFAULT_MODEL_LABEL = "Gemini 3.1 Pro Preview"  # premium but has a free sprint mode
DEFAULT_TONE = "technical"
DEFAULT_OPTION = "sprint"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class TuskModel:
    label: str
    key: str               # aiModelId
    display_name: str
    provider: str
    description: str
    is_premium: bool
    has_web_search: bool
    has_reasoning: bool
    input_modalities: list[str]
    output_modalities: list[str]
    options: list[dict]
    tones: list[dict]

    @property
    def option_keys(self) -> list[str]:
        return [o["key"] for o in self.options]

    @property
    def tone_keys(self) -> list[str]:
        return [t["key"] for t in self.tones]


@dataclass
class TuskReply:
    text: str
    html: str
    model: str
    model_id: str
    chat_id: str | None
    chat_log_id: str | None
    elapsed_sec: float
    raw: dict
    error: str | None = None        # non-null if the reply was a sign-up/credit wall
    truncated: bool = False


# ---------------------------------------------------------------------------
# Session handling
# ---------------------------------------------------------------------------


class TuskSessionMissing(RuntimeError):
    """Raised when no Clerk session is saved. Call setup.py first."""


class TuskSessionExpired(RuntimeError):
    """Raised when the saved session is rejected (Clerk session ended)."""


def _load_session() -> dict:
    if not TUSK_SESSION_FILE.exists():
        raise TuskSessionMissing(
            f"No session found at {TUSK_SESSION_FILE}. Run setup.py first."
        )
    return json.loads(TUSK_SESSION_FILE.read_text())


def _cookie_header_from_storage(storage: dict) -> str:
    """Build a Cookie header from a Playwright storage_state dict or flat cookies dict."""
    parts = []
    # List-of-cookie-objects format (Playwright storage_state.json, browser profile)
    cookie_list = storage.get("cookies", [])
    if not cookie_list:
        # Fallback: flat dict format (cookies.json from setup.py: {"name": "value", ...})
        for k, v in storage.items():
            parts.append(f"{k}={v}")
        return "; ".join(parts)
    for c in cookie_list:
        domain = c.get("domain", "")
        if domain and not domain.endswith("tuskcentral.ai"):
            continue
        parts.append(f"{c['name']}={c['value']}")
    return "; ".join(parts)


def _cookies_to_playwright_storage(storage: dict) -> dict:
    if not storage or not isinstance(storage, dict):
        return storage
    cookie_list = storage.get("cookies")
    if isinstance(cookie_list, list) and cookie_list:
        return storage
    out = {"cookies": [], "origins": []}
    for name, value in storage.items():
        out["cookies"].append({
            "name": name,
            "value": str(value),
            "domain": ".tuskcentral.ai",
            "path": "/",
            "expires": -1,
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax",
        })
    return out


def _request(
    method: str,
    path: str,
    *,
    body: dict | None = None,
    storage: dict | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict | str]:
    """Direct HTTP call to the Tusk API. Returns (status, parsed-or-raw)."""
    url = f"{TUSK_ORIGIN}{path}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Tuskcentral-Wrapper/1.0",
        "Accept": "application/json, text/plain, */*",
        "Origin": TUSK_ORIGIN,
        "Referer": f"{TUSK_ORIGIN}/?tusk_webview=1",
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    if storage is not None:
        cookie = _cookie_header_from_storage(storage)
        if cookie:
            headers["Cookie"] = cookie

    req = urlrequest.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urlrequest.urlopen(req, timeout=timeout)
        raw = resp.read().decode("utf-8", errors="replace")
        return resp.status, raw
    except HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        return e.code, raw
    except URLError as e:
        raise RuntimeError(f"Network error talking to {url}: {e}") from e


# ---------------------------------------------------------------------------
# Providers (model catalog)
# ---------------------------------------------------------------------------


def fetch_providers(storage: dict | None = None) -> list[TuskModel]:
    """Fetch the model catalog. Public endpoint — storage optional."""
    status, raw = _request("GET", "/api/v2/chat/providers", storage=storage)
    if status != 200:
        raise RuntimeError(f"GET /providers returned {status}: {raw[:300]}")
    data = json.loads(raw)
    return [_parse_model(p) for p in data.get("providers", [])]


def _parse_model(p: dict) -> TuskModel:
    return TuskModel(
        label=p["label"],
        key=p["key"],
        display_name=p.get("displayName", p["label"]),
        provider=p.get("providerName", "Unknown"),
        description=p.get("description", ""),
        is_premium=bool(p.get("isPremium", False)),
        has_web_search=bool(p.get("hasWebSearch", False)),
        has_reasoning=bool(p.get("hasReasoning", False)),
        input_modalities=p.get("inputModalities", []),
        output_modalities=p.get("outputModalities", []),
        options=p.get("options", []),
        tones=p.get("tones", []),
    )


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


SIGNUP_WALL_MARKERS = (
    "Sign up for a free account to use this model",
    "Sign in to use this model",
)


def _parse_ndjson_chat(raw: str) -> dict:
    """Parse a Tuskcentral chat response.

    The server streams NDJSON (one JSON object per line) where each line is
    a chunk: ``{"chatId": ..., "sessionId": ..., "content": "{\"isComplete\": false, \"content\": \"<html chunk>\"}"}``

    The outer object also has a ``content`` field whose *string value* is itself
    JSON-encoded; the actual streaming text lives in the innermost ``content``
    field, often split token-by-token.

    Returns a dict with keys:
        chat_id, session_id, log_id, model, text, html, chunks, is_complete
    """
    result = {
        "chat_id": None,
        "session_id": None,
        "log_id": None,
        "model": None,
        "text": "",
        "html": "",
        "chunks": [],
        "is_complete": False,
    }
    if not raw:
        return result
    final_inner: dict | None = None
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            outer = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(outer, dict):
            continue
        if outer.get("chatId"):
            result["chat_id"] = outer["chatId"]
        if outer.get("sessionId"):
            result["session_id"] = outer["sessionId"]
        if outer.get("chatLogId"):
            result["log_id"] = outer["chatLogId"]
        content_str = outer.get("content")
        if not isinstance(content_str, str) or not content_str:
            continue
        try:
            inner = json.loads(content_str)
        except json.JSONDecodeError:
            # Not all lines are double-encoded; ignore
            continue
        if not isinstance(inner, dict):
            continue
        if inner.get("model"):
            result["model"] = inner["model"]
        chunk_html = inner.get("content")
        if isinstance(chunk_html, str) and chunk_html:
            result["chunks"].append(chunk_html)
        if inner.get("isComplete"):
            result["is_complete"] = True
            final_inner = inner
    # Assemble final text. Prefer the final (isComplete=true) line; fall back
    # to concatenating the chunks.
    if final_inner is not None and isinstance(final_inner.get("content"), str):
        result["html"] = final_inner["content"]
    elif result["chunks"]:
        result["html"] = "".join(result["chunks"])
    result["text"] = _html_to_text(result["html"]) if result["html"] else ""
    return result


def _looks_like_wall(parsed: dict) -> tuple[str, str] | None:
    """Return (plain_text, html) of the wall message if the response is an
    auth/credit wall, else None. Unwraps the stringified inner JSON first."""
    chat_id = parsed.get("chatId")
    log_id = parsed.get("chatLogId")
    content = parsed.get("content", "")
    if not isinstance(content, str) or not content:
        return None
    try:
        inner = json.loads(content)
        html_body = inner.get("content", "") if isinstance(inner, dict) else ""
    except (json.JSONDecodeError, TypeError):
        html_body = content
    if not html_body:
        return None
    low = html_body.lower().strip()
    text_only = _html_to_text(html_body).strip()
    marker_hit = any(m in html_body for m in SIGNUP_WALL_MARKERS) or (
        "credits" in low and "required" in low
    )
    # Server returns content="." with null chatId/logId when blocked
    blocked_payload = chat_id is None and log_id is None and text_only in ("", ".", "…")
    if marker_hit:
        return _html_to_text(html_body) or text_only, html_body
    if blocked_payload:
        return (
            "Tuskcentral did not return a reply. "
            "Your session may have expired — re-run setup.py.",
            "<p>Tuskcentral did not return a reply. Your session may have expired — re-run setup.py.</p>",
        )
    return None


def _parse_reply_payload(content_str: str) -> tuple[str, str]:
    """The API returns a JSON-stringified inner object with HTML. Parse it."""
    try:
        inner = json.loads(content_str)
    except (json.JSONDecodeError, TypeError):
        return html.unescape(content_str), content_str
    html_body = inner.get("content", "") if isinstance(inner, dict) else ""
    if not html_body:
        return "", ""
    plain = _html_to_text(html_body)
    return plain, html_body


def _html_to_text(h: str) -> str:
    """Lightweight HTML → text. Keeps code blocks intact, drops tags otherwise."""
    # Preserve code blocks (replace with placeholders)
    code_blocks: list[str] = []
    def _stash(m):
        code_blocks.append(m.group(2))
        return f"\n```\n{len(code_blocks) - 1}\n```\n"
    h = re.sub(r"<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>", _stash, h, flags=re.DOTALL)
    # Inline code
    inlines: list[str] = []
    def _stash_inline(m):
        inlines.append(m.group(1))
        return f"\x00INLINE{len(inlines) - 1}\x00"
    h = re.sub(r"<code[^>]*>(.*?)</code>", _stash_inline, h, flags=re.DOTALL)
    # Block elements → newlines
    h = re.sub(r"</?(p|div|br|li|h[1-6]|tr)[^>]*>", "\n", h, flags=re.IGNORECASE)
    h = re.sub(r"</td[^>]*>", "\t", h, flags=re.IGNORECASE)
    # Strip remaining tags
    h = re.sub(r"<[^>]+>", "", h)
    # Unescape entities
    h = html.unescape(h)
    # Restore inline code
    for i, code in enumerate(inlines):
        h = h.replace(f"\x00INLINE{i}\x00", f"`{code}`")
    # Restore code blocks (the placeholder is the index, swap to real code)
    for i, code in enumerate(code_blocks):
        h = h.replace(f"```\n{i}\n```", f"```\n{code.strip()}\n```")
    # Collapse blank lines
    h = re.sub(r"\n{3,}", "\n\n", h)
    return h.strip()


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class TuskClient:
    """High-level client. Loads session lazily on first call."""

    def __init__(self, session_path: Path | None = None):
        self._storage: dict | None = None
        self._session_path = session_path or TUSK_SESSION_FILE
        # Persistent Playwright (lazily started on first chat call)
        self._pw = None
        self._pw_browser = None
        self._pw_page = None

    def __del__(self):
        # Best-effort cleanup if the user forgot to call close()
        try:
            self.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def _ensure_session(self) -> dict:
        if self._storage is None:
            self._storage = _load_session()
        return self._storage

    def list_models(self, *, refresh: bool = False) -> list[TuskModel]:
        """Returns the live model list. The catalog is public, but we pass
        storage anyway so cookies travel with the request."""
        return fetch_providers(self._ensure_session())

    def find_model(self, identifier: str | TuskModel) -> TuskModel:
        """Resolve by display label, label substring, or UUID. Also accepts a TuskModel."""
        if isinstance(identifier, TuskModel):
            return identifier
        models = self.list_models()
        ident = identifier.strip().lower()
        # UUID exact match first
        for m in models:
            if m.key.lower() == ident:
                return m
        # Exact label / display name
        for m in models:
            if m.label.lower() == ident or m.display_name.lower() == ident:
                return m
        # Substring match (prefer the most specific short match)
        scored: list[tuple[int, TuskModel]] = []
        for m in models:
            label_l = m.label.lower()
            if ident in label_l:
                scored.append((len(label_l) - len(ident), m))
        if not scored:
            raise ValueError(
                f"No model matched {identifier!r}. "
                f"Try --list-models to see the catalog."
            )
        scored.sort()
        return scored[0][1]

    def chat(
        self,
        text: str,
        *,
        model: str | None = None,
        model_id: str | None = None,
        option: str | None = None,
        tone: str | None = None,
        web_search: bool | None = None,
        reasoning: bool | None = None,
        chat_id: str | None = None,
        new_chat: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
        headless: bool = True,
    ) -> TuskReply:
        """Send a prompt and return the model's reply.

        Drives the real chat UI via Playwright (the only path that gets past
        the Clerk auth wall). Uses the saved storage state to skip sign-in.
        """
        if not text or not text.strip():
            raise ValueError("text must be non-empty")
        storage = self._ensure_session()
        models = self.list_models()
        if model_id:
            chosen = next((m for m in models if m.key.lower() == model_id.lower()), None)
            if not chosen:
                raise ValueError(f"No model with key {model_id!r}.")
        elif model:
            try:
                chosen = self.find_model(model)
            except ValueError:
                raise
        else:
            chosen = next((m for m in models if "Gemini 3.1 Pro Preview" in m.label), models[0])

        # Validate options/tones against the model
        opt = option or ("marathon" if chosen.is_premium else "sprint")
        if opt not in chosen.option_keys:
            raise ValueError(
                f"Model {chosen.label!r} has options {chosen.option_keys}, not {opt!r}."
            )
        tn = tone or DEFAULT_TONE
        if tn not in chosen.tone_keys:
            raise ValueError(
                f"Model {chosen.label!r} has tones {chosen.tone_keys}, not {tn!r}."
            )

        return _chat_via_playwright(
            text=text,
            model=chosen,
            option=opt,
            tone=tn,
            storage=storage,
            timeout=timeout,
            headless=headless,
            new_chat=new_chat,
            client=self,
        )

    def _find_model_by_id(self, model_id: str) -> TuskModel:
        for m in self.list_models():
            if m.key.lower() == model_id.lower():
                return m
        raise ValueError(f"No model with key {model_id!r}.")

    def _playwright_browser(self):
        """Lazy singleton: keep one browser alive across chat() calls."""
        if self._pw_browser is None:
            from playwright.sync_api import sync_playwright as _sp

            self._pw = _sp().start()
            self._pw_browser = self._pw.chromium.launch(
                headless=True, args=["--no-sandbox"])
        return self._pw_browser

    def close(self):
        """Shut down the persistent browser, if any."""
        if self._pw_browser is not None:
            try:
                self._pw_browser.close()
            except Exception:
                pass
            self._pw_browser = None
        if self._pw is not None:
            try:
                self._pw.stop()
            except Exception:
                pass
            self._pw = None


# ---------------------------------------------------------------------------
# Playwright-driven chat
# ---------------------------------------------------------------------------


from playwright.sync_api import sync_playwright, Page  # noqa: E402


def _chat_via_playwright(
    *,
    text: str,
    model: TuskModel,
    option: str,
    tone: str,
    storage: dict,
    timeout: int,
    headless: bool,
    new_chat: bool,
    client,
) -> TuskReply:
    """Drive the actual chat UI in Chromium. Returns the model's reply."""
    from playwright.sync_api import sync_playwright as _sp
    
    t0 = time.monotonic()
    
    # Lazy browser init
    browser = client._playwright_browser()
    context = browser.new_context(
        storage_state=_cookies_to_playwright_storage(storage),
        viewport={"width": 1280, "height": 800},
    )
    try:
        page = context.new_page()
        page.goto(
            f"{TUSK_ORIGIN}/chat",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        # Wait for the textarea to be ready
        page.wait_for_selector(
            "textarea#main-search-textarea, textarea",
            timeout=20000,
        )
        
        # Type message
        ta = page.locator("textarea#main-search-textarea, textarea").first
        ta.click()
        ta.fill(text)
        
        # Submit
        try:
            page.locator("button.submit-button").first.click(timeout=2000)
        except Exception:
            page.keyboard.press("Enter")
        
        # Wait for response
        deadline = time.monotonic() + timeout
        last_text = ""
        stable = 0
        while time.monotonic() < deadline:
            current = _read_last_assistant_message(page)
            if current == last_text and current:
                stable += 1
                if stable >= 2:
                    break
            else:
                stable = 0
                last_text = current
            time.sleep(0.7)
        
        elapsed = time.monotonic() - t0
        final = last_text or ""
        
        # Wall detection
        if not final or final in (".", "…") or "Sign up" in final:
            return TuskReply(
                text=f"No reply (wall). Re-run setup.py.", html="<p>No reply.</p>",
                model=model.label, model_id=model.key,
                chat_id=None, chat_log_id=None,
                elapsed_sec=elapsed, error="No reply.", raw=None,
            )
        
        return TuskReply(
            text=final, html=final,
            model=model.label, model_id=model.key,
            chat_id=None, chat_log_id=None,
            elapsed_sec=elapsed, raw=None,
        )
    finally:
        context.close()


def _ensure_model_selected(page, model: TuskModel) -> bool:
    """If a model picker is visible, select the requested model. Otherwise
    no-op (model is fixed in webview)."""
    try:
        # The picker usually has a trigger button with the current model name
        trigger = page.locator("button:has-text('Choose a model'), button[aria-label*='model' i]").first
        if not trigger.is_visible(timeout=1000):
            return True  # no picker, nothing to do
        trigger.click()
        page.wait_for_selector(f"text={model.label}", timeout=5000)
        page.locator(f"text={model.label}").first.click()
        time.sleep(0.3)
        return True
    except Exception as e:
        log.debug("model selector not used: %s", e)
        return True


def _read_last_assistant_message(page) -> str:
    """Read the most recent assistant message bubble's text content."""
    # Tuskcentral renders assistant turns in a specific class. Try a few selectors.
    selectors = [
        "[data-role='assistant']",
        ".assistant-message",
        ".message.assistant",
        "div[class*='assistant']",
    ]
    for sel in selectors:
        try:
            elements = page.locator(sel).all()
            if elements:
                return elements[-1].inner_text(timeout=2000).strip()
        except Exception:
            continue
    # Fallback: last "ai" or markdown div on the page
    try:
        all_msgs = page.locator(".message").all()
        if all_msgs:
            return all_msgs[-1].inner_text(timeout=2000).strip()
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Last-chat persistence
# ---------------------------------------------------------------------------


def _read_last_chat_id() -> str | None:
    if not TUSK_LAST_CHAT_FILE.exists():
        return None
    try:
        return json.loads(TUSK_LAST_CHAT_FILE.read_text()).get("chat_id")
    except (json.JSONDecodeError, OSError):
        return None


def _write_last_chat_id(chat_id: str) -> None:
    TUSK_DATA_DIR.mkdir(parents=True, exist_ok=True)
    TUSK_LAST_CHAT_FILE.write_text(json.dumps({"chat_id": chat_id, "ts": time.time()}))
