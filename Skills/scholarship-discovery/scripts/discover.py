#!/usr/bin/env python3
"""
Scholarship Discovery Skill - canonical global batch runner.

Usage:
    python3 discover.py --limit 200 [--candidates research_batch.json] [--report report.json]

Discovers new scholarships from a research candidate file, HTTP-verifies every
application URL (following redirects, recording final destination), deduplicates
against BOTH ScholarSearch databases via name_hash(name, organization) and exact
application_url, and inserts verified non-duplicates into both databases.

Never fabricates records. Shortfalls are reported with reasons.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from link_recovery import recover_application_url
from verification import default_fetcher, normalize_key, verify_candidate

DB_PATHS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

INSERT_SQL = """
INSERT INTO scholarships (
    source, source_id, scholarship_name, organization, organization_type,
    description, eligibility, amount_min, amount_max, amount_display,
    deadline, application_url, form_url, email, phone, address, website,
    category, education_level, field_of_study, state_restriction,
    gpa_min, citizenship, ethnicity, gender, military_affiliation,
    url_status, last_checked, link_notes, name_hash, active,
    verification_score, verification_method, source_provenance
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

COLUMNS = 33


def name_hash(name: str, organization: str) -> str:
    payload = f"{normalize_key(name)}||{normalize_key(organization)}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def load_known(db_path: str):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    urls = {r[0] for r in conn.execute("SELECT application_url FROM scholarships WHERE application_url IS NOT NULL")}
    hashes = {r[0] for r in conn.execute("SELECT name_hash FROM scholarships WHERE name_hash IS NOT NULL")}
    conn.close()
    return urls, hashes


def insert_all(record: dict) -> int:
    inserted = 0
    for db_path in DB_PATHS:
        conn = sqlite3.connect(db_path, timeout=30)
        try:
            conn.execute(INSERT_SQL, tuple(record.get(col) for col in COLUMNS_LIST))
            conn.commit()
            inserted += 1
        finally:
            conn.close()
    return inserted


COLUMNS_LIST = [
    "source", "source_id", "scholarship_name", "organization", "organization_type",
    "description", "eligibility", "amount_min", "amount_max", "amount_display",
    "deadline", "application_url", "form_url", "email", "phone", "address", "website",
    "category", "education_level", "field_of_study", "state_restriction",
    "gpa_min", "citizenship", "ethnicity", "gender", "military_affiliation",
    "url_status", "last_checked", "link_notes", "name_hash", "active",
    "verification_score", "verification_method", "source_provenance",
]

INSERT_SQL = """
INSERT INTO scholarships (
    source, source_id, scholarship_name, organization, organization_type,
    description, eligibility, amount_min, amount_max, amount_display,
    deadline, application_url, form_url, email, phone, address, website,
    category, education_level, field_of_study, state_restriction,
    gpa_min, citizenship, ethnicity, gender, military_affiliation,
    url_status, last_checked, link_notes, name_hash, active,
    verification_score, verification_method, source_provenance
) VALUES (%s)
""" % ",".join(["?"] * len(COLUMNS_LIST))


def run(candidates: list, limit: int, fetcher, searcher) -> dict:
    known_urls, known_hashes = {}, {}
    for db_path in DB_PATHS:
        u, h = load_known(db_path)
        known_urls[db_path] = u
        known_hashes[db_path] = h

    report = {
        "run_date": datetime.now(timezone.utc).isoformat(),
        "target": limit,
        "candidates": len(candidates),
        "added": 0,
        "duplicates": 0,
        "failed_link": 0,
        "rejected": 0,
        "recovered": 0,
        "remaining_to_target": limit,
        "by_source": Counter(),
        "by_region": Counter(),
        "rejected_detail": Counter(),
        "inserted": [],
    }

    seen_names = set()
    fetch_errors = Counter()

    for raw in candidates:
        if report["added"] >= limit:
            break

        name = " ".join(str(raw.get("scholarship_name", "")).split())
        org = " ".join(str(raw.get("organization", "")).split())
        if not name or not org:
            report["rejected"] += 1
            report["rejected_detail"]["missing_name_or_org"] += 1
            continue

        key = name_hash(name, org)
        if key in seen_names or any(key in known_hashes[p] for p in DB_PATHS):
            report["duplicates"] += 1
            report["rejected_detail"]["name_hash_duplicate"] += 1
            continue

        result = verify_candidate(raw, fetcher)

        if result["status"] in {"temporarily_unavailable", "needs_review", "not_found"} and not result["score"].startswith(("A", "B")):
            recovered = recover_application_url(raw, fetcher, searcher)
            if recovered["recovered_url"]:
                retry = dict(raw, application_url=recovered["recovered_url"])
                retry_result = verify_candidate(retry, fetcher)
                if retry_result["score"] in {"A", "B"}:
                    result = retry_result
                    report["recovered"] += 1

        if result["score"] not in {"A", "B"}:
            if result["status"] in {"temporarily_unavailable", "not_found"}:
                report["failed_link"] += 1
                fetch_errors[result["notes"][0] if result["notes"] else result["status"]] += 1
            else:
                report["rejected"] += 1
            report["rejected_detail"][result["status"]] += 1
            continue

        final_url = result["final_url"]
        if any(final_url in known_urls[p] for p in DB_PATHS):
            report["duplicates"] += 1
            report["rejected_detail"]["url_duplicate"] += 1
            continue

        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        record = {
            "source": raw.get("source") or "web_discovery",
            "source_id": raw.get("source_id") or f"disc_{now.replace('-', '').replace(':', '')}_{report['added']}",
            "scholarship_name": name,
            "organization": org,
            "organization_type": raw.get("organization_type") or "Other",
            "description": raw.get("description"),
            "eligibility": raw.get("eligibility"),
            "amount_min": raw.get("amount_min"),
            "amount_max": raw.get("amount_max"),
            "amount_display": raw.get("amount_display") or "Varies",
            "deadline": raw.get("deadline"),
            "application_url": final_url,
            "form_url": final_url,
            "email": raw.get("email"),
            "phone": raw.get("phone"),
            "address": raw.get("address"),
            "website": raw.get("website") or final_url,
            "category": raw.get("category") or "Academic",
            "education_level": raw.get("education_level") or "Undergraduate",
            "field_of_study": raw.get("field_of_study"),
            "state_restriction": raw.get("state_restriction"),
            "gpa_min": raw.get("gpa_min"),
            "citizenship": raw.get("citizenship"),
            "ethnicity": raw.get("ethnicity"),
            "gender": raw.get("gender"),
            "military_affiliation": raw.get("military_affiliation"),
            "url_status": "verified",
            "last_checked": now,
            "link_notes": f"Verified reachable destination: {final_url}. Score {result['score']}. " + "; ".join(result["notes"]),
            "name_hash": key,
            "active": 1,
            "verification_score": result["score"],
            "verification_method": "http_direct",
            "source_provenance": raw.get("source_provenance") or raw.get("source_url") or final_url,
        }

        if insert_all(record) == len(DB_PATHS):
            for p in DB_PATHS:
                known_urls[p].add(final_url)
                known_hashes[p].add(key)
            report["added"] += 1
            report["remaining_to_target"] = limit - report["added"]
            report["by_source"][record["source"]] += 1
            report["by_region"][raw.get("region") or "unspecified"] += 1
            report["inserted"].append({
                "scholarship_name": name,
                "organization": org,
                "amount_display": record["amount_display"],
                "deadline": record["deadline"],
                "education_level": record["education_level"],
                "region": raw.get("region") or "unspecified",
                "source": record["source"],
                "application_url": final_url,
                "verification_score": result["score"],
            })

    report["remaining_to_target"] = limit - report["added"]
    report["by_source"] = dict(report["by_source"])
    report["by_region"] = dict(report["by_region"])
    report["rejected_detail"] = dict(report["rejected_detail"])
    report["fetch_errors"] = dict(fetch_errors)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--candidates", type=Path, default=Path(__file__).parent / "research_batch.json")
    parser.add_argument("--report", type=Path, default=Path(__file__).parent / "discovery_report.json")
    parser.add_argument("--region", default=None)
    args = parser.parse_args()

    candidates = json.loads(args.candidates.read_text())
    if args.region:
        for c in candidates:
            c.setdefault("region", args.region)

    fetcher = default_fetcher
    searcher = lambda query: []

    report = run(candidates, args.limit, fetcher, searcher)

    totals = {}
    for db_path in DB_PATHS:
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            totals[db_path] = conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
            conn.close()
        except Exception as exc:
            totals[db_path] = f"error: {exc}"
    report["db_totals_after"] = totals

    args.report.write_text(json.dumps(report, indent=2, default=str))
    print(json.dumps({k: v for k, v in report.items() if k != "inserted"}, indent=2, default=str))
    print(f"Top results: {json.dumps(report['inserted'][:10], indent=2)}")


if __name__ == "__main__":
    main()
