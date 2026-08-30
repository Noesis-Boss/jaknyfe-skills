#!/usr/bin/env python3
"""
Generate fresh scholarship candidates from web search results and pipe to discover.py
"""
import os
import sys
import json
import re
import urllib.parse
import time
import random
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

DB_PATHS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
REQUEST_TIMEOUT = 20
CONV_WORKSPACE = "/home/.z/workspaces/con_Xg1QFfyDCEtjEY8u"

SEARCH_QUERIES = [
    # US - broad
    "undergraduate scholarships 2026 no essay",
    "college scholarships 2026 application deadline",
    "graduate scholarships STEM 2026",
    "minority scholarships 2026 Hispanic Black",
    # State-specific
    "California scholarships 2026 high school seniors",
    "Texas scholarships 2026 college students",
    "New York scholarships 2026",
    "Arizona scholarships 2026",
    # International
    "scholarships international students 2026 Canada",
    "scholarships international students 2026 UK",
    "scholarships international students 2026 Australia",
    "EU scholarships international students 2026",
    # By field
    "engineering scholarships 2026 undergraduate",
    "computer science scholarships 2026",
    "nursing scholarships 2026 undergraduate",
    "women STEM scholarships 2026",
    # Organizations
    "Masonic scholarships 2026",
    "Hispanic scholarship fund 2026",
    "disability scholarships 2026 college",
    # Platforms
    "fastweb scholarships 2026 new",
    "bold.org scholarships 2026",
    "scholarships360 2026",
    "cappex scholarships 2026",
]

def normalize(text):
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def clean_num(val):
    if not val:
        return None
    m = re.search(r"[\$\,\€\£]?\s*([0-9,]+)", str(val).replace(",", ""))
    if m:
        num = int(m.group(1))
        if num > 1000000:
            return None
        return num
    return None

def guess_country(url, text=""):
    combined = (url + " " + text).lower()
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
        return "Australia"
    if any(t in combined for t in [".edu", "university", "college", "fastweb", "bold.org", "accessscholarships"]):
        return "USA"
    if any(t in combined for t in ["erasmus", "daad", "campusfrance", "studynetherlands"]):
        return "EU"
    return "International"

def guess_state(text):
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "tennessee": "TN", "missouri": "MO", "maryland": "MD", "minnesota": "MN",
        "wisconsin": "WI", "alabama": "AL", "utah": "UT", "nevada": "NV",
        "new jersey": "NJ", "connecticut": "CT", "indiana": "IN", "ohio": "OH",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def guess_category(text, url=""):
    combined = (text + " " + url).lower()
    if re.search(r"\bmasonic\b", combined):
        return "Masonic"
    if re.search(r"\bstem\b|\bengineering\b|\bcomputer science\b|\bmath\b|\bscience\b", combined):
        return "STEM"
    if re.search(r"\bmedicine\b|\bnursing\b|\bhealth\b", combined):
        return "Medicine"
    if re.search(r"\blaw\b|\blegal\b", combined):
        return "Law"
    if re.search(r"\bbusiness\b|\bentrepreneur\b|\bMBA\b", combined):
        return "Business"
    if re.search(r"\bart\b|\bhumanities\b|\bfine arts\b|\bmusic\b", combined):
        return "Arts"
    if re.search(r"\btrade\b|\bvocational\b|\btechnical\b|\bcarpenter\b|\belectrician\b", combined):
        return "Trade School"
    if re.search(r"\bwomen\b|\bfemale\b", combined):
        return "Women"
    if re.search(r"\bcommunity\b|\bservice\b", combined):
        return "Community"
    if re.search(r"\bgraduate\b|\bmasters\b|\bph\.d\b", combined):
        return "Academic"
    if re.search(r"\bundergraduate\b|\bfreshman\b|\bsophomore\b", combined):
        return "Undergraduate"
    return "Academic"

def guess_education_level(text, url=""):
    combined = (text + " " + url).lower()
    if re.search(r"\bph\.?d\b|\bdoctorate\b", combined):
        return "PhD"
    if re.search(r"\bgraduate\b|\bmasters\b|\bmba\b|\bprofessional\b", combined):
        return "Graduate"
    if re.search(r"\bhigh school\b|\bfreshman\b|\bsenior\b", combined):
        return "High School"
    if re.search(r"\btrade school\b|\bvocational\b|\bcertificate\b", combined):
        return "Trade School"
    if re.search(r"\bassociate\b", combined):
        return "Associate"
    if re.search(r"\bcollege\b|\buniversity\b|\bundergraduate\b", combined):
        return "Undergraduate"
    return "Undergraduate"

def extract_scholarship_from_text(title, text, url):
    # Skip non-scholarship pages
    if not re.search(r"scholarship|bursary|fellowship|grant|award", text, re.I) and not re.search(r"scholarship|bursary|fellowship|grant|award", title, re.I):
        return None

    # Clean title
    name = title.strip()
    name = re.sub(r"\s*[-|–—]\s*.*$", "", name)
    name = re.sub(r"\s*\|\s*.*$", "", name)
    name = name.strip()
    if len(name) < 5:
        return None

    # Extract amount
    amount_display = "Varies"
    amount_min = None
    amount_max = None
    
    amt_matches = re.findall(r"\$([0-9,]+)", text)
    amounts = []
    for a in amt_matches:
        try:
            n = int(a.replace(",", ""))
            if 100 < n < 500000:
                amounts.append(n)
        except:
            pass
    
    if amounts:
        amount_min = min(amounts)
        amount_max = max(amounts) if len(amounts) > 1 else None
        if amount_min == amount_max:
            amount_display = f"${amount_min:,}"
        else:
            amount_display = f"${amount_min:,} - ${amount_max:,}"
    elif re.search(r"full tuition|full cost of attendance|full ride", text, re.I):
        amount_display = "Full Cost of Attendance"
        amount_min = 50000
        amount_max = 80000

    # Extract deadline
    deadline = ""
    deadline_m = re.search(r"(?:deadline|closing|apply by|due|ends)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
    if not deadline_m:
        deadline_m = re.search(r"([A-Za-z]+ \d{1,2},? \d{4})", text)
    if deadline_m:
        deadline = deadline_m.group(1)

    # Extract organization
    org = ""
    # Try to extract from URL domain
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    parts = domain.split(".")
    if len(parts) >= 2:
        org = parts[-2].replace("-", " ").title()

    # Try to get better org name from text
    org_m = re.search(r"(?:offered by|provided by|sponsored by|by the)\s+([A-Z][A-Za-z\s&]+?(?:Foundation|University|College|Institute|Association|Organization|Society|Fund|Program|Lodge|Trust|Corporation|Bank|Company|Center|Group|Scholarship))", text, re.I | re.S)
    if org_m:
        org = org_m.group(1).strip()

    # Extract eligibility (first 300 chars)
    eligibility = ""
    elig_m = re.search(r"(?:eligible?|requirements|criteria|must be)[:.\s]+(.{30,400})", text, re.I | re.S)
    if elig_m:
        eligibility = elig_m.group(1).strip()[:400]

    # Determine fields
    category = guess_category(text + " " + title, url)
    education_level = guess_education_level(text + " " + title, url)
    state_restriction = guess_state(text + " " + title)
    country = guess_country(url, text)

    return {
        "source": "web_search_20260722",
        "source_id": "",
        "scholarship_name": name,
        "organization": org,
        "organization_type": "",
        "description": text[:1000],
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
        "field_of_study": "",
        "state_restriction": state_restriction or "",
        "gpa_min": None,
        "citizenship": "None",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "name_hash": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "link_notes": "",
        "status": "active",
    }

def search_duckduckgo(query, max_results=20):
    """Use DuckDuckGo HTML search to find scholarships."""
    candidates = []
    try:
        params = {
            "q": query,
            "t": "h_",
            "ia": "web",
        }
        resp = requests.get("https://html.duckduckgo.com/html/", params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(resp.text, "lxml")
        results = soup.select(".result")
        
        for r in results[:max_results]:
            title_tag = r.select_one(".result__title a")
            snippet_tag = r.select_one(".result__snippet")
            if not title_tag or not snippet_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            href = title_tag.get("href", "")
            text = snippet_tag.get_text(strip=True)
            
            # Extract actual URL from DDG redirect
            if "duckduckgo.com" in href:
                m = re.search(r"uddg=([^&]+)", href)
                if m:
                    href = urllib.parse.unquote(m.group(1))
            
            # Skip non-scholarship pages
            if not re.search(r"scholarship|bursary|fellowship|grant|award.*(?:student|college|university)", title + " " + text, re.I):
                continue
            
            candidates.append((title, href, text))
    except Exception as e:
        sys.stderr.write(f"Search error for '{query}': {e}\n")
    return candidates

def main():
    seen_names = set()
    all_scholarships = []
    seq = 0
    
    sys.stderr.write(f"=== Starting candidate generation ===\n")
    
    for query in SEARCH_QUERIES:
        sys.stderr.write(f"Searching: {query}\n")
        results = search_duckduckgo(query, max_results=15)
        sys.stderr.write(f"  -> {len(results)} raw results\n")
        
        for title, url, text in results:
            norm = normalize(title)
            if not norm or norm in seen_names:
                continue
            seen_names.add(norm)
            
            s = extract_scholarship_from_text(title, text, url)
            if s:
                seq += 1
                s["source_id"] = f"websearch_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{seq:04d}"
                all_scholarships.append(s)
        
        time.sleep(random.uniform(0.5, 1.5))
    
    sys.stderr.write(f"=== Generated {len(all_scholarships)} unique candidates ===\n")
    
    # Output JSON array to stdout (for pipe)
    json.dump(all_scholarships, sys.stdout, indent=2, default=str)

if __name__ == "__main__":
    main()
