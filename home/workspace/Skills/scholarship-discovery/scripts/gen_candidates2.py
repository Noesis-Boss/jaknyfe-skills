#!/usr/bin/env python3
"""
Generate clean scholarship candidates from targeted web searches.
Reads saved web_search JSON files + does live searches via requests+BeautifulSoup,
extracts individual scholarship pages, and compiles them into the JSON format
expected by discover.py --input.
"""
import os, sys, json, re, time, random
from datetime import datetime, timezone
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup

SEARCH_DIR = "/home/.z/workspaces/con_Xg1QFfyDCEtjEY8u/read_webpage"
DB_PATHS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/3.0)"}
REQUEST_TIMEOUT = 20
JITTER = (0.2, 0.6)
TODAY = datetime.now(timezone.utc).strftime("%Y%m%d")

# ------------------------------------------------------------------
# Link verification for dedup (discoverscans both DBs)
# ------------------------------------------------------------------
import sqlite3, hashlib

def normalize(text):
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def name_hash(name, org):
    raw = normalize(name) + "||" + normalize(org)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def clean_num(val):
    if not val:
        return None
    m = re.search(r"[\$\,\€\£]?\s*([0-9,]+)", str(val).replace(",", ""))
    return int(m.group(1)) if m else None

def is_dup(name, org, amount_min, amount_max):
    # Quick in-memory/db dedup
    nh = name_hash(name, org)
    for db in DB_PATHS:
        if not os.path.exists(db):
            continue
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, amount_min, amount_max FROM scholarships WHERE name_hash = ? OR (normalized_name = ? AND LOWER(organization) = ?)",
            (nh, normalize(name), normalize(org))
        )
        rows = cur.fetchall()
        if not rows:
            # Try name-only fuzzy
            cur.execute(
                "SELECT id, amount_min, amount_max FROM scholarships WHERE normalized_name = ?",
                (normalize(name),)
            )
            rows = cur.fetchall()
        for row in rows:
            existing_min = row[1] or 0
            existing_max = row[2] or existing_min or 0
            new_min = amount_min or 0
            new_max = amount_max or new_min or 0
            if existing_min > 0 and new_min > 0:
                ratio = min(new_min, existing_min) / max(new_min, existing_min)
                if ratio > 0.9:
                    conn.close()
                    return True
        conn.close()
    return False

# ------------------------------------------------------------------
# Search helpers
# ------------------------------------------------------------------
def duckduckgo_search(query):
    query_url = "https://html.duckduckgo.com/html/?q=" + quote(query)
    results = []
    try:
        r = requests.get(query_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(r.text, "lxml")
        for res in soup.select(".result"):
            title_tag = res.select_one(".result__title a")
            snippet_tag = res.select_one(".result__snippet")
            if title_tag and title_tag.get("href"):
                url = title_tag["href"]
                title = title_tag.get_text(strip=True)
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                # DDG wraps URLs: //duckduckgo.com/l/?uddg=...&...
                if "uddg=" in url:
                    url = url.split("uddg=")[1].split("&")[0]
                results.append({"title": title, "url": url, "text": snippet})
    except Exception as e:
        print(f"search error for {query!r}: {e}", file=sys.stderr)
    return results

def is_listing_page(text, title):
    listing_indicators = [
        "list of scholarships", "browse scholarships", "find scholarships",
        "top scholarships", "best scholarships", "scholarship search",
        "scholarship directory", "scholarship listings", "scholarships for ",
        "how to find", "guide to scholarships", "tips for scholarships"
    ]
    comb = (title + " " + text).lower()
    if any(ind in comb for ind in listing_indicators):
        return True
    # Fastweb/College Board article pages
    if any(d in comb for d in ["fastweb.com/college-scholarships/articles/",
                               "how2winscholarships.com",
                               "scholarships360.org/scholarships/scholarships-for-fall",
                               "accessscholarships.com/blog"]):
        return True
    return False

def looks_like_scholarship_page(title, url, text):
    # Must mention scholarship/award/fellowship/grant
    if not re.search(r"scholarship|bursary|fellowship|grant|award", title + text, re.I):
        return False
    # Should have dollar amount or scholarship amount info
    amt = re.search(r"[\$\,\€\£]\s*([0-9,]+)", title + text)
    has_amount = amt is not None
    # Should have deadline or deadline-like date
    dl = re.search(r"(deadline|closing|due|apply by|ends)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4})", title + text, re.I)
    has_deadline = dl is not None
    # Should not be a listing page
    if is_listing_page(text, title):
        return False
    # Prefer sites with actual scholarship data
    good_domains = [".edu", ".gov", ".ac.uk", ".org", "scholarships360.org/scholarship/",
                    "bold.org/scholarship", "appily.com/scholarship",
                    "jlvcollegecounseling.com/scholarship",
                    "collegescholarships.org/scholarship",
                    "accessscholarships.com/scholarship",
                    "studentscholarships.org/scholarship",
                    "studentaid.gov", "fastweb.com/financial-aid/scholarships",
                    "getintocollege.com"]
    good = any(d in url.lower() for d in good_domains)
    if good or has_amount or has_deadline:
        return True
    # If it has scholarship in title + reasonable length, accept
    if len(text) > 500 and "scholarship" in title.lower():
        return True
    return False

def extract_amount(text):
    amounts = re.findall(r'[\$\,\€\£]\s*([0-9,]+)', text.replace(",", ""))
    amount_min = None
    amount_max = None
    amount_display = "Varies"
    if amounts:
        nums = [int(a) for a in amounts if 100 < int(a) < 1500000]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            if amount_min == amount_max:
                amount_display = f"${amount_min:,}"
            else:
                amount_display = f"${amount_min:,}+" if amount_max is None else f"${amount_min:,} - ${amount_max:,}"
    elif re.search(r"full tuition|full cost|full ride|full attendance", text, re.I):
        amount_display = "Full Cost of Attendance"
        amount_min = 60000
        amount_max = 80000
    elif re.search(r"tuition discount|discount", text, re.I):
        amount_display = "Tuition Discount"
        amount_min = 5000
        amount_max = 20000
    return amount_min, amount_max, amount_display

def extract_deadline(text):
    m = re.search(r"(?:deadline|closing|apply by|due|ends|submitted by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
    if m:
        return m.group(1)
    m = re.search(r"([A-Za-z]+ \d{1,2},? \d{4})", text)
    if m:
        return m.group(1)
    return "2026-12-31"

def extract_org(text, title):
    org_m = re.search(r"(?:offered by|provided by|sponsored by|from the|by the)\s+([A-Z][A-Za-z\s&]+?(?:Foundation|University|College|Institute|Association|Organization|Society|Fund|Program|Lodge|Trust|Corporation|Bank|Company|Center|Group|Scholarship))", text, re.I)
    if org_m:
        return org_m.group(1).strip()
    # Try to extract from URL
    m = re.search(r"https?://(?:www\.)?([^/]+)", title.lower() + " " + text.lower())
    if m:
        return m.group(1).replace("-", " ").title()
    return "Unknown"

def extract_eligibility(text):
    m = re.search(r"(?:eligible|eligibility|criteria|requirements|open to)[:\s]+(.{20,300})", text, re.I | re.S)
    return m.group(1).strip().replace("\n", " ")[:500] if m else ""

def guess_category(text, title=""):
    text = (text + " " + title).lower()
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"), (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", "Medicine"),
        (r"\blaw\b|\blegal\b|\bjuris\b", "Law"), (r"\bbusiness\b|\bentrepreneurship\b|\bcommerce\b|\bmba\b", "Business"),
        (r"\bart\b|\bhumanities\b|\bdesign\b|\bperforming\b", "Arts"),
        (r"\bsocial\b|\bpsychology\b|\beducation\b|\bteaching\b", "Social Science"),
        (r"\btrade\b|\bvocational\b|\btechnical\b|\bhvac\b|\belectrician\b", "Trade School"),
        (r"\bwomen\b|\bfemale\b|\bgirls\b", "Women"), (r"\bgraduate\b|\bmaster\b|\bph\.d\b|\bdoctorate\b", "Graduate"),
        (r"\bdoctoral\b", "PhD"),
        (r"\bhigh school\b|\bsenior\b|\bfreshman\b|\bjunior\b|\bsophomore\b", "Undergraduate"),
        (r"\bcommunity college\b|\bassociate\b", "Associate"),
        (r"\bprofessional\b|\bcareer\b", "Professional"),
        (r"\bmilitary\b|\bveteran\b", "Military/Veteran"),
        (r"\bminority\b|\bdiverse\b|\bunderrepresented\b|\bhbc\b|\blatino\b|\bhispanic\b|\bblack\b|\bindigenous\b", "Community"),
        (r"\bfirst.generation\b", "Undergraduate"),
        (r"\btech\b|\bsoftware\b|\bdeveloper\b|\bit\b", "Tech"),
    ]:
        if re.search(pat, text):
            return cat
    return "Academic"

def guess_education_level(text, title=""):
    text = (text + " " + title).lower()
    if re.search(r"\bph\.?d\b|\bdoctorate\b|\bdoctoral\b|\bpostdoctoral\b", text):
        return "PhD"
    if re.search(r"\bgraduate\b|\bmaster\b|\bm\.s\.\b|\bm\.a\.\b|\bbusiness school\b|\bmba\b", text):
        return "Graduate"
    if re.search(r"\btrade\b|\bvocational\b|\bcertificate\b", text):
        return "Trade School"
    if re.search(r"\bprofessional\b|\bmedical school\b|\blaw school\b|\bdental\b", text):
        return "Professional"
    if re.search(r"\bassociate\b", text):
        return "Associate"
    if re.search(r"\bhigh school\b|\bsenior\b|\bfreshman\b|\bsenior year\b|\bclass of\b", text):
        return "High School"
    if re.search(r"\bgpa\b|\btranscript\b|\bcumulative\b", text):
        return "Undergraduate"
    return "Undergraduate"

def guess_state_country(url, text=""):
    combined = (url + " " + text).lower()
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "university of toronto", "mcgill"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "reading.ac.uk", "oxford.ac.uk"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "university of sydney", "university of melbourne"]):
        return "Australia"
    if any(t in combined for t in ["en.govt.nz", "studylink", "university of auckland", "auckland.ac.nz"]):
        return "NZ"
    if any(t in combined for t in ["europa.eu", "erasmus", "daad", "campusfrance", "studynetherlands", "ethz.ch"]):
        return "EU"
    if any(t in combined for t in [".edu", ".gov", "university", "college", "fastweb.com", "bold.org", "accessscholarships"]):
        return "US"
    return "US"

def guess_state_from_url(url):
    m = re.search(r"/([a-z]{2})/", url.lower())
    if m:
        abbr = m.group(1).upper()
        if abbr in {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"}:
            return abbr
    m = re.search(r"state\s+(?:of\s+)?([a-z]+)", url.lower())
    return None

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    candidates = []
    seen_urls = set()
    seen_names = set()
    seq = 1

    # Load existing web_search results from conversation workspace
    search_files = []
    if os.path.exists(SEARCH_DIR):
        for f in os.listdir(SEARCH_DIR):
            if f.startswith("web_search") and f.endswith(".json"):
                search_files.append(os.path.join(SEARCH_DIR, f))

    print(f"Found {len(search_files)} saved search result files", file=sys.stderr)

    def add_candidate(name, org, url, text="", amount_min=None, amount_max=None, amount_display="Varies",
                      deadline="2026-12-31", category="Academic", education_level="Undergraduate",
                      state_restriction=None, citizenship=None, residency=None,
                      description="", eligibility="", field_of_study=""):
        nonlocal seq
        if not url or url in seen_urls:
            return
        if name in seen_names:
            return
        # Basic quality gate
        if not re.search(r"scholarship|bursary|fellowship|grant|award", name.lower()) and len(name) < 5:
            return
        # Check duplicate with DBs
        if is_dup(name, org, amount_min, amount_max):
            return
        seen_urls.add(url)
        seen_names.add(name)
        cand = {
            "source": "web_search_20260722",
            "source_id": f"websearch{TODAY}_{seq:04d}",
            "scholarship_name": name,
            "organization": org,
            "organization_type": "Other",
            "description": description,
            "eligibility": eligibility,
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
            "field_of_study": field_of_study,
            "state_restriction": state_restriction,
            "gpa_min": None,
            "citizenship": citizenship or "US Citizen",
            "ethnicity": "",
            "gender": "",
            "military_affiliation": "",
            "residency_requirement": residency,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "link_notes": "",
            "status": "active",
            "url_status": "unchecked",
            "last_checked": None,
            "name_hash": name_hash(name, org),
        }
        candidates.append(cand)
        seq += 1

    # ------------------------------------------------------------------
    # Process saved web_search results
    # ------------------------------------------------------------------
    for sf in search_files:
        try:
            with open(sf) as f:
                data = json.load(f)
            for item in data:
                title = item.get("title", "")
                url = item.get("url", "")
                text = item.get("text", "")
                if not title or not url:
                    continue
                if looks_like_scholarship_page(title, url, text):
                    amount_min, amount_max, amount_display = extract_amount(text)
                    deadline = extract_deadline(text)
                    org = extract_org(text, title)
                    category = guess_category(text, title)
                    education_level = guess_education_level(text, title)
                    residency = guess_state_country(url, text)
                    state = guess_state_from_url(url)
                    eligibility = extract_eligibility(text)
                    add_candidate(
                        name=title,
                        org=org,
                        url=url,
                        text=text,
                        amount_min=amount_min,
                        amount_max=amount_max,
                        amount_display=amount_display,
                        deadline=deadline,
                        category=category,
                        education_level=education_level,
                        state_restriction=state,
                        residency=residency if residency != "US" else None,
                        citizenship="US Citizen",
                        eligibility=eligibility,
                    )
        except Exception as e:
            print(f"Error processing {sf}: {e}", file=sys.stderr)

    print(f"After processing saved searches: {len(candidates)} candidates", file=sys.stderr)

    # ------------------------------------------------------------------
    # Live searches for high-yield scholarships
    # ------------------------------------------------------------------
    extra_queries = [
        "2026 scholarship $5000 undergraduate no essay",
        "2026 scholarship $10000 STEM engineering",
        "2026 scholarship women in technology",
        "Masonic scholarship 2026 state",
        "Hispanic scholarship 2026 college",
        "Black scholarship 2026 undergraduate",
        "first generation scholarship 2026",
        "Nursing scholarship 2026 undergraduate",
        "Computer science scholarship 2026",
        "business scholarship 2026 MBA",
        "law school scholarship 2026",
        "community service scholarship 2026",
        "art scholarship 2026 high school",
        "trade school scholarship HVAC 2026",
        "veterans scholarship 2026 college",
        "LGBTQ scholarship 2026",
        "disability scholarship 2026 college",
        "California scholarship 2026 high school",
        "Texas scholarship 2026 college",
        "New York scholarship 2026",
        "Florida scholarship 2026 undergraduate",
        "Illinois scholarship 2026",
        "Arizona scholarship 2026",
        "Georgia scholarship 2026",
        "Michigan scholarship 2026",
        "Washington scholarship 2026",
        "Oregon scholarship 2026",
        "Colorado scholarship 2026",
        "Virginia scholarship 2026",
        "Pennsylvania scholarship 2026",
        "Ohio scholarship 2026",
        "North Carolina scholarship 2026",
        "Canada scholarship 2026 international",
        "UK scholarship 2026 international students",
        "Australia scholarship 2026 international",
        "Germany DAAD scholarship 2026",
        "Netherlands scholarship 2026",
        "Sweden scholarship 2026",
        "Norway scholarship 2026",
        "Finland scholarship 2026",
        "France scholarship 2026",
    ]

    random.seed(42)
    random.shuffle(extra_queries)
    for query in extra_queries:
        if len(candidates) >= 220:
            break
        results = duckduckgo_search(query)
        time.sleep(random.uniform(*JITTER))
        for item in results:
            title = item.get("title", "")
            url = item.get("url", "")
            text = item.get("text", "")
            if not title or not url or not looks_like_scholarship_page(title, url, text):
                continue
            # Skip aggregator listing sites
            if any(d in url.lower() for d in ["fastweb.com/college-scholarships/articles/",
                                              "how2winscholarships.com",
                                              "scholarships360.org/scholarships/scholarships-for-fall",
                                              "accessscholarships.com/blog",
                                              "study.com"]):
                continue
            amount_min, amount_max, amount_display = extract_amount(text)
            deadline = extract_deadline(text)
            org = extract_org(text, title)
            category = guess_category(text, title)
            education_level = guess_education_level(text, title)
            residency = guess_state_country(url, text)
            state = guess_state_from_url(url)
            eligibility = extract_eligibility(text)
            add_candidate(
                name=title,
                org=org,
                url=url,
                text=text,
                amount_min=amount_min,
                amount_max=amount_max,
                amount_display=amount_display,
                deadline=deadline,
                category=category,
                education_level=education_level,
                state_restriction=state,
                residency=residency if residency != "US" else None,
                citizenship="US Citizen" if residency == "US" else "International",
                eligibility=eligibility,
            )
        print(f"  {query}: {len(results)} results -> total candidates {len(candidates)}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Fetch actual pages for richer extraction
    # ------------------------------------------------------------------
    def fetch_page(url):
        try:
            r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            return r.text, r.url
        except Exception:
            return None, None

    # Refresh candidates with page-derived metadata
    enriched = 0
    page_fetch_budget = min(len(candidates), 120)
    page_fetch_interval = max(1, len(candidates) // page_fetch_budget)
    for i, cand in enumerate(candidates):
        if i % page_fetch_interval != 0:
            continue
        html, final_url = fetch_page(cand["application_url"])
        if not html:
            continue
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(separator=" ", strip=True)
        title = soup.title.string.strip() if soup.title else cand["scholarship_name"]
        # Update title
        if title and title != "Find Scholarships":
            cand["scholarship_name"] = title
        # Update org
        cand["organization"] = extract_org(text, title)
        # Update amount
        amin, amax, adisp = extract_amount(text)
        if amin:
            cand["amount_min"] = amin
            cand["amount_max"] = amax
            cand["amount_display"] = adisp
        # Update deadline
        dl = extract_deadline(text)
        if dl:
            cand["deadline"] = dl
        # Update category/level
        cand["category"] = guess_category(text, title)
        cand["education_level"] = guess_education_level(text, title)
        cand["eligibility"] = extract_eligibility(text)
        enriched += 1
        time.sleep(random.uniform(*JITTER))
        # Refresh seen names after enrichment
        seen_names = {c["scholarship_name"] for c in candidates[:i+1]}

    print(f"Enriched {enriched} candidates via page fetch", file=sys.stderr)

    # Final dedup pass
    final = []
    seen_names.clear()
    for cand in candidates:
        if cand["scholarship_name"] in seen_names:
            continue
        if is_dup(cand["scholarship_name"], cand["organization"], cand["amount_min"], cand["amount_max"]):
            continue
        seen_names.add(cand["scholarship_name"])
        final.append(cand)

    print(f"After final dedup: {len(final)} candidates", file=sys.stderr)
    json.dump(final, sys.stdout)
    print(file=sys.stdout)

if __name__ == "__main__":
    main()
