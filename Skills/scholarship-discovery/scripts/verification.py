"""HTTP verification for scholarship application URLs.

Exports used by discovery_pipeline.link_recovery and the canonical runner:
  normalize_key(value) -> str
  default_fetcher(url) -> Response-like (url, status, content_type, body, title, links)
  verify_candidate(candidate, fetcher) -> {"score", "status", "final_url", "notes"}
  is_search_aggregator(url) -> bool
  is_application_page(title, body, links) -> bool
  same_opportunity(candidate, body, title) -> bool
"""
from __future__ import annotations

import re
import socket
import urllib.error
import urllib.request
from urllib.parse import urlparse

USER_AGENT = "ScholarSearch discovery pipeline/1.0 (+https://scholarsearch; verification bot)"
TIMEOUT = 15

BLOCKED_HOSTS = {
    "scholarships.com", "www.scholarships.com", "app.scholarships.com",
    "accessscholarships.com", "www.accessscholarships.com",
    "bold.org", "www.bold.org",
    "fastweb.com", "www.fastweb.com",
    "niche.com", "www.niche.com",
    "scholarships360.org", "www.scholarships360.org",
    "apps.apple.com", "play.google.com",
    "unigo.com", "www.unigo.com",
    "cappex.com", "www.cappex.com",
    "collegexpress.com", "www.collegexpress.com",
    "scholarshipowl.com", "www.scholarshipowl.com",
    "goingmerry.com", "www.goingmerry.com",
    "scholarships360.com",
    "facebook.com", "www.facebook.com", "x.com", "twitter.com", "instagram.com", "linkedin.com",
}

LISTING_PATH_RE = re.compile(
    r"/(by-(major|state|year|type|demographics)|category|categories|search|results|blog|our-blog|scholarships?(/|s/?$)?|directory|tags?)(/|$)",
    re.IGNORECASE,
)

APPLICATION_TERMS = re.compile(
    r"\b(apply|application|deadline|award|eligib|scholarship|fellowship|grant|submit|candidate|nominate)\b",
    re.IGNORECASE,
)

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
LINK_RE = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
SCRIPT_RE = re.compile(r"<(script|style|noscript)[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def is_search_aggregator(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return True
    if host in BLOCKED_HOSTS:
        return True
    return bool(LISTING_PATH_RE.search(urlparse(url).path or ""))


INSTALLER_HOSTS = {"apps.apple.com", "play.google.com"}


def is_installer_url(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower().removeprefix("www.")
        path = (urlparse(url).path or "").lower()
    except ValueError:
        return False
    return host in INSTALLER_HOSTS or bool(re.search(r"\.(apk|ipa|exe|msi|dmg|pkg|appx)(?:$|[?#])", path))


def page_text(body: str) -> str:
    return TAG_RE.sub(" ", SCRIPT_RE.sub(" ", body or ""))


def is_application_page(title: str, body: str, links) -> bool:
    text = f"{title or ''} {page_text(body)[:6000]}"
    return bool(APPLICATION_TERMS.search(text))


def same_opportunity(candidate: dict, body: str, title: str) -> bool:
    name = normalize_key(candidate.get("scholarship_name", ""))
    org = normalize_key(candidate.get("organization", ""))
    if not name:
        return False
    text = normalize_key(f"{title or ''} {page_text(body)[:8000]}")
    name_words = [w for w in name.split() if len(w) > 3]
    if not name_words:
        name_words = name.split()
    hits = sum(1 for w in name_words if w in text)
    return hits >= max(1, int(len(name_words) * 0.5)) or (org and org.split()[0] in text and hits >= 1)


def default_fetcher(url: str, timeout: int = TIMEOUT):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
            "Accept-Language": "en-US,en;q=0.8",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(400_000)
        charset = response.headers.get_content_charset() or "utf-8"
        body = raw.decode(charset, "replace")
        title_match = TITLE_RE.search(body)
        links = []
        base = response.geturl()
        for match in LINK_RE.findall(body)[:400]:
            try:
                from urllib.parse import urljoin
                links.append(urljoin(base, match))
            except ValueError:
                continue
        return type(
            "FetchedPage",
            (),
            {
                "url": base,
                "status": getattr(response, "status", 200),
                "content_type": response.headers.get("content-type", ""),
                "body": body,
                "title": re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "",
                "links": links,
            },
        )()


def verify_candidate(candidate: dict, fetcher) -> dict:
    url = str(candidate.get("application_url", "")).strip()
    notes = []
    if not url or not re.match(r"^https?://", url, re.IGNORECASE):
        return {"score": "D", "status": "invalid_url", "final_url": url or None, "notes": ["missing or non-http application_url"]}
    if is_search_aggregator(url):
        return {"score": "D", "status": "aggregator_or_listing", "final_url": url, "notes": [f"blocked source: {url}"]}

    try:
        response = fetcher(url)
    except urllib.error.HTTPError as exc:
        status = "temporarily_unavailable" if exc.code >= 500 or exc.code == 429 else "not_found"
        return {"score": "D", "status": status, "final_url": url, "notes": [f"HTTP {exc.code} on {url}"]}
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
        return {"score": "D", "status": "temporarily_unavailable", "final_url": url, "notes": [f"fetch failed: {exc}"]}

    final_url = str(getattr(response, "url", url))
    status = int(getattr(response, "status", 0) or 0)
    body = str(getattr(response, "body", "") or "")
    title = str(getattr(response, "title", "") or "")

    if status >= 400:
        status_name = "temporarily_unavailable" if status >= 500 or status == 429 else "not_found"
        return {"score": "D", "status": status_name, "final_url": final_url, "notes": [f"HTTP {status} after redirects: {final_url}"]}

    if is_search_aggregator(final_url):
        return {"score": "D", "status": "aggregator_or_listing", "final_url": final_url, "notes": [f"redirected to blocked destination: {final_url}"]}

    content_type = str(getattr(response, "content_type", "") or "")
    if content_type and not any(t in content_type for t in ("text/html", "application/xhtml", "text/plain")):
        return {"score": "D", "status": "needs_review", "final_url": final_url, "notes": [f"non-html content type: {content_type}"]}

    name_match = same_opportunity(candidate, body, title)
    app_like = is_application_page(title, body, getattr(response, "links", []))

    if name_match and app_like:
        score = "A"
        notes.append(f"name matched on page; application language present; final: {final_url}")
    elif app_like and len(body) > 2000:
        score = "B"
        notes.append(f"official page reachable with application language (name not confirmed); final: {final_url}")
    elif status < 400 and len(body) > 1000:
        score = "C"
        status = "needs_review"
        notes.append(f"reachable page but not confirmed as application page; final: {final_url}")
    else:
        score = "D"
        status = "needs_review"
        notes.append(f"page too thin to verify (len={len(body)}); final: {final_url}")

    return {"score": score, "status": status, "final_url": final_url, "notes": notes}
