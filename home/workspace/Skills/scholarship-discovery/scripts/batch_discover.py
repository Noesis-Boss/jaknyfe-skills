#!/usr/bin/env python3
"""
Batch scholarship discovery: search, fetch, extract, verify, insert.
Reads saved web_search JSON results, fetches pages, extracts structured
scholarship data, verifies application URLs, dedups, and inserts into DB.
"""
import os, sys, json, re, sqlite3, hashlib, time, random
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 20
SEARCH_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
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
    m = re.search(r"[\$\,\€\£]?\s*([0-9,]+)", str(val).replace(",", ""))
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

def guess_country(url: str, text: str = "") -> str:
    combined = (url + " " + text).lower()
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "uk gov"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
        return "Australia"
    if any(t in combined for t in ["studyinzealand", "studylink", ".govt.nz"]):
        return "NZ"
    if any(t in combined for t in ["erasmus", "daad", "campusfrance", "studynetherlands"]):
        return "EU"
    return "USA"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

# ------------------------------------------------------------------
# Link verification (GET, not HEAD)
# ------------------------------------------------------------------
def verify_link(url: Optional[str]) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        # Check if page looks like an application form or scholarship page
        text = resp.text.lower()
        has_form = any(k in text for k in ["application", "apply now", "submit", "form", "portal"])
        has_scholarship = "scholarship" in text or "bursary" in text or "fellowship" in text or "award" in text
        if not has_scholarship:
            return {"ok": False, "reason": "not_scholarship_page", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url, "has_form": has_form}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}

# ------------------------------------------------------------------
# DB operations
# ------------------------------------------------------------------
def is_dup(conn: sqlite3.Connection, scholarship: Dict) -> bool:
    cur = conn.cursor()
    nh = name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", ""))
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

def add_scholarship(conn: sqlite3.Connection, scholarship: Dict) -> int:
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO scholarships (
            source, source_id, scholarship_name, organization, organization_type,
            description, eligibility, amount_min, amount_max, amount_display,
            deadline, application_url, form_url, email, phone, address, website,
            category, education_level, field_of_study, state_restriction,
            gpa_min, citizenship, ethnicity, gender, military_affiliation,
            name_hash, created_at, updated_at, link_notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            scholarship.get("source", "batch_discover"),
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

def stats():
    out = {}
    for path in DB_PATHS:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scholarships")
        out[path] = cur.fetchone()[0]
        conn.close()
    return out

# ------------------------------------------------------------------
# Page parsers
# ------------------------------------------------------------------
def extract_from_page(url: str, html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    scholarships = []
    domain = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]

    # Generic extraction: look for scholarship-like blocks
    # Strategy 1: cards with headings/links
    for heading in soup.find_all(["h2", "h3", "h4", "h5", "strong", "b"]):
        title = heading.get_text(" ", strip=True)
        if not title or len(title) < 10:
            continue
        if not re.search(r"scholarship|bursary|fellowship|grant|award|program", title, re.I):
            continue

        # Find nearest link
        link = heading.find("a") or heading.find_parent().find("a") if heading.find_parent() else None
        href = link.get("href", "") if link else ""
        if href and not href.startswith("http"):
            href = requests.compat.urljoin(url, href)

        # Get surrounding text for amount/deadline
        parent = heading.parent
        text = parent.get_text(" ", strip=True) if parent else title
        if len(text) > 800:
            text = text[:800]

        scholarships.append({
            "scholarship_name": title[:180],
            "organization": domain,
            "organization_type": "Unknown",
            "description": text[:500],
            "eligibility": "",
            "amount_min": None,
            "amount_max": None,
            "amount_display": "Varies",
            "deadline": "",
            "application_url": href or url,
            "form_url": href or url,
            "email": "",
            "phone": "",
            "address": "",
            "website": href or url,
            "category": "Academic",
            "education_level": "Undergraduate",
            "field_of_study": "",
            "state_restriction": "",
            "gpa_min": None,
            "citizenship": "None",
            "ethnicity": "",
            "gender": "",
            "military_affiliation": "",
            "source": f"page_{domain}",
            "source_id": hashlib.md5((title + href).encode()).hexdigest()[:12],
            "link_notes": "",
        })

    # Strategy 2: lists with scholarship items
    if not scholarships:
        for li in soup.find_all("li"):
            text = li.get_text(" ", strip=True)
            if not re.search(r"scholarship|bursary|fellowship|grant|award|program", text, re.I):
                continue
            if len(text) < 15:
                continue
            link = li.find("a")
            href = link.get("href", "") if link else ""
            if href and not href.startswith("http"):
                href = requests.compat.urljoin(url, href)
            scholarships.append({
                "scholarship_name": text[:180],
                "organization": domain,
                "organization_type": "Unknown",
                "description": text[:500],
                "eligibility": "",
                "amount_min": None,
                "amount_max": None,
                "amount_display": "Varies",
                "deadline": "",
                "application_url": href or url,
                "form_url": href or url,
                "email": "",
                "phone": "",
                "address": "",
                "website": href or url,
                "category": "Academic",
                "education_level": "Undergraduate",
                "field_of_study": "",
                "state_restriction": "",
                "gpa_min": None,
                "citizenship": "None",
                "ethnicity": "",
                "gender": "",
                "military_affiliation": "",
                "source": f"page_{domain}",
                "source_id": hashlib.md5((text + href).encode()).hexdigest()[:12],
                "link_notes": "",
            })

    # Dedup within page
    seen = set()
    unique = []
    for s in scholarships:
        key = normalize(s["scholarship_name"]) + "||" + normalize(s["organization"])
        if key not in seen:
            seen.add(key)
            unique.append(s)
    return unique

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    limit = 200
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)

    # Load all search result files to get URLs
    search_files = []
    for f in os.listdir(SEARCH_DIR):
        if f.startswith("web_search") and f.endswith(".json"):
            search_files.append(os.path.join(SEARCH_DIR, f))

    print(f"Found {len(search_files)} search result files")

    urls_to_fetch = set()
    for sf in search_files:
        try:
            with open(sf, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            items = data if isinstance(data, list) else data.get("results", data.get("data", []))
            for item in items:
                url = item.get("url", "")
                if url and url.startswith("http"):
                    urls_to_fetch.add(url)
        except Exception as e:
            print(f"Error reading {sf}: {e}")

    urls_to_fetch = list(urls_to_fetch)
    print(f"Unique URLs to fetch: {len(urls_to_fetch)}")

    before = stats()
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    errors = 0
    verified = []

    for url in urls_to_fetch[:limit * 3]:
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            if resp.status_code >= 400:
                continue
            candidates = extract_from_page(url, resp.text)
        except Exception as e:
            errors += 1
            continue

        for c in candidates:
            # Check duplicates
            dup = False
            for path in DB_PATHS:
                conn = sqlite3.connect(path)
                if is_dup(conn, c):
                    dup = True
                    conn.close()
                    break
                conn.close()
            if dup:
                skipped_dup += 1
                continue

            # Verify link
            vr = verify_link(c.get("application_url"))
            if not vr.get("ok"):
                skipped_verify += 1
                continue

            if vr.get("final_url"):
                c["application_url"] = vr["final_url"]
                c["form_url"] = vr["final_url"]

            for path in DB_PATHS:
                conn = sqlite3.connect(path)
                add_scholarship(conn, c)
                conn.close()
            added += 1
            verified.append(c)
            if added >= limit:
                break
        if added >= limit:
            break
        time.sleep(random.uniform(0.2, 0.8))

    after = stats()

    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: {errors}")
    print(f"  DB totals before: {before}")
    print(f"  DB totals after: {after}")

    from collections import Counter
    cats = Counter(c.get("category", "Unknown") for c in verified)
    print(f"\nBreakdown by category:")
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")

    top = sorted(verified, key=lambda x: x.get("amount_min") or 0, reverse=True)[:10]
    print(f"\nTop 10 by amount:")
    for c in top:
        print(f"  {c['amount_display']} - {c['scholarship_name'][:60]}")

    # Report failed verifications
    print(f"\nFailed verification count: {skipped_verify}")

if __name__ == "__main__":
    main()
