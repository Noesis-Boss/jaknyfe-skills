#!/usr/bin/env python3
"""Query-matrix discovery: combinatorial web searches feeding the strict A/B gate.

Pipeline: query matrix -> DuckDuckGo -> landing URLs -> multi_channel.candidates()
depth-1 crawl -> verify_candidate (A/B) -> guarded insert into both DBs.
Bounded by --queries, --search-deadline, --verify-deadline.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from urllib.parse import unquote
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db_safety import make_backup
from gen_candidates2 import duckduckgo_search
from multi_channel_discover import DBS, candidates, is_installer_url, is_search_aggregator, verified
from verification import verify_candidate
from multi_channel_discover import fetch
from urllib.parse import urlparse

DEMOGRAPHICS = [
    "first generation college student", "women in STEM", "nursing student", "veteran dependent",
    "single parent", "Hispanic student", "Black student", "Native American student",
    "foster youth", "nontraditional student", "community college transfer", "student with disability",
    "diabetes", "LGBTQ student", "asian american student", "rural student",
    "first responder dependent", "left handed", "vegan", "tall",
    "redhead", "twin", "eagle scout", "girl scout",
]
STATES = ["Arizona", "Texas", "California", "Florida", "New York", "Georgia", "Ohio", "Michigan", "North Carolina", "Washington"]
SPONSORS = ["civic organization", "professional association", "labor union", "credit union",
            "utility company", "foundation", "fraternal organization", "employer"]

REPORT_PATH = Path(__file__).with_name("query_matrix_report.json")

SCHOL_WORDS = re.compile(r"scholarships?|fellowship|bursary|award|grant", re.I)
JUNK_NAME = re.compile(r"\b(skip to content|read more|learn more|click here|view here|terms|privacy|recipients?|winners?|congratulations|faq|about us|contact us|donate|menu|home page|subscribe|sign (in|up)|apply now|philosophy|processing|policy|procedures|checklist|directory|hub|portal|find more|i have an?|share a|how to|guide to|list of|state awards|top \d+|best \d+)\b", re.I)
EXPIRED_YEAR = re.compile(r"\b(20[0-1][0-9]|2020|2021|2022|2023|2024|2025)\b")
INDEX_NAME = re.compile(r"^[A-Za-z'\- ]{0,40}scholarships$", re.I)
JUNK_PATH = re.compile(r"(/category/|/(terms|privacy|recipients?|winners?|past-winners|archive|news|blog|press|faq|about|contact|donate|login|signin)(/|$|\.)|/scholarships?/?$|/fellowships?/?$|/awards?/?$|/grants?/?$)", re.I)
BLOCKED_DOMAINS = {
    "bigfuture.collegeboard.org", "studentscholarships.org",
    "scholarship-search.collegerecon.com", "collegerecon.com",
    "azstudentopportunityhub.org", "studentopportunityhub.org",
    "scholarships360.org", "raise.me", "cappex.com", "collegexpress.com",
    "unigo.com", "scholarshipowl.com", "scholarsanta.com", "tun.com",
    "practicaladultinsights.com", "globalindianschool.org", "accessscholarships.com", "scholarshipbuddytexas.com", "scholarshipbud.com", "instagram.com", "tiktok.com", "x.com", "twitter.com", "youtube.com", "facebook.com", "linkedin.com", "scholarshipsedge.com", "scholarshipsandgrants.us", "scholarshipamerica.org",
    "consumer.ftc.gov", "usnews.com", "forbes.com", "nerdwallet.com",
    "scholarshipbuddy.com", "awardscholar.com", "research.com",
    "ngwebsolutions.com", "edumed.org", "blogs.colum.edu", "blogs.uofi.uic.edu", "form.jotform.com", "onlinedegree.com", "blackcollegescholarships.com",
}
BROWSE_URL = re.compile(r"[?&](q|query|search|cat|category|page|p)=")
# Nav/footer/page-furniture names that slip through the generic filters.
GENERIC_NAME = re.compile(r"^(scholarship (policies|fund|finder|universe|donor|appeal|info(\.html)?|thank you letter|application)|scholarships?\s*(&|and)\s*(grants|aid)|costs,?\s*scholarships|i'?m? ?a? ?scholarship (donor|fund)|apply (for )?grants|go to scholarship|browse\?|sam\.gov|submit a scholarship|scholarship resources|local scholarship|state and school grants|about the scholarship|scholarships? (by|for) (organizations|education|region|state|women|students)|undergraduate/?bachelor'?s?|scholarship guide|common scholarships|become a scholarship|go to the official)\b", re.I)
NEWSY_NAME = re.compile(r"\$\d|\b(million|billion|sweepstak\w*|is offering)\b|https?://|[\U0001F000-\U0001FAFF\u2600-\u27BF]|\u00b7", re.I)
FURNITURE_NAME = re.compile(r"^\s*(about|add|new here|find your|scholarship (login|matches?|match registration|manager)|transfer scholarships|types? of scholarships|apply (for the|on) |become a|our scholarships|scholarship (faq|rules|regulations|portal)|scholarships? (and|&) (financial aid|resources)|tribal scholarship organizations|now accepting)\b" , re.I)
MANAGER_NAME = re.compile(r"\b(manager|registration)\b", re.I)


def is_junky_name(name: str) -> bool:
    n = re.sub(r"^(previous|next):\s*", "", name.strip(), flags=re.I)
    if len(n) < 10 or len(n) > 160:
        return True
    if not SCHOL_WORDS.search(n) or JUNK_NAME.search(n) or EXPIRED_YEAR.search(n):
        return True
    if FURNITURE_NAME.match(n) or MANAGER_NAME.search(n) or INDEX_NAME.match(n) or GENERIC_NAME.match(n) or NEWSY_NAME.search(n):
        return True
    if n.lower() in {"scholarships", "scholarship"} or n.rstrip().endswith("?"):
        return True
    return bool(re.fullmatch(r"[a-z0-9\-]+\.(com|org|net|edu|gov|us|io)", n.lower()))


def is_junky_url(u: str) -> bool:
    p_ = urlparse(u)
    host = p_.netloc.lower().removeprefix("www.")
    if any(host == d or host.endswith("." + d) for d in BLOCKED_DOMAINS):
        return True
    if p_.path in ("", "/") and not p_.query:
        return True  # bare-domain homepage, not an application page
    return bool(JUNK_PATH.search(p_.path)) or bool(BROWSE_URL.search(u))


def norm_url(u: str) -> str:
    return u.split("#", 1)[0].rstrip("/")


def build_queries(limit: int) -> list[str]:
    queries: list[str] = []
    demos = DEMOGRAPHICS.copy()
    states = STATES.copy()
    # Round-robin demographic x state for coverage, then sponsor + site: variants.
    for i in range(max(len(demos), len(STATES))):
        d = demos[i % len(demos)]
        s = states[i % len(states)]
        queries.append(f"{d} scholarship {s} 2026 apply deadline")
        queries.append(f'"{d}" scholarship site:.edu apply')
        if len(queries) >= limit:
            return queries[:limit]
    for sp in SPONSORS:
        queries.append(f"{sp} scholarships 2026 application official")
        if len(queries) >= limit:
            break
    return queries[:limit]


def existing_urls_and_hashes() -> tuple[set, set]:
    urls, hashes = set(), set()
    for db in DBS:
        try:
            conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            urls |= {r[0] for r in conn.execute("SELECT application_url FROM scholarships WHERE active != 0")}
            hashes |= {r[0] for r in conn.execute("SELECT name_hash FROM scholarships WHERE active != 0")}
            conn.close()
        except sqlite3.Error:
            pass
    return urls, hashes


def name_hash(name: str) -> str:
    return hashlib.md5(re.sub(r"\W", "", name.lower()).encode()).hexdigest()


def _unquote_url(url: str) -> str:
    for _ in range(2):
        if "%3A%2F%2F" in url or "%2" in url:
            url = unquote(url)
        else:
            break
    return url


def candidate_from_search_result(title: str, url: str, query: str) -> dict | None:
    if not title or not url.startswith("http"):
        return None
    url = _unquote_url(url)
    if is_search_aggregator(url) or is_installer_url(url):
        return None
    org = re.sub(r"^www\.", "", re.sub(r"/.*$", "", re.sub(r"^https?://", "", url)))
    return {
        "scholarship_name": title[:180],
        "organization": org,
        "application_url": url,
        "source": f"query-matrix-{date.today()}",
        "source_url": query,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--queries", type=int, default=60)
    p.add_argument("--crawl-per-query", type=int, default=3)
    p.add_argument("--search-deadline", type=float, default=120)
    p.add_argument("--verify-deadline", type=float, default=150)
    p.add_argument("--verify-cap", type=int, default=400, help="Max candidates verified per run.")
    p.add_argument("--commit", action="store_true", help="Actually insert; without this, report only.")
    a = p.parse_args()

    queries = build_queries(a.queries)
    known_urls, known_hashes = existing_urls_and_hashes()
    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "queries_run": len(queries),
        "search_results": 0,
        "query_empty": 0,
        "skipped": {"aggregator_installer": 0, "already_in_db": 0},
        "landing_urls_crawled": 0,
        "detail_candidates": 0,
        "verification": {"candidates": 0, "A": 0, "B": 0, "C": 0, "reject": 0},
        "accepted": [],
        "inserted": {},
        "commit": bool(a.commit),
    }

    search_started = time.monotonic()
    search_deadline = search_started + a.search_deadline
    landing: list[dict] = []
    seen_landing = set()
    for qi, q in enumerate(queries):
        if time.monotonic() >= search_deadline:
            break
        results = duckduckgo_search(q)
        report["search_results"] += len(results)
        if not results:
            report["query_empty"] += 1
            time.sleep(4.0)
            continue
        taken = 0
        for r in results:
            if taken >= a.crawl_per_query:
                break
            c = candidate_from_search_result(r.get("title", ""), r.get("url", ""), q)
            if c is None:
                report["skipped"]["aggregator_installer"] += 1
                continue
            url = c["application_url"]
            if url in seen_landing:
                continue
            if url in known_urls or name_hash(c["scholarship_name"]) in known_hashes:
                report["skipped"]["already_in_db"] += 1
                continue
            seen_landing.add(url)
            landing.append(c)
            taken += 1
        time.sleep(2.0)

    verify_started = time.monotonic()
    verify_deadline = verify_started + a.verify_deadline
    accepted: list[dict] = []
    pool = ThreadPoolExecutor(max_workers=10)
    # Stage 1: crawl landing pages for detail/application links (depth-1).
    def crawl(c: dict) -> list[dict]:
        return candidates("query-matrix", c["organization"], c["application_url"], deadline=verify_deadline)
    detail_jobs = {pool.submit(crawl, c): c for c in landing[: max(1, a.queries * a.crawl_per_query)]}
    detail: list[dict] = []
    try:
        for f in as_completed(detail_jobs, timeout=max(0.01, verify_deadline - time.monotonic())):
            try:
                out = f.result()
            except Exception:
                out = []
            report["landing_urls_crawled"] += 1
            detail.extend(out)
    except TimeoutError:
        pass
    finally:
        for f in detail_jobs:
            f.cancel()
        pool.shutdown(wait=False, cancel_futures=True)
    report["detail_candidates"] = len(detail)

    # Stage 2: strict A/B verification (single scored pass) of detail candidates.
    verify_pool = ThreadPoolExecutor(max_workers=12)
    verify_set = detail if detail else landing
    per_host: dict[str, int] = {}
    filtered: list[dict] = []
    seen_urls: set[str] = set()
    seen_norm: set[str] = set()
    for c in verify_set:
        c["scholarship_name"] = re.sub(r"^(previous|next):\s*", "", c["scholarship_name"].strip(), flags=re.I)
        c["application_url"] = norm_url(c["application_url"])
        u = c["application_url"]
        norm = re.sub(r"\b20\d\d\b", "", c["scholarship_name"].lower())
        norm = re.sub(r"\W+", "", norm)
        if u in seen_urls or is_junky_name(c["scholarship_name"]) or is_junky_url(u):
            continue
        if norm in seen_norm:
            continue
        host = urlparse(u).netloc.lower()
        c["organization"] = re.sub(r"^www\.", "", host)
        if per_host.get(host, 0) >= 6:
            continue
        per_host[host] = per_host.get(host, 0) + 1
        seen_urls.add(u)
        seen_norm.add(norm)
        filtered.append(c)
    report["filtered_junk"] = len(verify_set) - len(filtered)
    verify_set = filtered[: a.verify_cap]

    def score_one(c: dict) -> str:
        def real_fetch(url):
            final, html = fetch(url, 10)
            from types import SimpleNamespace
            return SimpleNamespace(url=final, status=200 if html else 0, content_type="text/html", title="", body=html, links=[])
        try:
            return verify_candidate(c, real_fetch)["score"]
        except Exception:
            return "reject"

    scores = {"A": 0, "B": 0, "C": 0, "reject": 0}
    checks = {verify_pool.submit(score_one, c): c for c in verify_set}
    try:
        for f in as_completed(checks, timeout=max(0.01, verify_deadline - time.monotonic())):
            c = checks[f]
            try:
                s = f.result()
            except Exception:
                s = "reject"
            scores[s if s in scores else "reject"] += 1
            if s in ("A", "B"):
                accepted.append(c)
    except TimeoutError:
        for f in checks:
            f.cancel()
    finally:
        verify_pool.shutdown(wait=False, cancel_futures=True)
    report["verification"] = {"candidates": len(verify_set), **scores}

    report["accepted"] = [
        {"name": c["scholarship_name"], "org": c["organization"], "url": c["application_url"]}
        for c in accepted
    ]

    if a.commit and accepted:
        for db in DBS:
            make_backup(db)
        for db in DBS:
            from multi_channel_discover import insert
            report["inserted"][db] = insert(accepted, db)

    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "accepted"}, indent=2))


if __name__ == "__main__":
    main()
