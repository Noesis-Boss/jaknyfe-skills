#!/usr/bin/env python3
"""
Mass scholarship discovery: scrape multiple aggregator and institutional sites,
extract individual scholarships, verify application links, deduplicate, and
write a JSON file for insert via discover.py --input.
"""
import os, sys, json, re, sqlite3, hashlib, time, random, argparse
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
]
OUTPUT_DEFAULT = os.path.join(SCRIPT_DIR, "mass_discover_output.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0; +https://jaknyfe.zo.space)"}
REQUEST_TIMEOUT = 20
PARSE_BUDGET_SEC = 10
JITTER = (0.3, 0.8)

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

def guess_country(url: str, text: str = "") -> str:
    combined = (url + " " + text).lower()
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "university of toronto", "mcgill", "ubc"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "oxford", "cambridge", "imperial", "edinburgh"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "university of sydney", "university of melbourne"]):
        return "Australia"
    if any(t in combined for t in ["new zealand", "studylink", "nz gov"]):
        return "New Zealand"
    if any(t in combined for t in ["europa.eu", "erasmus", "daad", "campusfrance", "studynetherlands", "ethz"]):
        return "EU"
    if any(t in combined for t in [".edu", ".gov", "university", "college"]):
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
        "south carolina": "SC", "oklahoma": "OK", "kansas": "KS", "iowa": "IA",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def tag_category(name: str, org: str, raw_text: str, url: str = "") -> str:
    text = f"{name} {org} {raw_text} {url}".lower()
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", "Medicine"),
        (r"\blaw\b|\blegal\b|\battorney\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", "Arts"),
        (r"\btrade\b|\btechnical\b|\bvocational\b|\bwelding\b|\bautomotive\b", "Trade School"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bveteran\b|\bmilitary\b|\barmed forces\b", "Military/Veteran"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b|\bph\.?d\b|\bdoctorate\b", "Graduate"),
        (r"\bcommunity\b|\bvolunteer\b|\bservice\b", "Community"),
        (r"\bsocial science\b|\bpolitical\b|\bsociology\b|\bpsychology\b", "Social Science"),
    ]:
        if re.search(pat, text):
            return cat
    return "Academic"

def tag_level(name: str, raw_text: str) -> str:
    text = f"{name} {raw_text}".lower()
    for pat, lvl in [
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
        (r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", "Professional"),
        (r"\bhigh school\b|\bsecondary\b", "High School"),
    ]:
        if re.search(pat, text):
            return lvl
    return "Undergraduate"

# ------------------------------------------------------------------ #
# Site-specific extractors
# ------------------------------------------------------------------ #
def extract_from_studentscholarships_page(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=re.compile(r"/scholarship/\d+/")):
        href = urljoin(base_url, a.get("href", ""))
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        # Find parent container for more context
        parent = a.find_parent(["div", "li", "tr", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "StudentScholarships.org",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

def extract_from_bold_listing(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    # Bold.org often uses cards with links
    for a in soup.find_all("a", href=re.compile(r"/scholarships/[^/]+/?$")):
        href = urljoin(base_url, a.get("href", ""))
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "Bold.org",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

def extract_from_accessscholarships(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=re.compile(r"/(scholarship|grant|award)")):
        href = urljoin(base_url, a.get("href", ""))
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "AccessScholarships.com",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

def extract_from_appily(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=re.compile(r"/scholarship/")):
        href = urljoin(base_url, a.get("href", ""))
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "Appily",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

def extract_from_internationalscholarships(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=re.compile(r"/scholarship|/grant|/award")):
        href = urljoin(base_url, a.get("href", ""))
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "InternationalScholarships.com",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

def extract_from_studyportals(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=re.compile(r"/scholarship/")):
        href = urljoin(base_url, a.get("href", ""))
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "StudyPortals",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

# ------------------------------------------------------------------ #
# Generic listing parser
# ------------------------------------------------------------------ #
def extract_generic_listing(html: str, base_url: str, org_name: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    # Look for links that look like scholarships
    patterns = [
        re.compile(r"/scholarship/", re.I),
        re.compile(r"/grant/", re.I),
        re.compile(r"/fellowship/", re.I),
        re.compile(r"/award/", re.I),
        re.compile(r"/financial-aid/", re.I),
    ]
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a.get("href", ""))
        if not any(p.search(href) for p in patterns):
            continue
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        if not re.search(r"scholarship|bursary|fellowship|grant|award|financial aid", text, re.I):
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article", "tr"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": org_name,
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

# ------------------------------------------------------------------ #
# Scholarship page detail extraction
# ------------------------------------------------------------------ #
def extract_detail_from_page(html: str, url: str) -> Dict:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    title = soup.title.string.strip() if soup.title else ""
    combined = f"{title} {text}"

    amount_min, amount_max, amount_display = None, None, "Varies"
    amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", combined.replace(",", ""))
    if amounts:
        nums = [int(a) for a in amounts if 10 < int(a) < 500000]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            amount_display = parse_amount_display(amount_min, amount_max)

    deadline = ""
    dl_match = re.search(
        r"(?:deadline|due date|closing date|apply by|applications due)[:\s]+"
        r"([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})",
        combined, re.I,
    )
    if dl_match:
        deadline = dl_match.group(1)

    org = ""
    org_m = re.search(r"(?:offered by|provided by|sponsored by|from)\s+([A-Z][A-Za-z\s&]+?)(?:\s*[\.,]|$)", combined)
    if org_m:
        org = org_m.group(1).strip()[:100]
    if not org:
        domain = re.search(r"https?://(?:www\.)?([^/]+)", url)
        if domain:
            org = domain.group(1).split(".")[0].replace("-", " ").title()

    return {
        "scholarship_name": title[:180] if title else "",
        "organization": org[:100] if org else "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "raw_text": combined[:2000],
    }

# ------------------------------------------------------------------ #
# Fetch with retry
# ------------------------------------------------------------------ #
def fetch(url: str, timeout: int = REQUEST_TIMEOUT) -> Optional[str]:
    for attempt in range(2):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                return r.text
            if r.status_code in (403, 404, 410):
                return None
        except requests.RequestException:
            pass
        time.sleep(1)
    return None

# ------------------------------------------------------------------ #
# Main
# ------------------------------------------------------------------ #
def main():
    parser = argparse.ArgumentParser(description="Mass scholarship discovery")
    parser.add_argument("--limit", type=int, default=200, help="Target new scholarships")
    parser.add_argument("--output", default=OUTPUT_DEFAULT, help="Output JSON path")
    parser.add_argument("--verify", action="store_true", help="Verify links before output")
    args = parser.parse_args()

    sources = [
        ("studentscholarships_org", "https://studentscholarships.org/scholarships/", extract_from_studentscholarships_page),
        ("bold_org", "https://bold.org/scholarships/", extract_from_bold_listing),
        ("accessscholarships_com", "https://accessscholarships.com", extract_from_accessscholarships),
        ("appily_com", "https://appily.com/scholarships", extract_from_appily),
        ("internationalscholarships_com", "https://www.internationalscholarships.com/", extract_from_internationalscholarships),
        ("studyportals_com", "https://www.studyportals.com/scholarships", extract_from_studyportals),
        ("scholarships360_org", "https://scholarships360.org", lambda h, b: extract_generic_listing(h, b, "Scholarships360")),
        ("cappex_com", "https://www.cappex.com/scholarships", lambda h, b: extract_generic_listing(h, b, "Cappex")),
    ]

    all_candidates: List[Dict] = []
    seen_urls = set()

    for src_id, url, extractor in sources:
        print(f"\n=== Fetching {src_id}: {url}")
        html = fetch(url)
        if not html:
            print(f"  -> failed to fetch")
            continue
        print(f"  -> fetched {len(html)} bytes")
        start = time.time()
        candidates = extractor(html, url)
        parse_time = time.time() - start
        print(f"  -> parsed {len(candidates)} candidates in {parse_time:.1f}s")
        all_candidates.extend(candidates)
        time.sleep(random.uniform(*JITTER))

    # Dedup by URL at candidate level
    unique = []
    for c in all_candidates:
        app_url = c.get("application_url", "")
        if app_url and app_url not in seen_urls:
            seen_urls.add(app_url)
            unique.append(c)
    print(f"\nTotal unique candidates: {len(unique)}")

    # Optionally verify links
    verified = []
    if args.verify:
        print("Verifying links...")
        for c in unique[: args.limit * 2]:
            url = c.get("application_url")
            if not url:
                continue
            v = verify_link(url)
            if v.get("ok"):
                c["application_url"] = v.get("final_url", url)
                c["website"] = v.get("final_url", url)
                verified.append(c)
            else:
                c["link_notes"] = v.get("reason", "link_failed")
                # Still include but mark inactive
                c["status"] = "inactive"
                verified.append(c)
            time.sleep(0.2)
    else:
        verified = unique

    # Limit
    verified = verified[: args.limit * 2]

    # Build output records
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    output = []
    for idx, c in enumerate(verified, start=1):
        raw_text = c.get("raw_text", "")
        detail = extract_detail_from_page(raw_text, c.get("application_url", "")) if raw_text else {}
        record = {
            "source": f"mass_discover_{src_id}",
            "source_id": f"mass_{src_id}_{today}_{idx:03d}",
            "scholarship_name": c.get("scholarship_name") or detail.get("scholarship_name", ""),
            "organization": c.get("organization") or detail.get("organization", ""),
            "organization_type": "",
            "description": "",
            "eligibility": "",
            "amount_min": detail.get("amount_min"),
            "amount_max": detail.get("amount_max"),
            "amount_display": detail.get("amount_display", c.get("amount_display", "Varies")),
            "deadline": c.get("deadline") or detail.get("deadline", ""),
            "application_url": c.get("application_url"),
            "form_url": None,
            "email": None,
            "phone": None,
            "address": "",
            "website": c.get("application_url"),
            "category": tag_category(c.get("scholarship_name", ""), c.get("organization", ""), raw_text, c.get("application_url", "")),
            "education_level": tag_level(c.get("scholarship_name", ""), raw_text),
            "field_of_study": None,
            "state_restriction": guess_state(raw_text),
            "gpa_min": None,
            "citizenship": None,
            "ethnicity": None,
            "gender": None,
            "military_affiliation": None,
            "name_hash": name_hash(c.get("scholarship_name", ""), c.get("organization", "")),
            "link_notes": c.get("link_notes", ""),
            "status": c.get("status", "active"),
        }
        output.append(record)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {len(output)} records to {args.output}")

if __name__ == "__main__":
    main()
