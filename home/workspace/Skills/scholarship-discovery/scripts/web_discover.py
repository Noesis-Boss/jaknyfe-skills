#!/usr/bin/env python3
"""
Web-based scholarship discovery.
Reads web_search JSON results, fetches pages, extracts structured scholarship data,
verifies links, dedups, and inserts into the DB.
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
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "uk gov"]):
        return "UK"
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "canadian"]):
        return "Canada"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "australia"]):
        return "Australia"
    if any(t in combined for t in ["new zealand", "studylink", "nz gov"]):
        return "New Zealand"
    if any(t in combined for t in [".edu", ".gov", "university", "college"]):
        return "USA"
    return "International"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "new jersey": "NJ", "minnesota": "MN", "wisconsin": "WI", "colorado": "CO",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower:
            return abbr
    return None

# ------------------------------------------------------------------
# Extraction from page HTML
# ------------------------------------------------------------------
def extract_amounts(text: str) -> tuple:
    amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", text.replace(",", ""))
    nums = [int(a) for a in amounts if int(a) > 0 and int(a) < 500000]
    if not nums:
        return None, None
    return min(nums), max(nums) if len(nums) > 1 else None

def extract_deadline(text: str) -> str:
    patterns = [
        r"(?:deadline|due|closing|apply by|application deadline)[:\s]+([A-Za-z]+ \d{1,2},? \d{4})",
        r"(?:deadline|due|closing|apply by)[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
        r"(?:deadline|due|closing|apply by)[:\s]+(\d{4}-\d{2}-\d{2})",
        r"([A-Za-z]+ \d{1,2},? \d{4})",  # fallback
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return m.group(1)
    return ""

def categorize(text: str) -> str:
    combined = text.lower()
    if re.search(r"\bmasonic\b|\bfreemason\b|\bscottish rite\b", combined):
        return "Masonic"
    if re.search(r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", combined):
        return "STEM"
    if re.search(r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", combined):
        return "Healthcare"
    if re.search(r"\blaw\b|\blegal\b", combined):
        return "Law"
    if re.search(r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", combined):
        return "Business"
    if re.search(r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", combined):
        return "Arts"
    if re.search(r"\bwomen\b|\bfemale\b", combined):
        return "Women"
    if re.search(r"\bmilitary\b|\bveteran\b|\barmed forces\b", combined):
        return "Military/Veteran"
    if re.search(r"\bhispanic\b|\blatino\b|\blatina\b", combined):
        return "Hispanic"
    if re.search(r"\bblack\b|\bafrican american\b|\bafrican\b", combined):
        return "Black"
    if re.search(r"\blgbtq\b|\blgbt\b|\bqueer\b|\btransgender\b", combined):
        return "LGBTQ"
    if re.search(r"\btrade\b|\btechnical\b|\bvocational\b|\bapprenticeship\b", combined):
        return "Trade School"
    if re.search(r"\bph\.?d\b|\bdoctorate\b|\bpostgraduate\b", combined):
        return "PhD"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b", combined):
        return "Graduate"
    if re.search(r"\bhigh school\b|\bsecondary\b", combined):
        return "High School"
    if re.search(r"\bcommunity college\b|\bassociate\b", combined):
        return "Associate"
    return "Academic"

def guess_education_level(text: str) -> str:
    combined = text.lower()
    if re.search(r"\bhigh school\b|\bsecondary\b", combined):
        return "High School"
    if re.search(r"\bph\.?d\b|\bdoctorate\b", combined):
        return "PhD"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b|\bpostgraduate\b", combined):
        return "Graduate"
    if re.search(r"\btrade\b|\btechnical\b|\bvocational\b|\bapprenticeship\b", combined):
        return "Trade School"
    if re.search(r"\bcommunity college\b|\bassociate\b", combined):
        return "Associate"
    return "Undergraduate"

def guess_citizenship(text: str) -> str:
    combined = text.lower()
    if "international" in combined or "non-us" in combined or "foreign" in combined:
        return "International"
    if "permanent resident" in combined or "green card" in combined:
        return "Permanent Resident"
    if "us citizen" in combined or "u.s. citizen" in combined or "american" in combined:
        return "US Citizen"
    return "None"

def guess_residency(text: str, url: str) -> str:
    combined = (text + " " + url).lower()
    if any(t in combined for t in ["canada", "canadian"]):
        return "Canada"
    if any(t in combined for t in ["uk ", "united kingdom", "british"]):
        return "UK"
    if any(t in combined for t in ["australia", "australian"]):
        return "Australia"
    if any(t in combined for t in ["new zealand", "nz "]):
        return "New Zealand"
    if any(t in combined for t in ["europe", "eu ", "germany", "france", "netherlands", "italy", "spain"]):
        return "EU"
    if any(t in combined for t in [".edu", ".gov", "united states", "usa ", "us "]):
        return "US"
    return "International"

# ------------------------------------------------------------------
# Page parsers for known sites
# ------------------------------------------------------------------
def parse_scholarships360(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    items = []
    # scholarships360 uses cards with h3/a for scholarship names
    for card in soup.select("article, .scholarship-card, .card, h3"):
        title = card.get_text(strip=True)
        link = ""
        a = card.find("a", href=True)
        if a:
            link = a["href"]
            if not link.startswith("http"):
                link = base_url.rstrip("/") + link
        if not title or len(title) < 10:
            continue
        if not re.search(r"scholarship|award|grant|fellowship", title, re.I):
            continue
        text = card.get_text(" ", strip=True)
        amount_min, amount_max = extract_amounts(text)
        items.append({
            "scholarship_name": title[:180],
            "organization": "Scholarships360",
            "description": text[:500],
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": extract_deadline(text),
            "application_url": link or base_url,
            "form_url": link or base_url,
            "website": base_url,
            "category": categorize(text),
            "education_level": guess_education_level(text),
            "state_restriction": guess_state(text) or "",
            "citizenship": guess_citizenship(text),
            "source": "web_discover",
            "source_id": hashlib.md5((title + base_url).encode()).hexdigest()[:12],
        })
    return items

def parse_bold_org(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    items = []
    # bold.org uses scholarship cards
    for card in soup.select("[class*='scholarship'], article, .card"):
        title = ""
        a = card.find("a", href=True)
        if a:
            title = a.get_text(strip=True)
            link = a["href"]
            if not link.startswith("http"):
                link = base_url.rstrip("/") + link
        else:
            h = card.find(["h2", "h3", "h4"])
            if h:
                title = h.get_text(strip=True)
                link = base_url
        if not title or len(title) < 5:
            continue
        text = card.get_text(" ", strip=True)
        amount_min, amount_max = extract_amounts(text)
        items.append({
            "scholarship_name": title[:180],
            "organization": "Bold.org",
            "description": text[:500],
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": extract_deadline(text),
            "application_url": link,
            "form_url": link,
            "website": base_url,
            "category": categorize(text + " " + title),
            "education_level": guess_education_level(text),
            "state_restriction": guess_state(text) or "",
            "citizenship": guess_citizenship(text),
            "source": "web_discover",
            "source_id": hashlib.md5((title + base_url).encode()).hexdigest()[:12],
        })
    return items

def parse_scholarships_com(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    items = []
    for card in soup.select(".scholarship-item, .listing-item, article, tr"):
        title = ""
        a = card.find("a", href=True)
        if a:
            title = a.get_text(strip=True)
            link = a["href"]
            if not link.startswith("http"):
                link = base_url.rstrip("/") + link
        else:
            continue
        if not title or len(title) < 5:
            continue
        text = card.get_text(" ", strip=True)
        amount_min, amount_max = extract_amounts(text)
        items.append({
            "scholarship_name": title[:180],
            "organization": "Scholarships.com",
            "description": text[:500],
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": extract_deadline(text),
            "application_url": link,
            "form_url": link,
            "website": base_url,
            "category": categorize(text + " " + title),
            "education_level": guess_education_level(text),
            "state_restriction": guess_state(text) or "",
            "citizenship": guess_citizenship(text),
            "source": "web_discover",
            "source_id": hashlib.md5((title + base_url).encode()).hexdigest()[:12],
        })
    return items

def parse_generic_listing(html: str, base_url: str) -> List[Dict]:
    """Generic parser: look for h2/h3/h4 with 'scholarship' nearby, or links."""
    soup = BeautifulSoup(html, "lxml")
    items = []
    seen_links = set()
    
    for tag in soup.find_all(["h2", "h3", "h4", "a"]):
        text = tag.get_text(" ", strip=True)
        if not re.search(r"scholarship|bursary|fellowship|grant|award", text, re.I):
            continue
        if len(text) < 10 or len(text) > 200:
            continue
        
        link = base_url
        a = tag if tag.name == "a" else tag.find("a", href=True)
        if a and a.get("href"):
            link = a["href"]
            if not link.startswith("http"):
                link = base_url.rstrip("/") + link
        
        # Avoid duplicates by link
        if link in seen_links:
            continue
        seen_links.add(link)
        
        amount_min, amount_max = extract_amounts(text)
        items.append({
            "scholarship_name": text[:180],
            "organization": base_url.split("//")[-1].split("/")[0],
            "description": text[:500],
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": extract_deadline(text),
            "application_url": link,
            "form_url": link,
            "website": base_url,
            "category": categorize(text),
            "education_level": guess_education_level(text),
            "state_restriction": guess_state(text) or "",
            "citizenship": guess_citizenship(text),
            "source": "web_discover",
            "source_id": hashlib.md5((text + base_url).encode()).hexdigest()[:12],
        })
    return items

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
        # Use GET instead of HEAD for better compatibility
        resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS, stream=True)
        final_url = resp.url
        # Read a small chunk to ensure the connection is valid
        try:
            next(resp.iter_content(chunk_size=1024))
        except StopIteration:
            pass
        resp.close()
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
            scholarship.get("source", "web_discover"),
            scholarship.get("source_id"),
            scholarship.get("scholarship_name"),
            scholarship.get("organization"),
            scholarship.get("organization_type", "Unknown"),
            scholarship.get("description"),
            scholarship.get("eligibility", ""),
            scholarship.get("amount_min"),
            scholarship.get("amount_max"),
            scholarship.get("amount_display"),
            scholarship.get("deadline"),
            scholarship.get("application_url"),
            scholarship.get("form_url"),
            scholarship.get("email", ""),
            scholarship.get("phone", ""),
            scholarship.get("address", ""),
            scholarship.get("website"),
            scholarship.get("category"),
            scholarship.get("education_level"),
            scholarship.get("field_of_study", ""),
            scholarship.get("state_restriction"),
            scholarship.get("gpa_min"),
            scholarship.get("citizenship"),
            scholarship.get("ethnicity", ""),
            scholarship.get("gender", ""),
            scholarship.get("military_affiliation", ""),
            name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", "")),
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            scholarship.get("link_notes", ""),
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
    
    # Extract URLs from search results
    urls_to_fetch = set()
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
                if url and url.startswith("http"):
                    urls_to_fetch.add(url)
        except Exception as e:
            print(f"Error reading {sf}: {e}")
    
    print(f"Found {len(urls_to_fetch)} unique URLs to fetch")
    
    # Also add some specific high-yield URLs
    extra_urls = [
        "https://scholarships360.org/scholarships/computer-science-scholarships",
        "https://bold.org/scholarships/by-demographics/women/women-stem-scholarships",
        "https://bold.org/scholarships/by-demographics/military",
        "https://bold.org/scholarships/by-demographics/lgbtq-scholarships",
        "https://bold.org/scholarships/by-type/veteran-scholarships",
        "https://www.fastweb.com/college-scholarships/articles/college-scholarships-for-military-children-spouses",
        "https://www.scholarships.com/financial-aid/college-scholarships/scholarships-by-type/veteran-scholarships",
        "https://www.scholarships.com/financial-aid/college-scholarships/scholarships-by-type/stem-scholarships",
        "https://scholarshipamerica.org/students/scholarships-for-veterans",
        "https://www.onlinemastersdegrees.org/financial-aid/scholarships/graduate-scholarships-for-veterans",
        "https://www.fastweb.com/college-scholarships/articles/scholarships-for-african-american-students",
        "https://bold.org/scholarships/by-demographics/minorities/black-students-scholarships",
        "https://www.scholarships.com/financial-aid/college-scholarships/scholarships-by-type/minority-scholarships/scholarships-for-black-students",
        "https://www.college-financial-aid-advice.com/hispanic-scholarships.html",
        "https://www.onlinemastersdegrees.org/financial-aid/scholarships/latino-hispanic-students",
        "https://www.bestcolleges.com/resources/lgbtq-scholarships",
        "https://www.stonewallfoundation.org/scholarships",
        "https://mydocumentedlife.org/2025/10/22/2026-point-foundations-flagship-scholarship-open-to-undocumented-lgbtq-students",
        "https://www.opportunitiescorners.com/list-of-government-funded-scholarships",
        "https://www.opportunitiescorners.com/republic-of-estonia-government-scholarships-2026",
        "https://www.opportunitiescorners.com/colombian-government-scholarship-2026",
        "https://www.opportunitiescorners.com/italian-government-maeci-scholarship-2026",
        "https://www.opportunitiescorners.com/malaysia-mtcp-scholarship-2026",
        "https://www.opportunitiescorners.com/chula-link-scholarship-2026",
        "https://www.opportunitiescorners.com/john-thompson-scholarship-2026",
        "https://www.opportunitiescorners.com/romania-arice-scholarship-2026",
        "https://opportunitiescorners.com/british-council-women-in-stem-scholarships",
        "https://www.scholars4dev.com/2467/aga-khan-international-scholarships-for-developing-countrie",
        "https://www.scholars4dev.com/7085/american-university-scholarships-for-international-students",
        "https://www.scholars4dev.com/26025/the-marshall-scholarship-for-americans-to-study-in-the-uk",
        "https://www.scholars4dev.com/6499/scholarships-in-usa-for-international-students",
        "https://www.scholars4dev.com/2735/japan-world-bank-graduate-scholarships-for-development-related-studies",
        "https://www.scholars4dev.com/1494/masters-scholarships-for-non-eu-students-at-university-of-twente",
        "https://www.scholars4dev.com/13921/icsp-tuition-scholarships-at-university-of-oregon-usa",
        "https://www.scholarshiptab.com/scholarships/kazakhstan-government-scholarship-2026",
        "https://www.scholarshiptab.com/scholarships/toyota-scholarship-program-2026",
        "https://www.scholarshiptab.com/scholarships/excelsior-scholarship-program-2026",
        "https://www.scholarshiptab.com/scholarships/chengdu-government-scholarship-2026",
        "https://www.scholarshiptab.com/scholarships/government-of-indonesia-knb-scholarship-2026",
        "https://www.scholarshiptab.com/scholarships/uc-berkeley-2026-regents-and-chancellor-s-scholarship",
        "https://www.scholarshiptab.com/scholarships/sbw-berlin-scholarship-2026",
        "https://genevamasoniclodge.org/scholarship-program",
        "https://newjerseygrandlodge.org/2026scholarships",
        "https://www.scholarships.com/scholarships/oakwood-masonic-lodge-1444-scholarship",
        "https://www.afterschoolafrica.com/100403/teesside-university-vice-chancellors-scholarship",
        "https://www.afterschoolafrica.com/114222/nalanda-university-scholarship",
        "https://www.afterschoolafrica.com/119080/meci-scholarship",
        "https://www.afterschoolafrica.com/98208/prince-sultan-university-scholarship",
        "https://www.afterschoolafrica.com/113871/study-in-canada-scholarships-3",
        "https://www.afterschoolafrica.com/117444/abdulkabir-aliu-foundation-aaf-scholarship",
        "https://www.afterschoolafrica.com/95012/university-of-melbourne-graduate-research-scholarships",
        "https://www.afterschoolafrica.com/81575/z-zurich-foundation-scholarship",
        "https://www.afterschoolafrica.com/95443/mandela-rhodes-scholarship-for-africans",
        "https://www.afterschoolafrica.com/93287/datacamp-data-community-scholarship",
        "https://www.opportunitiesforafricans.com/british-council-women-in-stem-scholarships-2026-2027",
        "https://unilag.edu.ng/opportunity-2026-british-council-women-in-stem-scholarship-now-open",
        "https://registryservices.ed.ac.uk/scholarships-and-student-funding/prospective-postgraduates/funding-for-international-students-18",
        "https://www.bath.ac.uk/campaigns/british-council-scholarships-for-women-in-stem",
        "https://www.qmul.ac.uk/scholarships/items/-british-council-women-in-stem-scholarship.html",
        "https://www.durham.ac.uk/study/scholarships/international/british-council-scholarships-for-women-in-stem",
        "https://truescho.com/en/opportunities/university-of-sydney-international-stipend-scholarship-2026",
        "https://scholarshiproar.com/university-of-sydney-international-scholarships",
        "https://globalscholarships.com/scholarships/international-stipend-scholarship",
        "https://deroundtable.com/apply-for-university-of-toronto-lester-b-pearson-2026-fully-funded-scholarship-in-canada",
        "https://takadam.com/opportunity/lester-b-pearson-scholarship-2026-university-of-toronto-canada-fully-funded",
        "https://scholarshiproar.com/lester-b-pearson-international-scholarship-program",
        "https://mina7portal.com/en/opportunity/lester-b-pearson-international-scholarship-2026-at-university-of-toronto",
        "https://brightscholarship.com/university-of-toronto-scholarship-lester-b-pearson-scholarship",
        "https://scholarshipnext.com/university-of-toronto-lester-b-pearson-scholarship-2026-fully-funded",
        "https://www.mastere.tn/en/lester-b-pearson-international-scholarship",
        "https://selibeng.com/lester-b-pearson-international-scholarship-program-2026-for-study-at-the-university-of-toronto-canada",
        "https://www.scholars4dev.com/17963/fincad-women-in-finance-scholarship",
        "https://www.scholars4dev.com/5802/wmf-scholarships-for-developing-country-students",
        "https://www.wemakescholars.com/scholarship/women-in-stem-scholarship-program",
    ]
    for url in extra_urls:
        urls_to_fetch.add(url)
    
    print(f"Total URLs to fetch: {len(urls_to_fetch)}")
    
    # Fetch and parse pages
    all_items = []
    for url in list(urls_to_fetch)[:80]:  # limit to 80 pages for time
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            if resp.status_code != 200:
                continue
            html = resp.text
            base_url = url.split("?")[0].rstrip("/")
            
            # Choose parser
            if "scholarships360.org" in url:
                items = parse_scholarships360(html, base_url)
            elif "bold.org" in url:
                items = parse_bold_org(html, base_url)
            elif "scholarships.com" in url:
                items = parse_scholarships_com(html, base_url)
            else:
                items = parse_generic_listing(html, base_url)
            
            print(f"  {url}: {len(items)} items")
            all_items.extend(items)
            time.sleep(0.2)  # be polite
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
    
    print(f"\nExtracted {len(all_items)} total candidates from pages")
    
    # Dedup within candidates
    seen = set()
    unique = []
    for c in all_items:
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
    errors = []
    
    for c in unique[:limit]:
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
    
    after = stats()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: {len(errors)}")
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
    
    # Save verified list for email report
    with open("/home/workspace/scholarship-discovery/last_verified.json", "w") as f:
        json.dump(verified, f, indent=2)

if __name__ == "__main__":
    main()
