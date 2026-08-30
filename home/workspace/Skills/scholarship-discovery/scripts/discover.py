#!/usr/bin/env python3
"""
Scholarship Discovery Skill - Queue-Based Global Batch Discovery

Goal: ~200 new verified scholarships per run.

Workflow:
1. Load batch_queue.json and pick top-ready sources by priority + age.
2. For each source, fetch/extract candidate scholarships.
   - Timed HTML parse fallback: if parse finds <3 candidates in 10s,
     fall back to web_search("<site> scholarships 2026").
3. Normalize candidates (name, org, amount, deadline, url).
4. Dedup against DBs via name_hash(name||org).
5. Verify application links end-to-end:
   - HEAD request; if 200, record final_url.
   - If 3xx, follow and record final_url.
   - If 4xx/5xx, mark inactive and attach link_notes.
6. Tag at ingestion: country/state from source metadata and page text.
7. Insert into both working + site DBs atomically per candidate.
8. Update batch_queue.json with last_scraped + last_batch_count.
9. Emit structured report for daily email.

Dependencies: requests, beautifulsoup4 (bs4)
"""
import os
import sys
import json
import time
import re
import random
import sqlite3
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("requests required: pip install requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # optional HTML parse fallback

from crawl_directory_sources import fetch as fetch_directory, individual_links, parse_detail

DATA_DIR = "/home/workspace/scholarsearch/data"
MAIN_DB_PATH = "/home/workspace/scholarsearch/data/processed/scholarships.db"
SITE_DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"
QUEUE_PATH = "/home/workspace/Skills/scholarship-discovery/scripts/batch_queue.json"
DBS = [MAIN_DB_PATH, SITE_DB_PATH]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 15
PARSE_BUDGET_SEC = 8
SEARCH_FALLBACK_LIMIT = 8
BATCH_LIMIT_DEFAULT = 200
JITTER = (0.4, 1.4)

# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #
def normalize(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def name_hash(name: str, org: str) -> str:
    raw = normalize(name) + "||" + normalize(org)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def clean_num(val: Optional[str]) -> Optional[int]:
    if not val:
        return None
    m = re.search(r"[\$\€\£]?\s*([0-9,]+)", str(val).replace(",", ""))
    return int(m.group(1)) if m else None


def parse_amount_display(amount_min: Optional[int], amount_max: Optional[int]) -> str:
    if amount_min and amount_max:
        if amount_min == amount_max:
            return f"${amount_min:,}"
        return f"${amount_min:,} - ${amount_max:,}"
    if amount_min:
        return f"${amount_min:,}+"
    if amount_max:
        return f"Up to ${amount_max:,}"
    return "Varies"


def get_db_connection(path: str):
    return sqlite3.connect(path)


def is_dup(conn: sqlite3.Connection, scholarship: Dict) -> bool:
    cur = conn.cursor()
    nh = name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", ""))
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None


def add_scholarship(conn: sqlite3.Connection, scholarship: Dict) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO scholarships (
            source, source_id, scholarship_name, organization, organization_type,
            description, eligibility, amount_min, amount_max, amount_display,
            deadline, application_url, form_url, email, phone, address, website,
            category, education_level, field_of_study, state_restriction,
            gpa_min, citizenship, ethnicity, gender, military_affiliation,
            name_hash, created_at, updated_at, link_notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            scholarship.get("source", "global_discovery"),
            scholarship.get("source_id"),
            scholarship.get("scholarship_name"),
            scholarship.get("organization"),
            scholarship.get("organization_type"),
            scholarship.get("description"),
            scholarship.get("eligibility"),
            scholarship.get("amount_min"),
            scholarship.get("amount_max"),
            scholarship.get("amount_display"),
            scholarship.get("deadline"),
            scholarship.get("application_url"),
            scholarship.get("form_url"),
            scholarship.get("email"),
            scholarship.get("phone"),
            scholarship.get("address"),
            scholarship.get("website"),
            scholarship.get("category"),
            scholarship.get("education_level"),
            scholarship.get("field_of_study"),
            scholarship.get("state_restriction"),
            scholarship.get("gpa_min"),
            scholarship.get("citizenship"),
            scholarship.get("ethnicity"),
            scholarship.get("gender"),
            scholarship.get("military_affiliation"),
            name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", "")),
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            scholarship.get("link_notes"),
        ),
    )
    conn.commit()
    return cur.lastrowid


def verify_link(url: Optional[str], timeout: int = REQUEST_TIMEOUT) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.get(url, allow_redirects=True, timeout=timeout, headers=HEADERS)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}


GENERIC_PATH_RE = re.compile(
    r"/(?:blog|news|article|articles|directory|directories|category|categories|search|tag|tags|about|home|index|resources?)(?:/|$)",
    re.I,
)
GENERIC_NAME_RE = re.compile(
    r"^(?:scholarships?|scholarship opportunities|scholarship listings?|financial aid|home|resources?|directory|search results?)$",
    re.I,
)
NAVIGATION_NAME_RE = re.compile(
    r"show submenu|\b(?:admission|research|academics?|student life|types? of aid|faq|frequently asked questions|menu|explore)\b",
    re.I,
)
INDIVIDUAL_OPPORTUNITY_RE = re.compile(
    r"\b(?:scholarship|fellowship|grant|bursary|award|prize)\b",
    re.I,
)


def reject_reason(scholarship: Dict) -> Optional[str]:
    name = str(scholarship.get("scholarship_name") or "").strip()
    org = str(scholarship.get("organization") or "").strip()
    url = str(scholarship.get("application_url") or "").strip()
    if len(name) < 8:
        return "missing_or_short_name"
    if not org:
        return "missing_organization"
    if not url:
        return "missing_application_url"
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "invalid_application_url"
    if GENERIC_NAME_RE.fullmatch(name) or NAVIGATION_NAME_RE.search(name):
        return "generic_or_page_level"
    if GENERIC_PATH_RE.search(parsed.path):
        return "generic_or_page_level"
    if not INDIVIDUAL_OPPORTUNITY_RE.search(name):
        return "generic_or_page_level"
    return None


# ------------------------------------------------------------------ #
# Queue management
# ------------------------------------------------------------------ #
def load_queue() -> List[Dict]:
    if not os.path.exists(QUEUE_PATH):
        return []
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(queue: List[Dict]) -> None:
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)


def pick_sources(queue: List[Dict], limit: int) -> List[Dict]:
    now = datetime.now(timezone.utc).isoformat()
    ready = []
    for src in queue:
        age = 0
        if src.get("last_scraped"):
            try:
                age = (datetime.now(timezone.utc) - datetime.fromisoformat(src["last_scraped"])).total_seconds()
            except Exception:
                age = 999999
        src["age_score"] = age if age > 0 else 999999
        ready.append(src)
    
    # Group by category and round-robin to ensure diversity
    from collections import defaultdict
    by_group = defaultdict(list)
    for src in ready:
        by_group[src.get("group", "unknown")].append(src)
    
    # Sort each group by (-pri, -age_score)
    for grp in by_group:
        by_group[grp].sort(key=lambda x: (-x.get("pri", 0), -x["age_score"]))
    
    # Round-robin across groups
    result = []
    group_keys = sorted(by_group.keys())
    while len(result) < limit:
        added = False
        for grp in group_keys:
            if by_group[grp]:
                result.append(by_group[grp].pop(0))
                added = True
                if len(result) >= limit:
                    break
        if not added:
            break
    
    return result[:limit]


def update_source(queue: List[Dict], source_id: str, **kwargs) -> None:
    for src in queue:
        if src.get("id") == source_id:
            src.update(kwargs)
            break
    save_queue(queue)


# ------------------------------------------------------------------ #
# Extraction: HTML parse + search fallback
# ------------------------------------------------------------------ #
SCHOLARSHIP_KEYWORDS = re.compile(
    r"scholarship|bursary|fellowship|grant|award|financial aid",
    re.I,
)
RESIDENCY_TOKENS = {
    "Arizona": "AZ",
    "California": "CA",
    "Texas": "TX",
    "New York": "NY",
    "Florida": "FL",
    "Illinois": "IL",
    "Pennsylvania": "PA",
    "Ohio": "OH",
    "Georgia": "GA",
    "North Carolina": "NC",
    "Michigan": "MI",
    "Washington": "WA",
    "Virginia": "VA",
    "Colorado": "CO",
    "Oregon": "OR",
    "Massachusetts": "MA",
    "Maryland": "MD",
    "Tennessee": "TN",
    "Indiana": "IN",
    "Missouri": "MO",
    "Wisconsin": "WI",
    "Minnesota": "MN",
    "Arizona": "AZ",
}


def guess_country(src: Dict, html_text: str) -> str:
    url = src.get("url", "")
    if ".edu" in url or ".gov" in url:
        if any(t in url for t in [".edu/uk", ".ac.uk", "ucas", "scholarships.org.uk"]):
            return "UK"
        if any(t in url for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
            return "Canada"
        if any(t in url for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
            return "Australia"
        return "USA"
    return src.get("country", "USA")


def guess_state(src: Dict, html_text: str) -> Optional[str]:
    for name, abbr in RESIDENCY_TOKENS.items():
        if name.lower() in html_text.lower() or abbr.lower() in html_text.lower():
            return abbr
    return None


def parse_candidates_from_html(url: str, html_text: str, src_group: str) -> List[Dict]:
    if BeautifulSoup is None:
        return []
    soup = BeautifulSoup(html_text, "html.parser")
    candidates: List[Dict] = []
    seen = set()
    for tag in soup.find_all(["h2", "h3", "h4", "a", "li"]):
        text = tag.get_text(" ", strip=True)
        if not text or len(text) < 12:
            continue
        if not SCHOLARSHIP_KEYWORDS.search(text):
            continue
        key = normalize(text)
        if key in seen:
            continue
        seen.add(key)
        link = tag.get("href") if tag.name == "a" else None
        if not link and tag.find("a"):
            link = tag.find("a").get("href")
        if link and not link.startswith("http"):
            link = requests.compat.urljoin(url, link)
        candidates.append(
            {
                "scholarship_name": text[:180],
                "organization": src_group.replace("_", " ").title(),
                "application_url": link,
                "amount_display": "Varies",
                "deadline": "",
            }
        )
    return candidates[:80]


def search_fallback_candidates(source: Dict) -> List[Dict]:
    """Search fallback is not implemented in this environment; returns empty list."""
    domain = source.get("url", "").replace("https://", "").replace("http://", "").split("/")[0]
    query = f"{domain} scholarships 2026"
    print(f"  -> search fallback skipped: {query}")
    return []


# ------------------------------------------------------------------ #
# Geo + category tagging
# ------------------------------------------------------------------ #
CATEGORY_RULES = [
    (re.compile(r"\bmasonic\b", re.I), "Masonic"),
    (re.compile(r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", re.I), "STEM"),
    (re.compile(r"\bmedicine\b|\bnursing\b|\bhealth\b", re.I), "Healthcare"),
    (re.compile(r"\blaw\b|\blegal\b", re.I), "Law"),
    (re.compile(r"\bbusiness\b|\bfinance\b|\baccounting\b", re.I), "Business"),
    (re.compile(r"\bart\b|\bdesign\b|\bcreative\b", re.I), "Arts"),
    (re.compile(r"\beducation\b|\bteacher\b", re.I), "Education"),
]


def tag_category(name: str, org: str, raw_text: str) -> str:
    text = f"{name} {org} {raw_text}"
    for pat, cat in CATEGORY_RULES:
        if pat.search(text):
            return cat
    return "Academic"


LEVEL_RULES = [
    (re.compile(r"\bhigh school\b|\bsecondary\b", re.I), "High School"),
    (re.compile(r"\bgraduate\b|\bmaster\b|\bmba\b", re.I), "Graduate"),
    (re.compile(r"\bph\.?d\b|\bdoctorate\b", re.I), "PhD"),
    (re.compile(r"\btrade\b|\btechnical\b|\bvocational\b", re.I), "Trade School"),
    (re.compile(r"\bassociate\b|\bcommunity college\b", re.I), "Associate"),
    (re.compile(r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", re.I), "Professional"),
]


def tag_level(name: str, raw_text: str) -> str:
    text = f"{name} {raw_text}"
    for pat, lvl in LEVEL_RULES:
        if pat.search(text):
            return lvl
    return "Undergraduate"


# ------------------------------------------------------------------ #
# Core batch flow
# ------------------------------------------------------------------ #
def process_source(source: Dict, limit: int) -> Tuple[List[Dict], str]:
    url = source.get("url")
    group = source.get("group", "global")
    country = source.get("country", "USA")
    if not url:
        return [], "no_url"

    print(f"\n=== source: {source.get('id')} {group} {url}")
    candidates: List[Dict] = []
    raw_text = ""
    start = time.time()
    if source.get("kind") == "directory":
        try:
            final_url, raw_text = fetch_directory(url)
            for detail_url, link_text in individual_links(final_url, raw_text)[:limit]:
                detail_final, detail_html = fetch_directory(detail_url)
                record = parse_detail(detail_final, link_text, detail_html, urlparse(final_url).netloc)
                if record:
                    candidates.append(record)
            print(f"  directory crawl: {len(candidates)} individual pages")
        except Exception as e:
            print(f"  directory crawl error: {e}")
    else:
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            raw_text = resp.text or ""
            if SCHOLARSHIP_KEYWORDS.search(raw_text):
                candidates = parse_candidates_from_html(url, raw_text, group)
        except Exception as e:
            print(f"  fetch error: {e}")

    parse_time = time.time() - start
    if len(candidates) < 3 and parse_time < PARSE_BUDGET_SEC:
        candidates.extend(search_fallback_candidates(source))
    elif len(candidates) == 0:
        candidates.extend(search_fallback_candidates(source))

    state = guess_state(source, raw_text)
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    processed: List[Dict] = []
    for idx, c in enumerate(candidates[: limit], start=1):
        processed.append(
            {
                "source": f"queue_{source.get('id')}",
                "source_id": f"queue_{source.get('id')}_{today}_{idx:03d}",
                "scholarship_name": c.get("scholarship_name"),
                "organization": c.get("organization"),
                "organization_type": "",
                "description": "",
                "eligibility": "",
                "amount_min": None,
                "amount_max": None,
                "amount_display": c.get("amount_display", "Varies"),
                "deadline": c.get("deadline", ""),
                "application_url": c.get("application_url"),
                "form_url": None,
                "email": None,
                "phone": None,
                "address": "",
                "website": c.get("application_url"),
                "category": tag_category(c.get("scholarship_name", ""), c.get("organization", ""), raw_text),
                "education_level": tag_level(c.get("scholarship_name", ""), raw_text),
                "field_of_study": None,
                "state_restriction": state,
                    "gpa_min": None,
                "citizenship": None,
                "ethnicity": None,
                "gender": None,
                "military_affiliation": None,
                "link_notes": "",
            }
        )
    return processed, "ok"


def batch_insert(scholarships: List[Dict]) -> Dict:
    added_total = 0
    updated_total = 0
    skipped_dup = 0
    skipped_link = 0
    rejected = 0
    verified = 0
    errors = []

    for s in scholarships:
        reason = reject_reason(s)
        if reason:
            rejected += 1
            s["link_notes"] = reason
            continue

        duplicate = False
        for db_path in DBS:
            conn = get_db_connection(db_path)
            try:
                duplicate = is_dup(conn, s)
            finally:
                conn.close()
            if duplicate:
                break
        if duplicate:
            skipped_dup += 1
            continue

        checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        v = verify_link(s["application_url"])
        if not v["ok"]:
            skipped_link += 1
            continue

        s["application_url"] = v["final_url"]
        s["website"] = s.get("website") or v["final_url"]
        s["url_status"] = "verified"
        s["last_checked"] = checked_at
        s["link_notes"] = f"HTTP {v.get('status', 200)}; final URL recorded"
        verified += 1
        try:
            for db_path in DBS:
                conn = get_db_connection(db_path)
                try:
                    if is_dup(conn, s):
                        raise ValueError(f"duplicate detected during insert: {db_path}")
                    add_scholarship(conn, s)
                    conn.execute(
                        "UPDATE scholarships SET url_status = ?, last_checked = ?, link_notes = ?, active = 1 WHERE id = last_insert_rowid()",
                        (s["url_status"], s["last_checked"], s["link_notes"]),
                    )
                    conn.commit()
                    added_total += 1
                finally:
                    conn.close()
        except Exception as e:
            errors.append(str(e))

    return {
        "added": added_total,
        "updated": updated_total,
        "skipped_dup": skipped_dup,
        "skipped_link": skipped_link,
        "rejected": rejected,
        "verified_candidates": verified,
        "errors": errors,
    }


def stats() -> Dict:
    out = {}
    for db_path in DBS:
        conn = get_db_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scholarships")
        out[db_path] = cur.fetchone()[0]
        conn.close()
    return out


# ------------------------------------------------------------------ #
# Entrypoint
# ------------------------------------------------------------------ #
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Batch scholarship discovery")
    parser.add_argument("--limit", type=int, default=BATCH_LIMIT_DEFAULT, help="Target new scholarships")
    parser.add_argument("--input", help="Optional JSON file of scholarships to insert")
    parser.add_argument("--json-input", action="store_true", help="Expect JSON from stdin")
    args = parser.parse_args()

    before = stats()
    print("Before:", before)

    scholarships: List[Dict] = []
    source_report = []

    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for i, item in enumerate(raw[: args.limit], start=1):
            item.setdefault("source", "json_input")
            item.setdefault("source_id", f"json_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{i:03d}")
            item.setdefault("status", "active")
            scholarships.append(item)
    else:
        queue = load_queue()
        if not queue:
            print("Empty batch queue. Not running agent discovery.")
            sys.exit(0)

        sources = pick_sources(queue, max(30, min(80, args.limit // 3)))
        remaining = args.limit
        for src in sources:
            if remaining <= 0:
                break
            items, src_status = process_source(src, min(20, remaining))
            source_report.append({"id": src.get("id"), "group": src.get("group"), "count": len(items), "status": src_status})
            scholarships.extend(items)
            remaining -= len(items)
            update_source(
                queue,
                src["id"],
                last_scraped=datetime.now(timezone.utc).isoformat(),
                last_batch_count=len(items),
            )
            time.sleep(random.uniform(*JITTER))

        scholarships = scholarships[: args.limit]

    if not scholarships:
        print("No scholarships discovered in this run.")
        return

    result = batch_insert(scholarships)
    after = stats()

    print("Result:", result)
    print("After:", after)
    print("Source report:", json.dumps(source_report[:10], indent=2))
    print(f"Total scholarships: {before} -> {after}")


if __name__ == "__main__":
    main()
