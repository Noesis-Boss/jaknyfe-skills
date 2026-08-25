"""Bounded recovery of official scholarship application URLs."""
from __future__ import annotations

import time
from collections import deque
from urllib.parse import urljoin, urlparse, urlunparse

from verification import is_application_page, is_search_aggregator, same_opportunity


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def _clean(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, ""))


def _links(response, base_url: str) -> list[str]:
    result = []
    for link in getattr(response, "links", []) or []:
        try:
            candidate = _clean(urljoin(base_url, str(link)))
            if urlparse(candidate).scheme in {"http", "https"}:
                result.append(candidate)
        except ValueError:
            continue
    return list(dict.fromkeys(result))


def recover_application_url(candidate: dict, fetcher, searcher, *, clock=time.monotonic, max_depth=3, max_pages=10, max_queries=2, budget_seconds=60) -> dict:
    original_url = str(candidate.get("application_url", "")).strip()
    sponsor_url = str(candidate.get("sponsor_url", "")).strip()
    sponsor_host = _host(sponsor_url)
    started = clock()
    attempts: list[dict] = []
    evidence: list[str] = []
    visited: set[str] = set()
    budget_exhausted = False
    queue = deque([(u, 0) for u in dict.fromkeys(filter(None, [_clean(original_url) if original_url else "", _clean(sponsor_url) if sponsor_url else ""]))])
    queries = 0

    def timed_out() -> bool:
        nonlocal budget_exhausted
        budget_exhausted = clock() - started >= budget_seconds
        return budget_exhausted

    while queue and len(visited) < max_pages and not timed_out():
        url, depth = queue.popleft()
        if url in visited or depth > max_depth:
            continue
        visited.add(url)
        try:
            response = fetcher(url)
            final_url = _clean(str(getattr(response, "url", url)))
            body = str(getattr(response, "body", ""))
            title = str(getattr(response, "title", ""))
            status = int(getattr(response, "status", 0))
            attempts.append({"url": url, "final_url": final_url, "status": status, "depth": depth})
            if is_search_aggregator(final_url):
                evidence.append(f"ignored aggregator destination: {final_url}")
                continue
            if status < 400 and _host(final_url) == sponsor_host and same_opportunity(candidate, body, title) and is_application_page(title, body, []):
                evidence.append(f"application language matched on {final_url}")
                return {"recovered_url": final_url, "attempts": attempts, "status": "recovered", "evidence": evidence}
            if status < 400 and depth < max_depth and _host(final_url) == sponsor_host:
                for link in _links(response, final_url):
                    if _host(link) == sponsor_host and link not in visited:
                        queue.append((link, depth + 1))
        except Exception as exc:
            attempts.append({"url": url, "error": str(exc), "depth": depth})

    while queries < max_queries and not timed_out() and sponsor_host:
        queries += 1
        query = f"site:{sponsor_host} {candidate.get('scholarship_name', '')} apply application deadline"
        try:
            results = searcher(query) or []
        except Exception as exc:
            evidence.append(f"search failed: {exc}")
            continue
        for result in results:
            url = _clean(str(result.get("url", result) if isinstance(result, dict) else result))
            if _host(url) == sponsor_host and url not in visited:
                queue.append((url, 0))
        while queue and len(visited) < max_pages and not timed_out():
            url, depth = queue.popleft()
            if url in visited or depth > max_depth:
                continue
            visited.add(url)
            try:
                response = fetcher(url)
                final_url = _clean(str(getattr(response, "url", url)))
                body = str(getattr(response, "body", ""))
                title = str(getattr(response, "title", ""))
                status = int(getattr(response, "status", 0))
                attempts.append({"url": url, "final_url": final_url, "status": status, "depth": depth, "query": query})
                if status < 400 and _host(final_url) == sponsor_host and same_opportunity(candidate, body, title) and is_application_page(title, body, []):
                    evidence.append(f"restricted search matched {final_url}")
                    return {"recovered_url": final_url, "attempts": attempts, "status": "recovered", "evidence": evidence}
            except Exception as exc:
                attempts.append({"url": url, "error": str(exc), "depth": depth, "query": query})

    status = "timeout" if budget_exhausted or timed_out() else "not_recovered"
    evidence.append("recovery budget exhausted" if status == "timeout" else "no qualifying official application page found")
    return {"recovered_url": None, "attempts": attempts, "status": status, "evidence": evidence}
