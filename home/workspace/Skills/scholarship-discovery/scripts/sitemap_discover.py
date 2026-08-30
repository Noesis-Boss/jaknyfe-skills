#!/usr/bin/env python3
"""
Sitemap-based scholarship discovery.
Fetches sitemaps from studentscholarships.org, scholarships.com, bold.org,
fetches individual scholarship pages, extracts structured data, verifies links,
deduplicates, and inserts into DBs.
"""
import os, sys, json, re, sqlite3, hashlib, time, random, argparse
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup

DB_PATHS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0; +https://jaknyfe.zo.space)"}
REQUEST_TIMEOUT = 20
MAX_WORKERS = 25
BATCH_LIMIT_DEFAULT = 200
JITTER = (0.2, 0.8)

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
            scholarship.get("source", "sitemap_discover"),
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

def deadline_is_current(value: Optional[str]) -> bool:
    if not value:
        return True
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.replace(",", ""), fmt.replace(",", "")).date() >= datetime.now(timezone.utc).date()
        except ValueError:
            pass
    return True

# ------------------------------------------------------------------ #
# Geo + category tagging
# ------------------------------------------------------------------ #
RESIDENCY_TOKENS = {
    "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
    "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
    "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
    "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
    "new jersey": "NJ", "maryland": "MD", "minnesota": "MN", "missouri": "MO",
    "wisconsin": "WI", "tennessee": "TN", "indiana": "IN", "alabama": "AL",
    "south carolina": "SC", "kentucky": "KY", "louisiana": "LA", "oklahoma": "OK",
    "connecticut": "CT", "iowa": "IA", "kansas": "KS", "arkansas": "AR",
}

def guess_country(url: str, text: str = "") -> str:
    lower = url.lower() + " " + text.lower()
    if any(t in lower for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
        return "Canada"
    if any(t in lower for t in [".ac.uk", "ucas", "scholarships.org.uk", "oxford", "cambridge"]):
        return "UK"
    if any(t in lower for t in ["edu.au", "studyassist", "scholarships.gov.au", "melbourne", "sydney"]):
        return "Australia"
    if any(t in lower for t in ["studylink", "new zealand", "nz gov"]):
        return "New Zealand"
    if any(t in lower for t in ["europa.eu", "erasmus", "daad", "campusfrance", "studynetherlands"]):
        return "EU"
    if any(t in lower for t in [".edu", ".gov", "university", "college"]):
        return "USA"
    return "International"

def guess_state(text: str) -> Optional[str]:
    lower = text.lower()
    for name, abbr in RESIDENCY_TOKENS.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

CATEGORY_RULES = [
    (re.compile(r"\bmasonic\b", re.I), "Masonic"),
    (re.compile(r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", re.I), "STEM"),
    (re.compile(r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", re.I), "Medicine"),
    (re.compile(r"\blaw\b|\blegal\b", re.I), "Law"),
    (re.compile(r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", re.I), "Business"),
    (re.compile(r"\bart\b|\bdesign\b|\bcreative\b", re.I), "Arts"),
    (re.compile(r"\btrade\b|\btechnical\b|\bvocational\b|\bwelding\b|\bautomotive\b", re.I), "Trade School"),
    (re.compile(r"\bwomen\b|\bfemale\b", re.I), "Women"),
    (re.compile(r"\bveteran\b|\bmilitary\b", re.I), "Military/Veteran"),
    (re.compile(r"\bcommunity\b|\bvolunteer\b|\bservice\b", re.I), "Community"),
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

# ------------------------------------------------------------------ #
# Sitemap fetching
# ------------------------------------------------------------------ #
def fetch_sitemap_urls(sitemap_url: str) -> List[str]:
    try:
        r = requests.get(sitemap_url, timeout=30, headers=HEADERS)
        r.raise_for_status()
        urls = re.findall(r"<loc>(.*?)</loc>", r.text)
        return urls
    except Exception as e:
        print(f"  sitemap fetch error {sitemap_url}: {e}")
        return []

def get_scholarship_urls() -> List[str]:
    all_urls = []
    
    # studentscholarships.org sitemap
    print("Fetching studentscholarships.org sitemap...")
    ss_urls = fetch_sitemap_urls("https://studentscholarships.org/sitemaps/scholarships.xml")
    ss_scholarship = [u for u in ss_urls if re.match(r"https://studentscholarships\.org/scholarship/\d+", u)]
    print(f"  studentscholarships: {len(ss_scholarship)} scholarship URLs")
    all_urls.extend(ss_scholarship)
    
    # scholarships.com sitemap
    print("Fetching scholarships.com sitemap...")
    sc_urls = fetch_sitemap_urls("https://www.scholarships.com/scholarshipsitemap.xml")
    sc_scholarship = [u for u in sc_urls if re.match(r"https://www\.scholarships\.com/scholarships/[^/]+", u)]
    print(f"  scholarships.com: {len(sc_scholarship)} scholarship URLs")
    all_urls.extend(sc_scholarship)
    
    # bold.org sitemap
    print("Fetching bold.org sitemap...")
    bo_urls = fetch_sitemap_urls("https://bold.org/sitemap.xml")
    bo_scholarship = [u for u in bo_urls if re.match(r"https://bold\.org/scholarships/[^/]+/?$", u)]
    print(f"  bold.org: {len(bo_scholarship)} scholarship URLs")
    all_urls.extend(bo_scholarship)
    
    # Deduplicate by URL
    unique = list(dict.fromkeys(all_urls))
    print(f"Total unique scholarship URLs: {len(unique)}")
    return unique

# ------------------------------------------------------------------ #
# Page extraction
# ------------------------------------------------------------------ #
def extract_studentscholarships(html: str, url: str) -> Optional[Dict]:
    """Extract from studentscholarships.org individual pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    # Get title from URL slug or page
    slug = re.search(r"/scholarship/\d+/([^/]+)", url)
    name_from_url = slug.group(1).replace("-", " ").title() if slug else ""
    
    # Try to find h1 or title
    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""
    
    # Skip listing pages
    if len(soup.find_all(["h2", "h3"])) > 15:
        return None
    
    # Must contain scholarship keyword
    combined = f"{h1_text} {text}"
    if not re.search(r"scholarship|bursary|fellowship|grant|award", combined, re.I):
        return None
    
    # Extract amount
    amount_min = None
    amount_max = None
    amount_display = "Varies"
    
    val_match = re.search(r"Scholarship Value:\s*\$([0-9,]+)", text)
    if val_match:
        amount_min = int(val_match.group(1).replace(",", ""))
        amount_display = f"${amount_min:,}"
    else:
        amounts = re.findall(r"\$([0-9,]+)", combined.replace(",", ""))
        if amounts:
            nums = [int(a) for a in amounts if 10 < int(a) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
                amount_display = parse_amount_display(amount_min, amount_max)
    
    # Extract deadline
    deadline = ""
    dl_match = re.search(r"(?:Deadline|Award Deadline|Due Date|Apply By)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
    if dl_match:
        deadline = dl_match.group(1).strip()
    
    # Extract application URL
    application_url = None
    for a in soup.find_all("a", href=re.compile(r"http", re.I)):
        a_text = a.get_text(strip=True).lower()
        if "go to scholarship application" in a_text or "apply now" in a_text or "application" in a_text:
            application_url = a.get("href")
            break
    
    if not application_url:
        # Fallback: look for external links
        for a in soup.find_all("a", href=re.compile(r"^https?://(?!studentscholarships)", re.I)):
            href = a.get("href", "")
            if "scholarship" in href.lower() or "apply" in href.lower():
                application_url = href
                break
    
    # Extract organization
    org = "Unknown"
    org_match = re.search(r"(?:Sponsored by|Provided by|From|by)\s+([A-Z][A-Za-z0-9 &]+?)(?:\s+\.?\s|$)", text)
    if org_match:
        org = org_match.group(1).strip()
    else:
        # Try domain from URL
        domain = re.search(r"https?://(?:www\.)?([^/]+)", url)
        if domain:
            org = domain.group(1).replace(".org", "").replace(".com", "").replace("-", " ").title()
    
    # Extract eligibility snippet
    eligibility = ""
    elig_match = re.search(r"(?:eligibility|who can apply|eligible)[:\s]+(.{50,300}?)(?:\.[\s\n]|$)", text, re.I)
    if elig_match:
        eligibility = elig_match.group(1).strip()[:300]
    
    name = h1_text if h1_text else name_from_url
    
    scholarship_id = re.search(r"/scholarship/(\d+)", url).group(1)
    return {
        "scholarship_name": name[:180],
        "organization": org[:120],
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "application_url": application_url,
        "website": url,
        "description": text[:300],
        "eligibility": eligibility,
        "category": tag_category(name, org, text),
        "education_level": tag_level(name, text),
        "state_restriction": guess_state(text),
        "source": "studentscholarships_sitemap",
        "source_id": f"ss_{scholarship_id}",
    }

def extract_scholarshipscom(html: str, url: str) -> Optional[Dict]:
    """Extract from scholarships.com individual pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    title = soup.find("title")
    title_text = title.get_text(strip=True) if title else ""
    name = title_text.replace(" - Scholarships.com", "").strip()
    
    h1 = soup.find("h1")
    if h1:
        name = h1.get_text(strip=True)
    
    if not re.search(r"scholarship|bursary|fellowship|grant|award", name + " " + text, re.I):
        return None
    
    # Extract amount from title or meta
    amount_min = None
    amount_max = None
    amount_display = "Varies"
    
    amt_match = re.search(r"\$([0-9,]+)", name)
    if amt_match:
        amount_min = int(amt_match.group(1).replace(",", ""))
        amount_display = f"${amount_min:,}"
    else:
        amounts = re.findall(r"\$([0-9,]+)", text.replace(",", ""))
        if amounts:
            nums = [int(a) for a in amounts if 10 < int(a) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
                amount_display = parse_amount_display(amount_min, amount_max)
    
    # Extract deadline
    deadline = ""
    dl_match = re.search(r"(?:Deadline|Due|Apply By|Closing)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
    if dl_match:
        deadline = dl_match.group(1).strip()
    
    # Extract application URL - look for external links or apply buttons
    application_url = None
    for a in soup.find_all("a", href=re.compile(r"^https?://", re.I)):
        href = a.get("href", "")
        a_text = a.get_text(strip=True).lower()
        if any(x in a_text for x in ["apply", "application", "submit", "register"]):
            if "scholarships.com" not in href or "scc.aspx" in href:
                application_url = href
                break
    
    if not application_url:
        # Look for any external link that isn't social
        for a in soup.find_all("a", href=re.compile(r"^https?://(?!.*scholarships\.com)(?!.*facebook)(?!.*twitter)(?!.*linkedin)", re.I)):
            href = a.get("href", "")
            if href.startswith("http") and len(href) > 15:
                application_url = href
                break
    
    org = "Unknown"
    # Try to extract from URL slug
    slug = re.search(r"/scholarships/([^/]+)", url)
    if slug:
        org = slug.group(1).replace("-", " ").title()
    
    return {
        "scholarship_name": name[:180],
        "organization": org[:120],
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "application_url": application_url,
        "website": url,
        "description": text[:300],
        "category": tag_category(name, org, text),
        "education_level": tag_level(name, text),
        "state_restriction": guess_state(text),
        "source": "scholarshipscom_sitemap",
        "source_id": f"sc_{re.search(r'/scholarships/([^/]+)', url).group(1) if re.search(r'/scholarships/([^/]+)', url) else 'unknown'}",
    }

def extract_boldorg(html: str, url: str) -> Optional[Dict]:
    """Extract from bold.org individual scholarship pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    # Skip listing pages
    if any(x in url for x in ["/by-", "/by-state", "/by-major", "/by-year", "/by-type", "/by-demographics"]):
        return None
    
    h1 = soup.find("h1")
    name = h1.get_text(strip=True) if h1 else ""
    
    if not name or not re.search(r"scholarship|bursary|fellowship|grant|award", name + " " + text, re.I):
        return None
    
    # Extract amount
    amount_min = None
    amount_max = None
    amount_display = "Varies"
    
    amt_match = re.search(r"\$([0-9,]+)", name + " " + text)
    if amt_match:
        amount_min = int(amt_match.group(1).replace(",", ""))
        amount_display = f"${amount_min:,}"
    
    # Extract deadline
    deadline = ""
    dl_match = re.search(r"(?:Deadline|Due|Apply By|Closing)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
    if dl_match:
        deadline = dl_match.group(1).strip()
    
    # Extract application URL
    application_url = None
    for a in soup.find_all("a", href=re.compile(r"^https?://", re.I)):
        href = a.get("href", "")
        a_text = a.get_text(strip=True).lower()
        if any(x in a_text for x in ["apply", "application", "submit"]):
            if "bold.org" not in href:
                application_url = href
                break
    
    if not application_url:
        application_url = url
    
    org = "Bold.org"
    return {
        "scholarship_name": name[:180],
        "organization": org[:120],
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "application_url": application_url,
        "website": url,
        "description": text[:300],
        "category": tag_category(name, org, text),
        "education_level": tag_level(name, text),
        "state_restriction": guess_state(text),
        "source": "boldorg_sitemap",
        "source_id": f"bold_{url.split('/')[-1] or 'unknown'}",
    }

def extract_page(url: str, html: str) -> Optional[Dict]:
    """Route to the correct extractor based on domain."""
    if "studentscholarships.org" in url:
        return extract_studentscholarships(html, url)
    elif "scholarships.com" in url:
        return extract_scholarshipscom(html, url)
    elif "bold.org" in url:
        return extract_boldorg(html, url)
    return None

def fetch_and_parse(url: str) -> Optional[Dict]:
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        if r.status_code >= 400:
            return None
        return extract_page(url, r.text)
    except Exception as e:
        print(f"  fetch error {url}: {e}")
        return None

# ------------------------------------------------------------------ #
# Stats
# ------------------------------------------------------------------ #
def stats() -> Dict:
    out = {}
    for db_path in DB_PATHS:
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
    parser = argparse.ArgumentParser(description="Sitemap-based scholarship discovery")
    parser.add_argument("--limit", type=int, default=BATCH_LIMIT_DEFAULT, help="Target new scholarships")
    parser.add_argument("--max-fetch", type=int, default=600, help="Max pages to fetch")
    parser.add_argument("--input", help="Optional JSON file of scholarships to insert")
    args = parser.parse_args()

    before = stats()
    print("Before:", before)

    scholarships: List[Dict] = []
    
    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for i, item in enumerate(raw[: args.limit], start=1):
            item.setdefault("source", "json_input")
            item.setdefault("source_id", f"json_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{i:03d}")
            item.setdefault("status", "active")
            scholarships.append(item)
    else:
        urls = get_scholarship_urls()
        random.shuffle(urls)
        urls = urls[: args.max_fetch]
        print(f"Fetching {len(urls)} pages with {MAX_WORKERS} workers...")
        
        fetched = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(fetch_and_parse, u): u for u in urls}
            for future in as_completed(future_to_url):
                result = future.result()
                fetched += 1
                if fetched % 50 == 0:
                    print(f"  fetched {fetched}/{len(urls)}...")
                if result:
                    scholarships.append(result)
        
        print(f"Parsed {len(scholarships)} candidates from {fetched} pages")

    if not scholarships:
        print("No scholarships discovered in this run.")
        return

    # Dedup and insert
    added_total = 0
    skipped_dup = 0
    skipped_link = 0
    errors = []
    
    for s in scholarships[: args.limit * 2]:
        if not deadline_is_current(s.get("deadline")):
            continue
        for db_path in DB_PATHS:
            conn = get_db_connection(db_path)
            try:
                if is_dup(conn, s):
                    skipped_dup += 1
                    continue
                
                app_url = s.get("application_url")
                if app_url:
                    v = verify_link(app_url)
                    if not v["ok"]:
                        skipped_link += 1
                        s["status"] = "inactive"
                        s["link_notes"] = v.get("reason", "link_failed")
                        if v.get("final_url"):
                            s["application_url"] = v["final_url"]
                            s["website"] = v["final_url"]
                        continue
                
                if is_dup(conn, s):
                    skipped_dup += 1
                    continue
                
                add_scholarship(conn, s)
                added_total += 1
                if added_total >= args.limit:
                    break
            except Exception as e:
                errors.append(str(e))
            finally:
                conn.close()
        
        if added_total >= args.limit:
            break

    after = stats()
    result = {
        "added": added_total,
        "skipped_dup": skipped_dup,
        "skipped_link": skipped_link,
        "errors": errors,
    }
    
    print("Result:", result)
    print("After:", after)
    print(f"DB change: {before} -> {after}")
    
    return result

if __name__ == "__main__":
    main()
