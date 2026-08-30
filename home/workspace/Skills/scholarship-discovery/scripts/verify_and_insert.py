#!/usr/bin/env python3
"""
Focused scholarship discovery from individual scholarship pages.
Reads search results, fetches individual scholarship pages,
verifies links, dedups, and inserts real scholarships.
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

def guess_country(url: str, text: str) -> str:
    combined = (url + " " + text).lower()
    if any(t in combined for t in ["canada", "canadian", "gc.ca", "scholarships.ca"]):
        return "Canada"
    if any(t in combined for t in ["uk", "british", "ucas", "scholarships.org.uk", "ac.uk"]):
        return "UK"
    if any(t in combined for t in ["australia", "australian", "edu.au", "studyassist"]):
        return "Australia"
    if any(t in combined for t in ["new zealand", "studylink"]):
        return "New Zealand"
    if any(t in combined for t in ["germany", "daad", "campusfrance", "erasmus"]):
        return "EU"
    if any(t in combined for t in ["international students", "worldwide", "global"]):
        return "International"
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
# Extraction from scholarship pages
# ------------------------------------------------------------------
def extract_from_studentscholarships(html: str, url: str) -> Optional[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    
    title = ""
    title_el = soup.find("h1")
    if title_el:
        title = title_el.get_text(strip=True)
    if not title:
        title = soup.find("title").get_text(strip=True) if soup.find("title") else ""
    
    # Clean title
    title = re.sub(r"\s*[-|].*$", "", title).strip()
    if not title or len(title) < 5:
        return None
    
    # Must contain scholarship keyword
    if not re.search(r"scholarship|bursary|fellowship|grant|award", title + " " + html[:2000], re.I):
        return None
    
    text = soup.get_text(separator=" ", strip=True)
    
    # Extract amount
    amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", text.replace(",", ""))
    amount_min = None
    amount_max = None
    if amounts:
        nums = [int(a) for a in amounts if int(a) > 0]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            if amount_min and amount_min > 500000:
                amount_min = None
            if amount_max and amount_max > 500000:
                amount_max = None
    
    # Extract deadline
    deadline = ""
    deadline_m = re.search(
        r"(?:deadline|due|closing|apply by|award deadline)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})",
        text, re.I
    )
    if deadline_m:
        deadline = deadline_m.group(1)
    
    # Extract organization
    org = ""
    org_m = re.search(r"(?:provided by|offered by|from the|by the)\s+([A-Z][A-Za-z\s&]+?)(?:\s*[-–]|\s*scholarship|\s*foundation|\s*program|\s*\.)", text[:2000])
    if org_m:
        org = org_m.group(1).strip()
    if not org:
        # Try to extract from domain
        domain = re.search(r"//([^/]+)/", url)
        if domain:
            org = domain.group(1).replace("www.", "").title()
    
    # Determine category
    category = "Academic"
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b", "Healthcare"),
        (r"\blaw\b|\blegal\b|\bimmigration\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b|\btheater\b|\bmusic\b", "Arts"),
        (r"\btrade\b|\btechnical\b|\bvocational\b|\bauto body\b|\baviation\b", "Trade School"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bveteran\b|\bmilitary\b", "Military/Veteran"),
        (r"\bhispanic\b|\blatino\b", "Academic"),
        (r"\bblack\b|\bafrican american\b", "Academic"),
    ]:
        if re.search(pat, title + " " + text[:3000], re.I):
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
        if re.search(pat, title + " " + text[:3000], re.I):
            level = lvl
            break
    
    state = guess_state(text)
    country = guess_country(url, text)
    
    # Look for application URL
    app_url = url
    apply_links = soup.find_all("a", string=re.compile(r"apply|application", re.I))
    if apply_links:
        for link in apply_links:
            href = link.get("href", "")
            if href and not href.startswith("#"):
                app_url = href if href.startswith("http") else requests.compat.urljoin(url, href)
                break
    
    return {
        "scholarship_name": title[:200],
        "organization": org[:200] if org else "Unknown",
        "organization_type": "Unknown",
        "description": text[:500],
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": parse_amount_display(amount_min, amount_max),
        "deadline": deadline,
        "application_url": app_url,
        "form_url": app_url,
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
        "source_id": hashlib.md5((title + org).encode()).hexdigest()[:12],
        "link_notes": "",
    }

def extract_from_generic(html: str, url: str) -> Optional[Dict]:
    """Generic extraction for scholarship listing pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    if not re.search(r"scholarship|bursary|fellowship|grant|award", text[:3000], re.I):
        return None
    
    title = soup.find("title")
    title_text = title.get_text(strip=True) if title else ""
    title_text = re.sub(r"\s*[-|].*$", "", title_text).strip()
    
    # Extract amounts
    amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", text.replace(",", ""))
    amount_min = None
    amount_max = None
    if amounts:
        nums = [int(a) for a in amounts if int(a) > 0]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            if amount_min and amount_min > 500000:
                amount_min = None
            if amount_max and amount_max > 500000:
                amount_max = None
    
    domain = re.search(r"//([^/]+)/", url)
    org = domain.group(1).replace("www.", "").title() if domain else "Unknown"
    
    return {
        "scholarship_name": title_text[:200] if title_text else "Scholarship",
        "organization": org[:200],
        "organization_type": "Unknown",
        "description": text[:500],
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": parse_amount_display(amount_min, amount_max),
        "deadline": "",
        "application_url": url,
        "form_url": url,
        "email": "",
        "phone": "",
        "address": "",
        "website": url,
        "category": "Academic",
        "education_level": "Undergraduate",
        "field_of_study": "",
        "state_restriction": "",
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
        # Use GET with stream to avoid downloading large bodies
        resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS, stream=True)
        final_url = resp.url
        status = resp.status_code
        resp.close()
        if status >= 400:
            return {"ok": False, "reason": f"http_{status}", "final_url": final_url}
        return {"ok": True, "status": status, "final_url": final_url}
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
                # Skip non-scholarship pages
                if not re.search(r"scholarship|bursary|fellowship|grant|award", url, re.I):
                    continue
                # Skip obvious listing/aggregator pages for now
                if any(t in url for t in ["/scholarships/", "/scholarship-directory", "/college-scholarships"]):
                    continue
                candidates.append({
                    "url": url,
                    "title": item.get("title", ""),
                    "text": item.get("text", ""),
                })
        except Exception as e:
            print(f"Error reading {sf}: {e}")
    
    print(f"Found {len(candidates)} individual scholarship candidates from search")
    
    # Dedup within candidates
    seen = set()
    unique = []
    for c in candidates:
        key = normalize(c["title"]) + "||" + normalize(c["url"])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    print(f"After internal dedup: {len(unique)} unique candidates")
    
    # Fetch and parse each candidate page
    parsed = []
    for c in unique[:limit]:
        url = c["url"]
        try:
            resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            if resp.status_code >= 400:
                continue
            html = resp.text
            resp.close()
            
            # Try specific extractors
            if "studentscholarships.org" in url:
                s = extract_from_studentscholarships(html, url)
            else:
                s = extract_from_generic(html, url)
            
            if s and len(s.get("scholarship_name", "")) > 5:
                parsed.append(s)
        except Exception as e:
            continue
    
    print(f"Parsed {len(parsed)} scholarships from pages")
    
    # Verify and insert
    before = stats()
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    verified = []
    
    for s in parsed[:limit]:
        # Check duplicates against DBs
        dup = False
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            if is_dup(conn, s):
                dup = True
                conn.close()
                break
            conn.close()
        if dup:
            skipped_dup += 1
            continue
        
        # Verify link
        vr = verify_link(s.get("application_url"))
        if not vr.get("ok"):
            skipped_verify += 1
            continue
        
        # Update final URL if redirected
        if vr.get("final_url"):
            s["application_url"] = vr["final_url"]
            s["form_url"] = vr["final_url"]
        
        # Insert into DBs
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            add_scholarship(conn, s)
            conn.close()
        added += 1
        verified.append(s)
    
    after = stats()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
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
