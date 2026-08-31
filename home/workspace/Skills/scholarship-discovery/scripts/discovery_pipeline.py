"""Queue-oriented discovery handoff with official URL verification."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import parse_qsl, urlencode, urlunparse

from link_recovery import recover_application_url
from verification import verify_candidate


def _key(candidate: dict) -> tuple[str, str]:
    name = " ".join(str(candidate.get("scholarship_name", "")).lower().split())
    sponsor = " ".join(str(candidate.get("organization", "")).lower().split())
    return name, sponsor


def normalize_candidate(candidate: dict) -> dict:
    result = dict(candidate)
    result["scholarship_name"] = " ".join(str(result.get("scholarship_name", "")).split())
    result["organization"] = " ".join(str(result.get("organization", "")).split())
    result["source_provenance"] = result.get("source_provenance") or result.get("source_url") or result.get("website")
    result["canonical_application_url"] = canonical_url(result.get("application_url", ""))
    return result


def canonical_url(value: str) -> str:
    parsed = urlparse(str(value).strip())
    if not parsed.scheme or not parsed.netloc:
        return ""
    query = [(key, value) for key, value in parse_qsl(parsed.query) if not key.lower().startswith(("utm_", "fbclid"))]
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower().removeprefix("www."), parsed.path.rstrip("/") or "/", "", urlencode(sorted(query)), ""))


def run_discovery(source_batch: list[dict], limit: int, fetcher, searcher) -> dict:
    report = {"discovered": len(source_batch), "normalized": 0, "verified": 0, "recovered": 0, "rejected": 0, "review": 0, "by_source": {}, "rejections": []}
    seen = set()
    seen_urls = set()
    for raw in source_batch[:limit]:
        candidate = normalize_candidate(raw)
        report["normalized"] += 1
        source = str(candidate.get("source") or candidate.get("source_url") or "unknown")
        counts = report["by_source"].setdefault(source, Counter())
        candidate_url = candidate.get("canonical_application_url", "")
        rejection_reason = ""
        if not candidate.get("scholarship_name") or not candidate.get("organization"):
            rejection_reason = "missing scholarship name or organization"
        elif _key(candidate) in seen:
            rejection_reason = "duplicate scholarship and organization"
        elif candidate_url and candidate_url in seen_urls:
            rejection_reason = "duplicate canonical application URL"
        if rejection_reason:
            report["rejected"] += 1
            counts["rejected"] += 1
            report["rejections"].append({"source": source, "candidate": candidate, "reason": rejection_reason})
            continue
        seen.add(_key(candidate))
        if candidate_url:
            seen_urls.add(candidate_url)
        result = verify_candidate(candidate, fetcher)
        if result["score"] in {"A", "B"}:
            report["verified"] += 1
            counts["verified"] += 1
            continue
        if result["status"] in {"temporarily_unavailable", "needs_review", "not_found"}:
            recovered = recover_application_url(candidate, fetcher, searcher)
            if recovered["recovered_url"]:
                recovered_candidate = dict(candidate, application_url=recovered["recovered_url"])
                recovered_result = verify_candidate(recovered_candidate, fetcher)
                if recovered_result["score"] in {"A", "B"}:
                    report["recovered"] += 1
                    report["verified"] += 1
                    counts["recovered"] += 1
                    continue
            if recovered["status"] == "timeout" or result["status"] == "temporarily_unavailable":
                report["review"] += 1
                counts["review"] += 1
                continue
        report["rejected"] += 1
        counts["rejected"] += 1
    report["by_source"] = {key: dict(value) for key, value in report["by_source"].items()}
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()
    candidates = json.loads(args.input.read_text())

    def fetcher(url):
        from urllib.request import Request, urlopen
        with urlopen(Request(url, headers={"User-Agent": "ScholarSearch discovery pipeline/1.0"}), timeout=12) as response:
            body = response.read().decode("utf-8", "replace")
            return type("Response", (), {"url": response.geturl(), "status": response.status, "content_type": response.headers.get("content-type", ""), "body": body, "title": "", "links": []})()

    report = run_discovery(candidates, args.limit, fetcher, lambda _: [])
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
