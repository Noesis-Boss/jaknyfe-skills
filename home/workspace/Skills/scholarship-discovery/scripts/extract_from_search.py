#!/usr/bin/env python3
"""
Extract scholarships from saved web_search JSON results.
Reads all web_search*.json files from conversation workspace,
extracts scholarship data from snippets, dedups, verifies, and inserts.
"""
import os, sys, json, re, sqlite3, hashlib, time, random
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests

CONV_WORKSPACE = "/home/.z/workspaces/con_c8vlyHChdMPruaB5"
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 15

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

def guess_country(url: str) -> str:
    if ".edu" in url or ".gov" in url:
        if any(t in url for t in [".edu/uk", ".ac.uk", "ucas", "scholarships.org.uk"]):
            return "UK"
        if any(t in url for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
            return "Canada"
        if any(t in url for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
            return "Australia"
        return "USA"
    return "International"

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
# Extraction from search snippets
# ------------------------------------------------------------------
def extract_from_snippet(item: Dict) -> Optional[Dict]:
    title = item.get("title", "")
    text = item.get("text", "")
    url = item.get("url", "")
    
    combined = f"{title} {text}"
    
    # Must contain scholarship keyword
    if not re.search(r"scholarship|bursary|fellowship|grant|award", combined, re.I):
        return None
    
    # Extract amount - only match numbers with currency symbols to avoid
    # picking up years, title counts, and other non-amount numbers
    amounts = re.findall(r"[\$\€\£]\s*([0-9,]+)", combined.replace(",", ""))
    amount_min = None
    amount_max = None
    if amounts:
        nums = [int(a) for a in amounts if int(a) > 0]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            # Cap absurdly high amounts at $500,000
            if amount_min and amount_min > 500000:
                amount_min = None
            if amount_max and amount_max > 500000:
                amount_max = None
    
    # Extract deadline
    deadline = ""
    deadline_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", combined, re.I)
    if deadline_m:
        deadline = deadline_m.group(1)
    
    # Determine category
    category = "Academic"
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b", "Healthcare"),
        (r"\blaw\b|\blegal\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b", "Arts"),
    ]:
        if re.search(pat, combined, re.I):
            category = cat
            break
    
    # Determine education level
    level = "Undergraduate"
    for pat, lvl in [
        (r"\bhigh school\b|\bsecondary\b", "High School"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
    ]:
        if re.search(pat, combined, re.I):
            level = lvl
            break
    
    state = guess_state(combined)
    country = guess_country(url)
    
    return {
        "scholarship_name": title[:180],
        "organization": "Search Result",
        "organization_type": "Unknown",
        "description": text[:500],
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": parse_amount_display(amount_min, amount_max),
        "deadline": deadline,
        "application_url": url,
        "form_url": url,
        "email": "",
        "phone": "",
        "address": "",
        "website": url,
        "category": category,
        "education_level": level,
        "field_of_study": "",
        "state_restriction": state or "",
        "gpa_min": None,
        "citizenship": "None",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "source": "web_search",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "link_notes": "",
    }

# ------------------------------------------------------------------
# DB operations
# ------------------------------------------------------------------
def is_dup(conn: sqlite3.Connection, scholarship: Dict) -> bool:
    cur = conn.cursor()
    nh = name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", ""))
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

def verify_link(url: Optional[str]) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.head(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}

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
            scholarship.get("source", "web_search"),
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
# Main
# ------------------------------------------------------------------
def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    
    # Load all search result files
    candidates = []
    search_files = []
    for f in os.listdir(SEARCH_DIR):
        if f.startswith("web_search") and f.endswith(".json"):
            search_files.append(os.path.join(SEARCH_DIR, f))
    
    print(f"Found {len(search_files)} search result files")
    
    for sf in search_files:
        try:
            with open(sf, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, list):
                for item in data:
                    s = extract_from_snippet(item)
                    if s:
                        candidates.append(s)
            elif isinstance(data, dict):
                # Some files might be wrapped differently
                for item in data.get("results", data.get("data", [])):
                    s = extract_from_snippet(item)
                    if s:
                        candidates.append(s)
        except Exception as e:
            print(f"Error reading {sf}: {e}")
    
    print(f"Extracted {len(candidates)} candidates from search snippets")
    
    # Dedup within candidates
    seen = set()
    unique = []
    for c in candidates:
        key = normalize(c["scholarship_name"]) + "||" + normalize(c["organization"])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    print(f"After internal dedup: {len(unique)} unique candidates")
    
    # Verify and insert
    before = stats()
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    verified = []
    
    for c in unique[:limit]:
        # Check duplicates against DBs
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
        
        # Update final URL if redirected
        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]
        
        # Insert into both DBs
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            add_scholarship(conn, c)
            conn.close()
        added += 1
        verified.append(c)
    
    after = stats()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  DB totals before: {before}")
    print(f"  DB totals after: {after}")
    
    # Print breakdown by category
    from collections import Counter
    cats = Counter(c.get("category", "Unknown") for c in verified)
    print(f"\nBreakdown by category:")
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")
    
    # Print top 10 by amount
    top = sorted(verified, key=lambda x: x.get("amount_min") or 0, reverse=True)[:10]
    print(f"\nTop 10 by amount:")
    for c in top:
        print(f"  {c['amount_display']} - {c['scholarship_name'][:60]}")

if __name__ == "__main__":
    main()
