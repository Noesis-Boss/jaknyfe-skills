#!/usr/bin/env python3
"""
Real scholarship discovery: fetch individual scholarship pages, extract data, verify links, insert.
"""
import os, sys, json, re, sqlite3, hashlib, time, random
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
SEARCH_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")
DB_PATHS = ["/home/workspace/scholarsearch-site/data/processed/scholarships.db"]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0)"}
REQUEST_TIMEOUT = 20

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
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk"]):
        return "UK"
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
        return "Canada"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
        return "Australia"
    if any(t in combined for t in [".edu", ".gov"]):
        return "USA"
    if any(t in combined for t in ["erasmus", "daad", "campusfrance", "studynetherlands"]):
        return "EU"
    return "International"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "washington": "WA", "tennessee": "TN", "missouri": "MO", "maryland": "MD",
        "minnesota": "MN", "wisconsin": "WI", "colorado": "CO", "alabama": "AL",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def extract_from_page(url: str, html: str) -> Optional[Dict]:
    soup = BeautifulSoup(html, "lxml")
    
    # Remove script/style
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    
    text = soup.get_text(separator=" ", strip=True)
    title = soup.title.string.strip() if soup.title else ""
    
    # Skip listing pages - check for indicators
    listing_indicators = [
        "list of scholarships", "top scholarships", "best scholarships",
        "scholarships for", "find scholarships", "browse scholarships",
        "scholarship search", "scholarship directory", "scholarship listings"
    ]
    if any(ind in title.lower() for ind in listing_indicators):
        return None
    if len(soup.find_all(["h2", "h3"])) > 15:
        return None
    
    # Must contain scholarship keyword
    combined = f"{title} {text}"
    if not re.search(r"scholarship|bursary|fellowship|grant|award", combined, re.I):
        return None
    
    # Extract amount
    amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", combined.replace(",", ""))
    amount_min = None
    amount_max = None
    if amounts:
        nums = [int(a) for a in amounts if 100 < int(a) < 1000000]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
    
    # Extract deadline
    deadline = ""
    deadline_m = re.search(
        r"(?:deadline|due|closing|apply by|application due)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})",
        combined, re.I
    )
    if deadline_m:
        deadline = deadline_m.group(1)
    
    # Extract organization
    org = ""
    org_m = re.search(
        r"(?:offered by|provided by|sponsored by|from the|by the)\s+([A-Z][A-Za-z\s&]+?(?:Foundation|University|College|Institute|Association|Organization|Society|Fund|Program|Lodge|Trust|Corporation|Bank|Company|Center|Group|Scholarship))",
        combined, re.I
    )
    if org_m:
        org = org_m.group(1).strip()
    
    if not org:
        # Try to extract from URL
        domain = re.search(r"https?://(?:www\.)?([^/]+)", url)
        if domain:
            org = domain.group(1).replace(".org", "").replace(".com", "").replace(".edu", "").title()
    
    # Determine category
    category = "Academic"
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b|\btechnology\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b|\bdental\b", "Healthcare"),
        (r"\blaw\b|\blegal\b|\battorney\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b|\bmusic\b|\btheater\b", "Arts"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bveteran\b|\bmilitary\b|\barmed forces\b", "Military/Veteran"),
        (r"\bhispanic\b|\blatino\b|\blatina\b", "Hispanic"),
        (r"\bblack\b|\bafrican american\b|\bafrican-american\b", "Black"),
        (r"\blgbtq\b|\btransgender\b|\bqueer\b|\bsexual orientation\b", "LGBTQ"),
        (r"\btrade\b|\btechnical\b|\bvocational\b|\bautomotive\b|\bhvac\b", "Trade School"),
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
        (r"\bhigh school\b|\bsecondary\b", "High School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
        (r"\bteacher\b|\beducation\b|\beducator\b", "Education"),
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
        (r"\bprofessional\b|\blaw school\b|\bmedical school\b", "Professional"),
    ]:
        if re.search(pat, combined, re.I):
            level = lvl
            break
    
    state = guess_state(combined)
    country = guess_country(url, text)
    
    # Clean up scholarship name
    name = title.replace(" - Scholarship Application", "").replace(" | Studentscholarships.org", "").strip()
    if len(name) > 200:
        name = name[:200]
    
    return {
        "scholarship_name": name,
        "organization": org[:200] if org else "Unknown",
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

def verify_link(url: str) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
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

def fetch_page(url: str) -> Optional[str]:
    try:
        resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return None

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
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("results", data.get("data", []))
            
            for item in items:
                url = item.get("url", "")
                if not url:
                    continue
                # Only process individual scholarship pages
                if not any(p in url for p in [
                    "/scholarship/", "/scholarships/", "/grant/", "/fellowship/",
                    "/award/", "/opportunity/", "/apply"
                ]):
                    continue
                # Skip listing pages
                if any(p in url for p in [
                    "/scholarships-by-", "/scholarships-", "list-of-",
                    "top-", "best-", "college-scholarships"
                ]):
                    continue
                candidates.append(url)
        except Exception as e:
            print(f"Error reading {sf}: {e}")
    
    # Dedup URLs
    candidates = list(dict.fromkeys(candidates))
    print(f"Found {len(candidates)} individual scholarship URLs")
    
    # Fetch and parse pages
    before = {}
    for path in DB_PATHS:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scholarships")
        before[path] = cur.fetchone()[0]
        conn.close()
    
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    skipped_parse = 0
    errors = 0
    verified = []
    
    for url in candidates[:limit]:
        html = fetch_page(url)
        if not html:
            skipped_verify += 1
            continue
        
        scholarship = extract_from_page(url, html)
        if not scholarship:
            skipped_parse += 1
            continue
        
        # Check duplicates
        dup = False
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            if is_dup(conn, scholarship):
                dup = True
                conn.close()
                break
            conn.close()
        if dup:
            skipped_dup += 1
            continue
        
        # Verify link
        vr = verify_link(scholarship.get("application_url"))
        if not vr.get("ok"):
            skipped_verify += 1
            continue
        
        if vr.get("final_url"):
            scholarship["application_url"] = vr["final_url"]
            scholarship["form_url"] = vr["final_url"]
        
        # Insert
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            try:
                add_scholarship(conn, scholarship)
            except Exception as e:
                print(f"Insert error: {e}")
                errors += 1
            conn.close()
        added += 1
        verified.append(scholarship)
        print(f"  Added: {scholarship['scholarship_name'][:60]} ({scholarship['category']})")
        
        if added >= limit:
            break
    
    after = {}
    for path in DB_PATHS:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scholarships")
        after[path] = cur.fetchone()[0]
        conn.close()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Skipped (parse): {skipped_parse}")
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

if __name__ == "__main__":
    main()
