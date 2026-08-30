#!/usr/bin/env python3
"""
Parse structured scholarship data from web_search JSON snippets.
Reads web_search*.json from conversation workspace, extracts clean scholarship
entries from structured snippets (studentscholarships.org etc.), dedups,
verifies, and inserts.
"""
import os, sys, json, re, sqlite3, hashlib, time
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
SEARCH_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")
DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 15

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

def extract_studentscholarships(title: str, text: str, url: str) -> Optional[Dict]:
    if "studentscholarships.org/scholarship/" not in url:
        return None
    
    # Clean title
    name = title.replace("Scholarship Application - ", "").strip()
    if not name or len(name) < 5:
        return None
    
    # Extract amount - look for "Scholarship Value: $X" or "Award: $X" or dollar amounts
    amount_min = None
    amount_max = None
    amount_display = "Varies"
    
    # Try structured patterns first
    amt_match = re.search(r"Scholarship Value:\s*\$([0-9,]+)", text, re.I)
    if not amt_match:
        amt_match = re.search(r"Award.*?\$([0-9,]+)", text, re.I)
    if not amt_match:
        amt_match = re.search(r"\$([0-9,]+)\s*(?:scholarship|award|grant|prize)", text, re.I)
    if amt_match:
        amount_min = int(amt_match.group(1).replace(",", ""))
        amount_max = None
        amount_display = f"${amount_min:,}+"
    
    # Check for range
    range_match = re.search(r"\$([0-9,]+)\s*-\s*\$([0-9,]+)", text)
    if range_match:
        amount_min = int(range_match.group(1).replace(",", ""))
        amount_max = int(range_match.group(2).replace(",", ""))
        amount_display = f"${amount_min:,} - ${amount_max:,}"
    
    # Extract deadline
    deadline = ""
    deadline_m = re.search(r"(?:deadline|closing|apply by|due)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4})", text, re.I)
    if deadline_m:
        deadline = deadline_m.group(1)
    
    # Extract eligibility
    eligibility = ""
    elig_m = re.search(r"(?:eligib|criteria|requirements)[:\s]+(.{20,200})", text, re.I | re.S)
    if elig_m:
        eligibility = elig_m.group(1).strip()[:500]
    
    # Determine category
    category = "Academic"
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b", "Healthcare"),
        (r"\blaw\b|\blegal\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b", "Arts"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
    ]:
        if re.search(pat, text, re.I):
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
        if re.search(pat, text, re.I):
            level = lvl
            break
    
    # Extract organization
    org = "Unknown"
    org_m = re.search(r"(?:University|College|Foundation|Association|Institute|Society|Fund|Lodge|Organization|Corp|Inc|LLC)\b", text, re.I)
    if org_m:
        # Try to get the full org name
        start = max(0, org_m.start() - 50)
        end = min(len(text), org_m.end() + 50)
        org_snippet = text[start:end]
        org = re.sub(r"\s+", " ", org_snippet).strip()[:100]
    
    # For studentscholarships.org, often the org is implied by the scholarship name
    if org == "Unknown":
        org = name.split(" ")[0] + " Foundation" if len(name.split()) > 1 else "Scholarship Provider"
    
    return {
        "scholarship_name": name[:180],
        "organization": org[:180],
        "organization_type": "Unknown",
        "description": text[:500],
        "eligibility": eligibility[:500],
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
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
        "state_restriction": guess_state(text) or "",
        "gpa_min": None,
        "citizenship": "None",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "source": "web_search",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "link_notes": "Extracted from search snippet",
    }

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

def main():
    limit = 200
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
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
            items = data if isinstance(data, list) else data.get("results", data.get("data", []))
            for item in items:
                title = item.get("title", "")
                text = item.get("text", "")
                url = item.get("url", "")
                
                s = extract_studentscholarships(title, text, url)
                if s:
                    candidates.append(s)
        except Exception as e:
            print(f"Error reading {sf}: {e}")
    
    print(f"Extracted {len(candidates)} candidates from structured snippets")
    
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
    conn = sqlite3.connect(DB_PATH)
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    verified = []
    errors = []
    
    for c in unique[:limit]:
        if is_dup(conn, c):
            skipped_dup += 1
            continue
        
        vr = verify_link(c.get("application_url"))
        if not vr.get("ok"):
            skipped_verify += 1
            continue
        
        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]
        
        try:
            add_scholarship(conn, c)
            added += 1
            verified.append(c)
        except Exception as e:
            errors.append(str(e))
    
    conn.close()
    
    total = 8255 + added  # approximate, we'll query properly below
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM scholarships")
    after = cur.fetchone()[0]
    conn.close()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: {len(errors)}")
    print(f"  DB total after: {after}")
    
    # Breakdown by category
    from collections import Counter
    cats = Counter(c.get("category", "Unknown") for c in verified)
    print(f"\nBreakdown by category:")
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")
    
    # Top 10 by amount
    top = sorted(verified, key=lambda x: x.get("amount_min") or 0, reverse=True)[:10]
    print(f"\nTop 10 by amount:")
    for c in top:
        print(f"  {c['amount_display']} - {c['scholarship_name'][:60]}")

if __name__ == "__main__":
    main()
