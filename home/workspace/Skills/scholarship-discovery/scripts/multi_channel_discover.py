#!/usr/bin/env python3
"""Discover scholarship opportunities from official university, sponsor, association, and government sources."""
from __future__ import annotations

import argparse, hashlib, json, re, sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from db_safety import guarded_connection, make_backup
from verification import is_installer_url, is_search_aggregator, verify_candidate

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]
SOURCES = {
    "universities": [
        ("Harvard", "https://college.harvard.edu/financial-aid"),
        ("MIT", "https://sfs.mit.edu/undergraduate-students/undergraduate-admissions/"),
        ("Stanford", "https://financialaid.stanford.edu/undergrad/"),
        ("Princeton", "https://finaid.princeton.edu/how-aid-works"),
        ("UC Berkeley", "https://financialaid.berkeley.edu/types-of-aid/scholarships/"),
        ("University of Michigan", "https://finaid.umich.edu/scholarships/"),
        ("Ohio State", "https://undergrad.osu.edu/affordability-financial-aid/scholarships"),
        ("University of Arizona", "https://financialaid.arizona.edu/types-aid/scholarships"),
    ],
    "sponsors": [
        ("Coca-Cola Scholars", "https://www.coca-colascholarsfoundation.org/apply/"),
        ("Burger King Foundation", "https://burgerkingfoundation.org/scholarships/"),
        ("GE Reagan Foundation", "https://www.reaganfoundation.org/education/scholarship-programs/ge-reagan-foundation-scholarship-program/"),
        ("Horatio Alger Association", "https://horatioalger.org/scholarships-and-services/"),
        ("Jack Kent Cooke Foundation", "https://www.jkcf.org/our-scholarships/"),
        ("Elks National Foundation", "https://www.elks.org/scholars/scholarships/mvs.cfm"),
    ],
    "associations": [
        ("American Nurses Foundation", "https://www.nursingworld.org/foundation/scholarships/"),
        ("American Chemical Society", "https://www.acs.org/education/acs-scholars.html"),
        ("Society of Women Engineers", "https://swe.org/scholarships/"),
        ("American Legion", "https://www.legion.org/scholarships"),
        ("American Psychological Association", "https://www.apa.org/apf/funding/scholarships"),
        ("National Society of Black Engineers", "https://www.nsbe.org/scholarships"),
    ],
    "government_nonprofit": [
        ("Federal Student Aid", "https://studentaid.gov/understand-aid/types/scholarships"),
        ("Arizona Community Foundation", "https://www.azfoundation.org/scholarships/"),
        ("UNCF", "https://uncf.org/scholarships"),
        ("Point Foundation", "https://pointfoundation.org/scholarships/"),
        ("Hispanic Scholarship Fund", "https://www.hsf.net/scholarship"),
        ("P.E.O. International", "https://www.peointernational.org/about-peo-scholarships"),
    ],
}
HEADERS = {"User-Agent": "ScholarSearch/3.0 (+direct-application research)"}

def fetch(url: str) -> tuple[str, str]:
    try:
        with urlopen(Request(url, headers=HEADERS), timeout=10) as r:
            return r.geturl(), r.read(800_000).decode("utf-8", "replace")
    except Exception:
        return url, ""

def candidates(kind: str, source: str, url: str) -> list[dict]:
    final, html = fetch(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for a in soup.find_all("a", href=True):
        text = " ".join(a.get_text(" ", strip=True).split())
        href = urljoin(final, a["href"])
        blob = f"{text} {href}".lower()
        if not re.search(r"scholar|fellowship|award|grant", blob):
            continue
        if is_search_aggregator(href) or is_installer_url(href):
            continue
        host = urlparse(href).netloc.lower()
        if not host or host == urlparse(final).netloc.lower() and not re.search(r"apply|application|scholar|fellow|award", blob):
            continue
        title = text[:180] or href.rsplit("/", 2)[-1].replace("-", " ").title()
        out.append({"scholarship_name": title, "organization": source, "application_url": href, "source": kind, "source_url": url})
    return out

def verified(c: dict) -> bool:
    try:
        def real_fetch(url):
            final, html = fetch(url)
            return type("R", (), {"url": final, "status": 200 if html else 0, "content_type": "text/html", "title": "", "body": html, "links": []})()
        return verify_candidate(c, real_fetch)['score'] in {"A", "B"}
    except Exception:
        return False

def insert(records: list[dict], db: str) -> int:
    added = 0
    with guarded_connection(db) as conn:
        existing = {r[0] for r in conn.execute("SELECT application_url FROM scholarships WHERE active != 0")}
        for r in records:
            url = r["application_url"]
            if url in existing or is_search_aggregator(url) or is_installer_url(url):
                continue
            name = r["scholarship_name"]
            h = hashlib.md5(re.sub(r"\W", "", name.lower()).encode()).hexdigest()
            if conn.execute("SELECT 1 FROM scholarships WHERE name_hash=? OR lower(scholarship_name)=lower(?)", (h, name)).fetchone():
                continue
            vals = [r["source"], f"multi-{date.today()}-{h[:10]}", name, r["organization"], "", "Discovered from an official scholarship resource.", "", None, None, "Varies", "", url, "Academic", "Undergraduate", None, "US", None, "", "", "", "active", date.today().isoformat(), h, 1, date.today().isoformat(), date.today().isoformat()]
            cols = "source,source_id,scholarship_name,organization,organization_type,description,eligibility,amount_min,amount_max,amount_display,deadline,application_url,category,education_level,field_of_study,state_restriction,gpa_min,citizenship,ethnicity,gender,url_status,last_checked,name_hash,active,created_at,updated_at"
            conn.execute(f"INSERT INTO scholarships ({cols}) VALUES ({','.join('?' for _ in vals)})", vals)
            existing.add(url); added += 1
    return added

def main():
    p = argparse.ArgumentParser(); p.add_argument("--limit", type=int, default=100); p.add_argument("--commit", action="store_true"); p.add_argument("--output", type=Path, default=Path(__file__).with_name("multi_channel_report.json")); a = p.parse_args()
    jobs = [(k, n, u) for k, rows in SOURCES.items() for n, u in rows]
    raw = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        for f in as_completed([pool.submit(candidates, *j) for j in jobs]): raw.extend(f.result())
    unique = {}; rejected = 0
    for c in raw[:a.limit * 3]:
        key = (c["scholarship_name"].lower(), c["organization"].lower(), c["application_url"])
        if key in unique or not verified(c): rejected += 1
        else: unique[key] = c
    records = list(unique.values())[:a.limit]
    report = {"sources": {k: len(v) for k, v in SOURCES.items()}, "raw_candidates": len(raw), "verified_candidates": len(records), "rejected": rejected, "committed": False}
    if a.commit and records:
        for db in DBS: make_backup(db)
        report["added_each_db"] = [insert(records, db) for db in DBS]; report["committed"] = True
    a.output.write_text(json.dumps(report, indent=2)); print(json.dumps(report, indent=2))

if __name__ == "__main__": main()
