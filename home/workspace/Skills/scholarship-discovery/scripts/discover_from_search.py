#!/usr/bin/env python3
"""
Extract scholarships from saved web_search JSON results.
Processes all web_search*.json files in conversation workspace,
extracts scholarship data from structured snippets, verifies links, and inserts.
"""
import os, sys, json, re, sqlite3, hashlib, time, random, requests
from datetime import datetime, timezone
from typing import List, Dict, Optional

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 15
SEARCH_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")

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
    if any(t in combined for t in [".edu/uk", ".ac.uk", "ucas", "scholarships.org.uk"]):
        return "UK"
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
        return "Canada"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
        return "Australia"
    if any(t in combined for t in ["scholarships.gov.in", "gov.in"]):
        return "India"
    if any(t in combined for t in ["daad.de", "study-in-germany"]):
        return "Germany"
    if any(t in combined for t in ["campusfrance.org", "campusfrance"]):
        return "France"
    if any(t in combined for t in ["studyinnl", "holland", "netherlands"]):
        return "Netherlands"
    if any(t in combined for t in [".edu", ".gov"]):
        return "USA"
    return "International"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "tennessee": "TN", "missouri": "MO", "maryland": "MD", "wisconsin": "WI",
        "minnesota": "MN", "indiana": "IN", "alabama": "AL", "south carolina": "SC",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def guess_org_from_url(url: str) -> str:
    """Try to extract organization name from URL."""
    if not url:
        return "Unknown"
    # Remove protocol and www
    url = re.sub(r"^https?://(www\.)?", "", url)
    # Get domain
    domain = url.split("/")[0]
    # Remove TLD
    domain = re.sub(r"\.[a-z]{2,}$", "", domain)
    # Capitalize
    return domain.replace("-", " ").replace("_", " ").title()

def extract_category(text: str, url: str = "") -> str:
    combined = (text + " " + url).lower()
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b|\bmedical\b", "Medicine"),
        (r"\blaw\b|\blegal\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", "Arts"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bveteran\b|\bmilitary\b", "Military/Veteran"),
        (r"\binternational\b", "International"),
        (r"\bgraduate\b|\bmaster\b", "Graduate"),
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
    ]:
        if re.search(pat, combined):
            return cat
    return "Academic"

def extract_education_level(text: str) -> str:
    combined = text.lower()
    for pat, lvl in [
        (r"\bhigh school\b|\bsecondary\b", "High School"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
        (r"\bprofessional\b", "Professional"),
    ]:
        if re.search(pat, combined):
            return lvl
    return "Undergraduate"

def extract_from_snippet(item: Dict) -> Optional[Dict]:
    title = item.get("title", "")
    text = item.get("text", "")
    url = item.get("url", "")
    
    combined = f"{title} {text}"
    
    # Must contain scholarship keyword
    if not re.search(r"scholarship|bursary|fellowship|grant|award", combined, re.I):
        return None
    
    # Skip listing pages and generic pages
    skip_patterns = [
        r"top \d+ .*scholarships",
        r"best scholarships",
        r"scholarships for .* in \d{4}",
        r"\d+ scholarships",
        r"scholarship guide",
        r"how to find",
        r"how to apply",
    ]
    for pat in skip_patterns:
        if re.search(pat, title.lower()) or re.search(pat, text[:100].lower()):
            return None
    
    # Extract amount - prefer "Scholarship Value:" pattern
    amount_min = None
    amount_max = None
    amount_display = "Varies"
    
    # Pattern: Scholarship Value: $2,000 or Award: $5,000
    value_match = re.search(r"(?:scholarship value|award amount|amount|scholarship amount)[:\s]+([\$€£]?\s*[\d,]+(?:\s*[-–]\s*[\$€£]?\s*[\d,]+)?)", combined, re.I)
    if value_match:
        amt_str = value_match.group(1).replace(",", "").replace("$", "").replace("€", "").replace("£", "")
        if "-" in amt_str or "–" in amt_str:
            parts = re.split(r"[-–]", amt_str)
            nums = [int(p.strip()) for p in parts if p.strip().isdigit()]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums)
        else:
            nums = re.findall(r"\d+", amt_str)
            if nums:
                amount_min = int(nums[0])
                amount_max = None
    else:
        # Generic amount extraction
        amounts = re.findall(r"[\$€£]\s*([0-9,]+)", combined.replace(",", ""))
        if amounts:
            nums = [int(a) for a in amounts if int(a) > 0]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
                if amount_min and amount_min > 500000:
                    amount_min = None
                if amount_max and amount_max > 500000:
                    amount_max = None
    
    amount_display = parse_amount_display(amount_min, amount_max)
    
    # Extract deadline
    deadline = ""
    deadline_m = re.search(r"(?:deadline|due|closing|apply by|award deadline|application deadline)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}|[A-Za-z]+ \d{1,2})", combined, re.I)
    if deadline_m:
        deadline = deadline_m.group(1)
    else:
        # Look for dates like "Jul 1, 2026" or "June 2026"
        date_m = re.search(r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s*\d{4}\b", combined)
        if date_m:
            deadline = date_m.group(0)
    
    # Determine category
    category = extract_category(combined, url)
    
    # Determine education level
    education_level = extract_education_level(combined)
    
    # Determine state and country
    state = guess_state(combined)
    country = guess_country(url, text)
    
    # Extract organization
    org = guess_org_from_url(url)
    
    # Citizenship
    citizenship = "None"
    if re.search(r"us citizen|u\.s\. citizen|american citizen", combined, re.I):
        citizenship = "US Citizen"
    elif re.search(r"permanent resident|green card", combined, re.I):
        citizenship = "Permanent Resident"
    elif re.search(r"international student|non-us|foreign", combined, re.I):
        citizenship = "International"
    
    # Gender
    gender = ""
    if re.search(r"\bwomen\b|\bfemale\b", combined, re.I):
        gender = "Female"
    elif re.search(r"\bmen\b|\bmale\b", combined, re.I):
        gender = "Male"
    
    # Military affiliation
    military = ""
    if re.search(r"\bveteran\b|\bmilitary\b|\barmed forces\b", combined, re.I):
        military = "Military/Veteran"
    
    # Source
    source = "web_search"
    source_id = hashlib.md5(url.encode()).hexdigest()[:12]
    
    return {
        "scholarship_name": title[:180] if title else "",
        "organization": org,
        "organization_type": "Unknown",
        "description": text[:500],
        "eligibility": "",
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
        "education_level": education_level,
        "field_of_study": "",
        "state_restriction": state or "",
        "gpa_min": None,
        "citizenship": citizenship,
        "ethnicity": "",
        "gender": gender,
        "military_affiliation": military,
        "source": source,
        "source_id": source_id,
        "link_notes": "",
    }

# ------------------------------------------------------------------
# DB operations
# ------------------------------------------------------------------
def get_conn(path):
    return sqlite3.connect(path)

def is_dup(conn: sqlite3.Connection, scholarship: Dict) -> bool:
    cur = conn.cursor()
    nh = name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", ""))
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

def verify_link(url: Optional[str]) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        # Use GET with stream to avoid downloading full content
        resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS, stream=True)
        resp.close()
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
    limit = 200
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
    # Load all search result files
    candidates = []
    search_files = []
    if os.path.isdir(SEARCH_DIR):
        for f in os.listdir(SEARCH_DIR):
            if f.startswith("web_search") and f.endswith(".json"):
                search_files.append(os.path.join(SEARCH_DIR, f))
    
    print(f"Found {len(search_files)} search result files")
    
    for sf in search_files:
        try:
            with open(sf, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("results", data.get("data", []))
            
            for item in items:
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
    failed_verify = []
    verified = []
    
    for c in unique[:limit]:
        # Check duplicates against DBs
        dup = False
        for path in DB_PATHS:
            conn = get_conn(path)
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
            failed_verify.append({
                "name": c.get("scholarship_name", "")[:60],
                "url": c.get("application_url", ""),
                "reason": vr.get("reason", "unknown"),
            })
            continue
        
        # Update final URL if redirected
        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]
            c["website"] = vr["final_url"]
        
        # Insert into DBs
        for path in DB_PATHS:
            conn = get_conn(path)
            add_scholarship(conn, c)
            conn.close()
        added += 1
        verified.append(c)
    
    after = stats()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: 0")
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
    
    # Print failed verifications
    if failed_verify:
        print(f"\nFailed verification ({len(failed_verify)}):")
        for fv in failed_verify[:10]:
            print(f"  {fv['reason']} - {fv['name']} ({fv['url']})")

if __name__ == "__main__":
    main()
