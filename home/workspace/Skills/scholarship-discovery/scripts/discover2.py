#!/usr/bin/env python3
"""
Enhanced Scholarship Discovery - finds 200+ new scholarships per run.
Uses improved HTML parsing + DuckDuckGo search fallback.
"""
import os
import sys
import json
import time
import re
import random
import sqlite3
import hashlib
import urllib.parse
import subprocess
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from db_safety import guarded_connection, make_backup

try:
    import requests
except ImportError:
    raise SystemExit("requests required: pip install requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

DATA_DIR = "/home/workspace/scholarsearch/data"
DB_PATH = f"{DATA_DIR}/processed/scholarships.db"
SITE_DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"
QUEUE_PATH = "/home/workspace/Skills/scholarship-discovery/scripts/batch_queue.json"
DBS = [DB_PATH, SITE_DB_PATH]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0)"}
REQUEST_TIMEOUT = 15
PARSE_BUDGET_SEC = 8
SEARCH_FALLBACK_PER_SOURCE = 5
BATCH_LIMIT_DEFAULT = 200
JITTER = (0.4, 1.4)

SCHOLARSHIP_KEYWORDS = re.compile(
    r"scholarship|bursary|fellowship|grant|award|financial aid|no.?essay|full.?ride|merit|need.?based",
    re.I,
)

RESIDENCY_TOKENS = {
    "Arizona": "AZ", "California": "CA", "Texas": "TX", "New York": "NY",
    "Florida": "FL", "Illinois": "IL", "Pennsylvania": "PA", "Ohio": "OH",
    "Georgia": "GA", "North Carolina": "NC", "Michigan": "MI", "Washington": "WA",
    "Virginia": "VA", "Colorado": "CO", "Oregon": "OR", "Massachusetts": "MA",
    "Maryland": "MD", "Tennessee": "TN", "Indiana": "IN", "Missouri": "MO",
    "Wisconsin": "WI", "Minnesota": "MN", "Arizona": "AZ", "Nevada": "NV",
    "Utah": "UT", "New Jersey": "NJ", "Connecticut": "CT", "South Carolina": "SC",
    "Alabama": "AL", "Kentucky": "KY", "Iowa": "IA", "Kansas": "KS",
}

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
    return cur.lastrowid

def verify_link(url: Optional[str], timeout: int = REQUEST_TIMEOUT) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout, headers=HEADERS)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}

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
    ready.sort(key=lambda x: (-x.get("pri", 0), -x["age_score"]))
    return ready[:limit]

def update_source(queue: List[Dict], source_id: str, **kwargs) -> None:
    for src in queue:
        if src.get("id") == source_id:
            src.update(kwargs)
            break
    save_queue(queue)

# ------------------------------------------------------------------ #
# Geo + category tagging
# ------------------------------------------------------------------ #
CATEGORY_RULES = [
    (re.compile(r"\bmasonic\b", re.I), "Masonic"),
    (re.compile(r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", re.I), "STEM"),
    (re.compile(r"\bmedicine\b|\bnursing\b|\bhealth\b", re.I), "Medicine"),
    (re.compile(r"\blaw\b|\blegal\b", re.I), "Law"),
    (re.compile(r"\bbusiness\b|\bfinance\b|\baccounting\b", re.I), "Business"),
    (re.compile(r"\bart\b|\bdesign\b|\bcreative\b", re.I), "Arts"),
    (re.compile(r"\beducation\b|\bteacher\b", re.I), "Education"),
]

LEVEL_RULES = [
    (re.compile(r"\bhigh school\b|\bsecondary\b", re.I), "High School"),
    (re.compile(r"\bgraduate\b|\bmaster\b|\bmba\b", re.I), "Graduate"),
    (re.compile(r"\bph\.?d\b|\bdoctorate\b", re.I), "PhD"),
    (re.compile(r"\btrade\b|\btechnical\b|\bvocational\b", re.I), "Trade School"),
    (re.compile(r"\bassociate\b|\bcommunity college\b", re.I), "Associate"),
    (re.compile(r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", re.I), "Professional"),
]

def tag_category(name: str, org: str, raw_text: str) -> str:
    text = f"{name} {org} {raw_text}"
    for pat, cat in CATEGORY_RULES:
        if pat.search(text):
            return cat
    return "Academic"

def tag_level(name: str, raw_text: str) -> str:
    text = f"{name} {raw_text}"
    for pat, lvl in LEVEL_RULES:
        if pat.search(text):
            return lvl
    return "Undergraduate"

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

# ------------------------------------------------------------------ #
# Extraction: improved HTML parse + DuckDuckGo search fallback
# ------------------------------------------------------------------ #
def parse_candidates_from_html(url: str, html_text: str, src_group: str) -> List[Dict]:
    """Improved parser that looks in many more tags and uses better heuristics."""
    if not html_text or len(html_text) < 100:
        return []
    
    candidates = []
    seen = set()
    
    # Strategy 1: Parse with BeautifulSoup
    if BeautifulSoup:
        soup = BeautifulSoup(html_text, "html.parser")
        
        # Look in many tag types, not just headings and lists
        for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "a", "li", "div", "span", "p", "td", "th", "strong", "b", "em"]):
            text = tag.get_text(" ", strip=True)
            if not text or len(text) < 15 or len(text) > 300:
                continue
            if not SCHOLARSHIP_KEYWORDS.search(text):
                continue
            
            # Skip generic text that doesn't look like scholarship names
            if re.search(r"cookie|privacy|terms|navigation|menu|footer|header|sidebar", text, re.I):
                continue
            
            key = normalize(text)
            if key in seen:
                continue
            seen.add(key)
            
            # Extract link
            link = None
            if tag.name == "a":
                link = tag.get("href")
            else:
                # Look for nearest parent or child link
                parent_a = tag.find_parent("a")
                if parent_a:
                    link = parent_a.get("href")
                else:
                    child_a = tag.find("a")
                    if child_a:
                        link = child_a.get("href")
            
            if link and not link.startswith("http"):
                link = urllib.parse.urljoin(url, link)
            
            # Extract amount from text
            amount_min = None
            amount_max = None
            amount_match = re.search(r"\$([0-9,]+)(?:\s*-\s*\$([0-9,]+))?", text)
            if amount_match:
                amount_min = int(amount_match.group(1).replace(",", ""))
                amount_max = int(amount_match.group(2).replace(",", "")) if amount_match.group(2) else None
                # Cap absurdly high amounts at $500,000
                if amount_min and amount_min > 500000:
                    amount_min = None
                if amount_max and amount_max > 500000:
                    amount_max = None
            
            # Extract deadline
            deadline = ""
            deadline_match = re.search(r"(?:deadline|due|closes?|apply by)[\s:]+(\w+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\w+ \d{4})", text, re.I)
            if deadline_match:
                deadline = deadline_match.group(1)
            
            candidates.append({
                "scholarship_name": text[:180],
                "organization": src_group.replace("_", " ").title(),
                "application_url": link,
                "amount_display": parse_amount_display(amount_min, amount_max),
                "amount_min": amount_min,
                "amount_max": amount_max,
                "deadline": deadline,
                "source_url": url,
            })
    
    # Strategy 2: Regex-based extraction for structured text
    # Find patterns like "Scholarship Name - $Amount - Deadline"
    scholarship_blocks = re.findall(
        r"([A-Z][^.\n]{15,150}(?:scholarship|award|grant|fellowship|bursary)[^.\n]{0,100})",
        html_text,
        re.I
    )
    for block in scholarship_blocks:
        text = block.strip()
        if len(text) < 15 or len(text) > 300:
            continue
        key = normalize(text)
        if key in seen:
            continue
        seen.add(key)
        
        amount_min = None
        amount_max = None
        amount_match = re.search(r"\$([0-9,]+)(?:\s*-\s*\$([0-9,]+))?", text)
        if amount_match:
            amount_min = int(amount_match.group(1).replace(",", ""))
            amount_max = int(amount_match.group(2).replace(",", "")) if amount_match.group(2) else None
            # Cap absurdly high amounts at $500,000
            if amount_min and amount_min > 500000:
                amount_min = None
            if amount_max and amount_max > 500000:
                amount_max = None
        
        deadline = ""
        deadline_match = re.search(r"(?:deadline|due|closes?|apply by)[\s:]+(\w+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\w+ \d{4})", text, re.I)
        if deadline_match:
            deadline = deadline_match.group(1)
        
        # Try to find a link near this text
        link_match = re.search(r'href="([^"]+)"', html_text[html_text.find(text)-200:html_text.find(text)+200])
        link = link_match.group(1) if link_match else None
        if link and not link.startswith("http"):
            link = urllib.parse.urljoin(url, link)
        
        candidates.append({
            "scholarship_name": text[:180],
            "organization": src_group.replace("_", " ").title(),
            "application_url": link,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "amount_min": amount_min,
            "amount_max": amount_max,
            "deadline": deadline,
            "source_url": url,
        })
    
    return candidates[:80]

def search_fallback_candidates(source: Dict) -> List[Dict]:
    """Use DuckDuckGo HTML search to find scholarship pages from this source."""
    domain = source.get("url", "").replace("https://", "").replace("http://", "").split("/")[0]
    query = f"{domain} scholarships 2026"
    
    candidates = []
    try:
        # Use DuckDuckGo HTML search
        search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        resp = requests.get(search_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser") if BeautifulSoup else None
            if soup:
                # DuckDuckGo results are in <a class="result__a"> tags
                for result in soup.find_all("a", class_="result__a", limit=SEARCH_FALLBACK_PER_SOURCE):
                    title = result.get_text(strip=True)
                    href = result.get("href", "")
                    if not title or not href:
                        continue
                    if not SCHOLARSHIP_KEYWORDS.search(title):
                        continue
                    
                    # Extract actual URL from DuckDuckGo redirect
                    if href.startswith("//duckduckgo.com/l/?uddg="):
                        actual_url = href.split("uddg=")[1].split("&")[0]
                        actual_url = urllib.parse.unquote(actual_url)
                    else:
                        actual_url = href
                    
                    candidates.append({
                        "scholarship_name": title[:180],
                        "organization": source.get("group", "global_discovery").replace("_", " ").title(),
                        "application_url": actual_url,
                        "amount_display": "Varies",
                        "deadline": "",
                        "source_url": source.get("url", ""),
                    })
    except Exception as e:
        print(f"  Search fallback error: {e}")
    
    return candidates

# ------------------------------------------------------------------ #
# Main discovery loop
# ------------------------------------------------------------------ #
def stats():
    totals = {}
    for db in DBS:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM scholarships")
            totals[db] = cur.fetchone()[0]
            conn.close()
        else:
            totals[db] = 0
    return totals

def batch_insert(scholarships: List[Dict]) -> Dict:
    added = 0
    errors = 0
    for db in DBS:
        make_backup(db)
    for s in scholarships:
        for db in DBS:
            try:
                with guarded_connection(db) as conn:
                    if is_dup(conn, s):
                        continue
                    # Verify link if URL exists
                    if s.get("application_url"):
                        v = verify_link(s["application_url"])
                        if not v.get("ok"):
                            if "http_404" in v.get("reason", "") or "http_503" in v.get("reason", ""):
                                s["link_notes"] = f"Link failed: {v['reason']}"
                                s["application_url"] = v.get("final_url", s["application_url"])
                            else:
                                s["link_notes"] = f"Link check: {v.get('reason', 'unknown')}"
                    
                    # Tag metadata
                    raw_text = f"{s.get('scholarship_name','')} {s.get('description','')} {s.get('source_url','')}"
                    s["category"] = tag_category(s.get("scholarship_name", ""), s.get("organization", ""), raw_text)
                    s["education_level"] = tag_level(s.get("scholarship_name", ""), raw_text)
                    
                    add_scholarship(conn, s)
                    added += 1
            except Exception as e:
                errors += 1
                print(f"  DB error: {e}")
    return {"added": added, "errors": errors}

def process_source(source: Dict, limit: int, collected: List[Dict]) -> Tuple[int, List[Dict]]:
    """Process a single source and return (count, source_report)."""
    url = source.get("url", "")
    group = source.get("group", "global")
    source_id = source.get("id", "unknown")
    
    print(f"Processing {source_id}: {url}")
    
    # Fetch page
    html_text = ""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        html_text = resp.text
    except Exception as e:
        print(f"  Fetch error: {e}")
        return 0, {"id": source_id, "group": group, "count": 0, "status": "fetch_error", "error": str(e)[:100]}
    
    # Parse candidates
    candidates = parse_candidates_from_html(url, html_text, group)
    
    # If few candidates found, try search fallback
    if len(candidates) < 3 and BeautifulSoup:
        print(f"  Low yield ({len(candidates)}), trying search fallback...")
        fallback = search_fallback_candidates(source)
        candidates.extend(fallback)
    
    # Dedup within this batch
    seen_keys = set()
    unique = []
    for c in candidates:
        key = normalize(c.get("scholarship_name", "")) + "|" + normalize(c.get("organization", ""))
        if key not in seen_keys:
            seen_keys.add(key)
            unique.append(c)
    
    candidates = unique[:limit]
    
    # Add to collected list
    collected.extend(candidates)
    
    return len(candidates), {
        "id": source_id,
        "group": group,
        "count": len(candidates),
        "status": "ok" if len(candidates) > 0 else "empty"
    }

def main():
    limit = BATCH_LIMIT_DEFAULT
    queue = load_queue()
    
    if not queue:
        print("No batch_queue.json found")
        return
    
    before = stats()
    print(f"Before: {before}")
    
    # Pick sources
    sources = pick_sources(queue, max(30, min(80, limit // 3)))
    print(f"Picked {len(sources)} sources")
    
    all_candidates = []
    source_reports = []
    
    # Process sources in parallel with thread pool
    remaining = limit
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for source in sources:
            if remaining <= 0:
                break
            per_source = min(20, max(5, remaining // len(sources)))
            future = executor.submit(process_source, source, per_source, all_candidates)
            futures[future] = source
        
        for future in as_completed(futures):
            source = futures[future]
            try:
                count, report = future.result()
                source_reports.append(report)
                remaining -= count
            except Exception as e:
                source_reports.append({
                    "id": source.get("id", "unknown"),
                    "group": source.get("group", "unknown"),
                    "count": 0,
                    "status": "error",
                    "error": str(e)[:100]
                })
    
    # Sort reports by id for consistent output
    source_reports.sort(key=lambda x: x.get("id", ""))
    
    # Batch insert
    print(f"\nInserting {len(all_candidates)} candidates...")
    result = batch_insert(all_candidates)
    
    after = stats()
    
    print("Result:", result)
    print("After:", after)
    print("Source report:", json.dumps(source_reports[:10], indent=2))
    print(f"Total scholarships: {before} -> {after}")
    
    # Update queue with last_scraped
    for report in source_reports:
        if report.get("status") != "error":
            update_source(queue, report["id"], 
                         last_scraped=datetime.now(timezone.utc).isoformat(),
                         last_batch_count=report.get("count", 0))
    
    return result, after, source_reports

if __name__ == "__main__":
    main()
