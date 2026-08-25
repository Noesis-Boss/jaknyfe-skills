"""Queue-oriented discovery handoff with official URL verification."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

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
    return result


def run_discovery(source_batch: list[dict], limit: int, fetcher, searcher) -> dict:
    report = {"discovered": len(source_batch), "normalized": 0, "verified": 0, "recovered": 0, "rejected": 0, "review": 0, "by_source": {}}
    seen = set()
    for raw in source_batch[:limit]:
        candidate = normalize_candidate(raw)
        report["normalized"] += 1
        source = str(candidate.get("source") or candidate.get("source_url") or "unknown")
        counts = report["by_source"].setdefault(source, Counter())
        if not candidate.get("scholarship_name") or not candidate.get("organization") or _key(candidate) in seen:
            report["rejected"] += 1
            counts["rejected"] += 1
            continue
        seen.add(_key(candidate))
        result = verify_candidate(candidate, fetcher)
        if result["score"] in {"A", "B"}:
            report["verified"] += 1
            counts["verified"] += 1
            continue
        if result["status"] in {"temporarily_unavailable", "needs_review", "not_found"}:
            recovered = recover_application_url(candidate, fetcher, searcher)
            if recovered["recovered_url"]:
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
