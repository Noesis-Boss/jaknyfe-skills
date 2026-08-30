"""Deterministic checks for official scholarship application destinations."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from urllib.parse import urlparse

AGGREGATORS = {"scholarships.com", "bold.org", "fastweb.com", "goingmerry.com", "niche.com", "scholarships360.org"}
INSTALLER_HOSTS = {"apps.apple.com", "play.google.com"}
FAILURE_WORDS = re.compile(r"404|page not found|not found|access denied|domain for sale|parked|coming soon|account suspended", re.I)
APPLICATION_WORDS = re.compile(r"apply|application|submit|submission|portal|enter|deadline|eligib", re.I)

def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")

def is_search_aggregator(url: str) -> bool:
    host = _host(url)
    return any(host == domain or host.endswith("." + domain) for domain in AGGREGATORS)

def is_installer_url(url: str) -> bool:
    host = _host(url)
    path = urlparse(url).path.lower()
    return host in INSTALLER_HOSTS or bool(re.search(r"\.(apk|ipa|exe|msi|dmg|pkg|appx)(?:$|[?#])", path))

def is_application_page(title: str, body: str, links: list[str]) -> bool:
    text = " ".join((title, body, " ".join(links)))
    return bool(APPLICATION_WORDS.search(text)) and not bool(FAILURE_WORDS.search(text[:10000]))

def same_opportunity(candidate: dict, page_text: str, page_title: str) -> bool:
    name = str(candidate.get("scholarship_name", "")).strip()
    tokens = [token for token in re.findall(r"[a-z0-9]+", name.lower()) if len(token) > 3]
    haystack = f"{page_title} {page_text}".lower()
    return len(tokens) == 0 or sum(token in haystack for token in tokens) >= max(1, len(tokens) // 2)

def verify_candidate(candidate: dict, fetcher) -> dict:
    checked_at = datetime.now(timezone.utc).isoformat()
    url = str(candidate.get("application_url", "")).strip()
    sponsor = _host(str(candidate.get("sponsor_url", ""))) or None
    if not url or is_search_aggregator(url) or is_installer_url(url):
        return {"status": "redirected_to_aggregator", "score": "reject", "finalUrl": None, "sponsorDomain": sponsor, "evidence": ["final destination is a search aggregator"], "checkedAt": checked_at}
    try:
        response = fetcher(url)
    except Exception as exc:
        return {"status": "temporarily_unavailable", "score": "C", "finalUrl": None, "sponsorDomain": sponsor, "evidence": [f"fetch failed: {exc}"], "checkedAt": checked_at}
    final_url = getattr(response, "url", url)
    body = str(getattr(response, "body", ""))
    title = str(getattr(response, "title", ""))
    status = int(getattr(response, "status", 0))
    content_type = str(getattr(response, "content_type", "text/html"))
    if is_search_aggregator(final_url):
        state = "redirected_to_aggregator"
        score = "reject"
    elif status in (404, 410):
        state, score = "not_found", "reject"
    elif status >= 500 or status == 0:
        state, score = "temporarily_unavailable", "C"
    elif "text/html" not in content_type and "application/pdf" not in content_type:
        state, score = "needs_review", "C"
    elif FAILURE_WORDS.search(body[:10000]) or not same_opportunity(candidate, body, title):
        state, score = "needs_review", "C"
    elif is_application_page(title, body, list(getattr(response, "links", []))):
        state, score = "verified", "A" if candidate.get("deadline") else "B"
    else:
        state, score = "needs_review", "C"
    return {"status": state, "score": score, "finalUrl": final_url, "sponsorDomain": sponsor, "evidence": [f"HTTP {status}", f"content-type {content_type}"], "checkedAt": checked_at}
