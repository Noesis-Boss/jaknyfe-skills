#!/usr/bin/env python3
"""
Extract real individual scholarships from saved web_search JSON results.
Fetches each candidate page, parses structured scholarship data, verifies links, and inserts.
"""
import os, sys, json, re, sqlite3, hashlib, time, random, argparse
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
SEARCH_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0; +https://jaknyfe.zo.space)"}
REQUEST_TIMEOUT = 20
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

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
    lower = url.lower() + " " + text.lower()
    if any(t in lower for t in [".gc.ca", "canada.ca", "scholarships.ca", "university of toronto", "mcgill", "ubc"]):
        return "Canada"
    if any(t in lower for t in [".ac.uk", "ucas", "scholarships.org.uk", "oxford", "cambridge", "imperial", "edinburgh"]):
        return "UK"
    if any(t in lower for t in ["edu.au", "studyassist", "scholarships.gov.au", "university of sydney", "university of melbourne"]):
        return "Australia"
    if any(t in lower for t in ["europa.eu", "erasmus", "daad", "campusfrance", "studynetherlands", "ethz", "oxford", "cambridge"]):
        return "EU"
    if any(t in lower for t in [".edu", ".gov", "scholarships.com", "fastweb", "bold.org", "cappex"]):
        return "USA"
    return "International"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "new jersey": "NJ", "maryland": "MD", "minnesota": "MN", "missouri": "MO",
        "wisconsin": "WI", "tennessee": "TN", "indiana": "IN", "alabama": "AL",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def extract_amount_from_text(text: str) -> Tuple[Optional[int], Optional[int], str]:
    amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", text.replace(",", ""))
    amount_min = None
    amount_max = None
    if amounts:
        nums = [int(a) for a in amounts if 10 < int(a) < 500000]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
    return amount_min, amount_max, parse_amount_display(amount_min, amount_max)

def categorize(text: str, url: str) -> str:
    combined = (text + " " + url).lower()
    if re.search(r"\bmasonic\b", combined):
        return "Masonic"
    if re.search(r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", combined):
        return "STEM"
    if re.search(r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", combined):
        return "Healthcare"
    if re.search(r"\blaw\b|\blegal\b|\battorney\b", combined):
        return "Law"
    if re.search(r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", combined):
        return "Business"
    if re.search(r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", combined):
        return "Arts"
    if re.search(r"\btrade\b|\btechnical\b|\bvocational\b|\bwelding\b|\bautomotive\b", combined):
        return "Trade School"
    if re.search(r"\bwomen\b|\bfemale\b", combined):
        return "Women"
    if re.search(r"\bmilitary\b|\bveteran\b|\barmed forces\b", combined):
        return "Military/Veteran"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b|\bph\.?d\b|\bdoctorate\b", combined):
        return "Graduate"
    if re.search(r"\bcommunity\b|\bvolunteer\b|\bservice\b", combined):
        return "Community"
    return "Academic"

def guess_education_level(text: str) -> str:
    lower = text.lower()
    if re.search(r"\bph\.?d\b|\bdoctorate\b", lower):
        return "PhD"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b", lower):
        return "Graduate"
    if re.search(r"\btrade\b|\btechnical\b|\bvocational\b", lower):
        return "Trade School"
    if re.search(r"\bassociate\b|\bcommunity college\b", lower):
        return "Associate"
    if re.search(r"\bhigh school\b|\bsecondary\b", lower):
        return "High School"
    return "Undergraduate"

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
        resp = SESSION.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        # Basic check: page should contain scholarship-related content
        ct = resp.text.lower()
        if not re.search(r"scholarship|bursary|fellowship|grant|award|application", ct):
            return {"ok": False, "reason": "not_scholarship_page", "final_url": final_url}
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
            scholarship.get("source", "batch_discover2"),
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
# Page parsing
# ------------------------------------------------------------------
def extract_from_studentscholarships(html: str, url: str) -> List[Dict]:
    """Parse studentscholarships.org individual scholarship pages."""
    soup = BeautifulSoup(html, "lxml")
    results = []
    
    # Remove footer/header noise
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    
    title = soup.find("h1")
    name = title.get_text(strip=True) if title else ""
    if not name or len(name) < 5:
        return results
    
    # Extract org from breadcrumb or meta
    org = "Unknown"
    bc = soup.find("nav", {"aria-label": "breadcrumb"})
    if bc:
        links = bc.find_all("a")
        if len(links) >= 2:
            org = links[-2].get_text(strip=True)
    
    # Extract value
    value = "Varies"
    amount_min = None
    amount_max = None
    val_match = re.search(r"\$([0-9,]+)", html)
    if val_match:
        nums = [int(v.replace(",", "")) for v in re.findall(r"\$([0-9,]+)", html) if int(v.replace(",", "")) < 500000]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            value = parse_amount_display(amount_min, amount_max)
    
    # Extract deadline
    deadline = ""
    dl_match = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", html, re.I)
    if dl_match:
        deadline = dl_match.group(1)
    
    # Extract description
    desc = ""
    main = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile("content|main", re.I))
    if main:
        desc = main.get_text(separator=" ", strip=True)[:800]
    else:
        body = soup.find("body")
        if body:
            desc = body.get_text(separator=" ", strip=True)[:800]
    
    results.append({
        "scholarship_name": name[:180],
        "organization": org,
        "organization_type": "Foundation",
        "description": desc,
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": value,
        "deadline": deadline,
        "application_url": url,
        "form_url": url,
        "email": "",
        "phone": "",
        "address": "",
        "website": url,
        "category": categorize(name + " " + desc, url),
        "education_level": guess_education_level(name + " " + desc),
        "field_of_study": "",
        "state_restriction": guess_state(name + " " + desc) or "",
        "gpa_min": None,
        "citizenship": "None",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "source": "batch_discover2",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "link_notes": "",
    })
    return results

def extract_from_bold(html: str, url: str) -> List[Dict]:
    """Parse bold.org scholarship listing pages."""
    soup = BeautifulSoup(html, "lxml")
    results = []
    
    cards = soup.find_all("a", href=re.compile(r"/scholarships/"))
    seen_urls = set()
    
    for card in cards:
        href = card.get("href", "")
        if not href.startswith("http"):
            href = "https://bold.org" + href
        
        # Skip listing/filter pages
        if re.search(r"/by-|/type/|/demographics/", href):
            continue
        
        name = card.get_text(strip=True)
        if not name or len(name) < 5 or name in seen_urls:
            continue
        seen_urls.add(name)
        
        # Find amount nearby
        amount_min = None
        amount_max = None
        parent = card.find_parent()
        if parent:
            text = parent.get_text(separator=" ", strip=True)
            amt_match = re.search(r"\$([0-9,]+)", text)
            if amt_match:
                nums = [int(v.replace(",", "")) for v in re.findall(r"\$([0-9,]+)", text) if int(v.replace(",", "")) < 500000]
                if nums:
                    amount_min = min(nums)
                    amount_max = max(nums) if len(nums) > 1 else None
        
        results.append({
            "scholarship_name": name[:180],
            "organization": "bold.org",
            "organization_type": "Platform",
            "description": "",
            "eligibility": "",
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": "",
            "application_url": href,
            "form_url": href,
            "email": "",
            "phone": "",
            "address": "",
            "website": href,
            "category": "Academic",
            "education_level": "Undergraduate",
            "field_of_study": "",
            "state_restriction": "",
            "gpa_min": None,
            "citizenship": "None",
            "ethnicity": "",
            "gender": "",
            "military_affiliation": "",
            "source": "batch_discover2",
            "source_id": hashlib.md5(href.encode()).hexdigest()[:12],
            "link_notes": "",
        })
    return results[:50]

def extract_from_scholarships360(html: str, url: str) -> List[Dict]:
    """Parse scholarships360.org listing pages."""
    soup = BeautifulSoup(html, "lxml")
    results = []
    
    cards = soup.find_all(["h2", "h3", "h4"], string=re.compile(r"scholarship", re.I))
    seen = set()
    
    for card in cards:
        name = card.get_text(strip=True)
        if not name or len(name) < 10 or name in seen:
            continue
        seen.add(name)
        
        link = card.find("a")
        href = link.get("href", "") if link else url
        if href and not href.startswith("http"):
            href = "https://scholarships360.org" + href
        
        # Find amount in parent
        amount_min = None
        amount_max = None
        parent = card.find_parent()
        if parent:
            text = parent.get_text(separator=" ", strip=True)
            nums = [int(v.replace(",", "")) for v in re.findall(r"\$([0-9,]+)", text) if int(v.replace(",", "")) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
        
        results.append({
            "scholarship_name": name[:180],
            "organization": "Scholarships360",
            "organization_type": "Platform",
            "description": "",
            "eligibility": "",
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": "",
            "application_url": href,
            "form_url": href,
            "email": "",
            "phone": "",
            "address": "",
            "website": href,
            "category": "Academic",
            "education_level": "Undergraduate",
            "field_of_study": "",
            "state_restriction": "",
            "gpa_min": None,
            "citizenship": "None",
            "ethnicity": "",
            "gender": "",
            "military_affiliation": "",
            "source": "batch_discover2",
            "source_id": hashlib.md5(href.encode()).hexdigest()[:12],
            "link_notes": "",
        })
    return results[:50]

def extract_generic(html: str, url: str) -> List[Dict]:
    """Generic extraction from listing pages with structured cards."""
    soup = BeautifulSoup(html, "lxml")
    results = []
    
    # Look for cards or list items that mention scholarship and have amounts
    candidates = soup.find_all(["div", "li", "article", "tr"], class_=re.compile(r"scholarship|grant|award|card|item", re.I))
    
    for cand in candidates[:100]:
        text = cand.get_text(separator=" ", strip=True)
        if not re.search(r"scholarship|bursary|fellowship|grant|award", text, re.I):
            continue
        if len(text) < 20:
            continue
        
        # Try to extract name
        name_tag = cand.find(["h2", "h3", "h4", "h5", "a", "strong", "b"])
        name = name_tag.get_text(strip=True) if name_tag else text[:100]
        
        # Extract link
        link = cand.find("a", href=True)
        href = link.get("href", "") if link else ""
        if href and not href.startswith("http"):
            href = requests.compat.urljoin(url, href)
        
        # Extract amount
        amount_min, amount_max, value = extract_amount_from_text(text)
        
        # Extract deadline
        deadline = ""
        dl_match = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
        if dl_match:
            deadline = dl_match.group(1)
        
        results.append({
            "scholarship_name": name[:180],
            "organization": "Unknown",
            "organization_type": "Unknown",
            "description": text[:500],
            "eligibility": "",
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": value,
            "deadline": deadline,
            "application_url": href or url,
            "form_url": href or url,
            "email": "",
            "phone": "",
            "address": "",
            "website": href or url,
            "category": categorize(text, url),
            "education_level": guess_education_level(text),
            "field_of_study": "",
            "state_restriction": guess_state(text) or "",
            "gpa_min": None,
            "citizenship": "None",
            "ethnicity": "",
            "gender": "",
            "military_affiliation": "",
            "source": "batch_discover2",
            "source_id": hashlib.md5((name + href).encode()).hexdigest()[:12],
            "link_notes": "",
        })
    return results[:50]

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("limit", nargs="?", type=int, default=200)
    parser.add_argument("--skip-dupes", action="store_true")
    args = parser.parse_args()
    limit = args.limit
    
    # Load all search result files
    search_files = []
    for f in os.listdir(SEARCH_DIR):
        if f.startswith("web_search") and f.endswith(".json"):
            search_files.append(os.path.join(SEARCH_DIR, f))
    print(f"Found {len(search_files)} search result files")
    
    # Collect candidate URLs
    candidates = []
    for sf in search_files:
        try:
            with open(sf, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            items = data if isinstance(data, list) else data.get("results", data.get("data", []))
            for item in items:
                url = item.get("url", "")
                title = item.get("title", "")
                text = item.get("text", "")
                
                # Skip obvious listing/filter pages
                if re.search(r"/by-|/type/|/state/|/major/|/demographics/", url):
                    continue
                if re.search(r"list|directory|catalog|aggregator", title, re.I) and not re.search(r"scholarship", title, re.I):
                    continue
                
                candidates.append({"url": url, "title": title, "text": text})
        except Exception as e:
            print(f"Error reading {sf}: {e}")
    
    # Dedup candidates
    seen_urls = set()
    unique_candidates = []
    for c in candidates:
        if c["url"] not in seen_urls:
            seen_urls.add(c["url"])
            unique_candidates.append(c)
    print(f"Unique candidate URLs: {len(unique_candidates)}")
    
    # Fetch and parse pages
    all_scholarships = []
    fetched = 0
    failed = 0
    
    for c in unique_candidates[: min(len(unique_candidates), limit * 3)]:
        url = c["url"]
        if not url or not url.startswith("http"):
            continue
        
        try:
            resp = SESSION.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
            html = resp.text
            fetched += 1
            
            # Choose parser based on domain
            if "studentscholarships.org" in url:
                items = extract_from_studentscholarships(html, url)
            elif "bold.org" in url:
                items = extract_from_bold(html, url)
            elif "scholarships360.org" in url:
                items = extract_from_scholarships360(html, url)
            else:
                items = extract_generic(html, url)
            
            all_scholarships.extend(items)
            time.sleep(0.3)
        except Exception as e:
            failed += 1
            continue
    
    print(f"Fetched {fetched} pages, {failed} failed, extracted {len(all_scholarships)} scholarships")
    
    # Dedup within candidates
    seen_keys = set()
    unique_scholarships = []
    for s in all_scholarships:
        key = normalize(s["scholarship_name"]) + "||" + normalize(s["organization"])
        if key not in seen_keys:
            seen_keys.add(key)
            unique_scholarships.append(s)
    print(f"After internal dedup: {len(unique_scholarships)}")
    
    # Verify and insert
    before = stats()
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    verified = []
    
    for s in unique_scholarships[:limit]:
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
        
        vr = verify_link(s.get("application_url"))
        if not vr.get("ok"):
            skipped_verify += 1
            continue
        
        if vr.get("final_url"):
            s["application_url"] = vr["final_url"]
            s["form_url"] = vr["final_url"]
        
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
    cats = Counter(s.get("category", "Unknown") for s in verified)
    print(f"\nBreakdown by category:")
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")
    
    top = sorted(verified, key=lambda x: x.get("amount_min") or 0, reverse=True)[:10]
    print(f"\nTop 10 by amount:")
    for s in top:
        print(f"  {s['amount_display']} - {s['scholarship_name'][:60]}")

if __name__ == "__main__":
    main()
