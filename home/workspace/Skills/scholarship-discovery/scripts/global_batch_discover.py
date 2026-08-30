#!/usr/bin/env python3
"""
Global Batch Scholarship Discovery
Scrapes scholarship listing pages, extracts structured data, verifies links, dedups, and inserts.
"""
import os
import sys
import json
import re
import sqlite3
import hashlib
import time
import random
import urllib.parse
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup

CONV_WORKSPACE = "/home/.z/workspaces/con_ezJjjBZwcPFeBKED/read_webpage"
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0)"}
REQUEST_TIMEOUT = 20
JITTER = (0.2, 0.6)

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
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "university of toronto", "mcgill", "ubc"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "oxford", "cambridge", "imperial", "edinburgh"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "university of sydney", "university of melbourne"]):
        return "Australia"
    if any(t in combined for t in ["europa.eu", "erasmus", "daad", "campusfrance", "studynetherlands", "ethz"]):
        return "EU"
    if any(t in combined for t in [".edu", ".gov", "university", "college", "scholarships.com", "fastweb", "bold.org", "accessscholarships", "scholarships360"]):
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
        "south carolina": "SC", "kentucky": "KY", "louisiana": "LA", "oklahoma": "OK",
        "connecticut": "CT", "iowa": "IA", "kansas": "KS", "arkansas": "AR",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None


def is_dup(conn: sqlite3.Connection, name: str, org: str) -> bool:
    nh = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None


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
            scholarship.get("source", "global_batch"),
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


def categorize(text: str) -> str:
    combined = text.lower()
    if re.search(r"\bmasonic\b", combined):
        return "Masonic"
    if re.search(r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", combined):
        return "STEM"
    if re.search(r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b|\bmedical\b", combined):
        return "Medicine"
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
    if re.search(r"\bcommunity\b|\bvolunteer\b|\bservice\b", combined):
        return "Community"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b|\bph\.?d\b|\bdoctorate\b", combined):
        return "Graduate"
    if re.search(r"\bhigh school\b|\bsecondary\b", combined):
        return "High School"
    return "Academic"


def tag_level(text: str) -> str:
    combined = text.lower()
    if re.search(r"\bph\.?d\b|\bdoctorate\b", combined):
        return "PhD"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b", combined):
        return "Graduate"
    if re.search(r"\btrade\b|\btechnical\b|\bvocational\b", combined):
        return "Trade School"
    if re.search(r"\bassociate\b|\bcommunity college\b", combined):
        return "Associate"
    if re.search(r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", combined):
        return "Professional"
    if re.search(r"\bhigh school\b|\bsecondary\b", combined):
        return "High School"
    return "Undergraduate"


# ------------------------------------------------------------------
# Parsers by site
# ------------------------------------------------------------------
def parse_accessscholarships(html: str, url: str) -> List[Dict]:
    """Parse AccessScholarships blog listing pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    candidates = []
    
    # Split into blocks separated by blank lines or large headers
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        # Look for scholarship names - usually 3+ words ending with Scholarship/Grant/Award
        if re.search(r"\b(scholarship|grant|award|fellowship)\b", line, re.I) and len(line) > 10:
            name = line.strip()
            if len(name) > 200:
                name = name[:200]
            
            # Gather context: next few lines
            context_lines = []
            for j in range(i+1, min(i+6, len(lines))):
                context_lines.append(lines[j])
            context = " ".join(context_lines)
            
            # Extract amount from context
            amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", context.replace(",", ""))
            amount_min = None
            amount_max = None
            if amounts:
                nums = [int(a) for a in amounts if 10 < int(a) < 500000]
                if nums:
                    amount_min = min(nums)
                    amount_max = max(nums) if len(nums) > 1 else None
            
            # Extract deadline from context
            deadline = ""
            dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", context, re.I)
            if dl_m:
                deadline = dl_m.group(1).strip()
            
            # Extract org from name if possible, else use domain
            org = "Access Scholarships"
            name_lower = name.lower()
            if " by " in name_lower:
                parts = name.rsplit(" by ", 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    org = parts[1].strip()
            
            # Skip generic article headers
            skip = ["top", "best", "list of", "how to", "tips", "guide", "introduction", "frequently asked"]
            if any(name_lower.startswith(s) for s in skip):
                i += 1
                continue
            
            candidates.append({
                "scholarship_name": name[:180],
                "organization": org[:100],
                "amount_min": amount_min,
                "amount_max": amount_max,
                "amount_display": parse_amount_display(amount_min, amount_max),
                "deadline": deadline,
                "description": context[:300],
                "application_url": url,
                "website": url,
            })
        i += 1
    
    return candidates


def parse_mefa(html: str, url: str) -> List[Dict]:
    """Parse MEFA scholarship deadline pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    candidates = []
    
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r"\b(scholarship|grant|award|fellowship|contest)\b", line, re.I) and len(line) > 8:
            context = " ".join(lines[i:min(i+5, len(lines))])
            amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", context.replace(",", ""))
            amount_min = None
            amount_max = None
            if amounts:
                nums = [int(a) for a in amounts if 10 < int(a) < 500000]
                if nums:
                    amount_min = min(nums)
                    amount_max = max(nums) if len(nums) > 1 else None
            
            deadline = ""
            dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4})", context, re.I)
            if dl_m:
                deadline = dl_m.group(1).strip()
            
            name = line.strip()
            if len(name) > 180:
                name = name[:180]
            
            candidates.append({
                "scholarship_name": name,
                "organization": "MEFA",
                "amount_min": amount_min,
                "amount_max": amount_max,
                "amount_display": parse_amount_display(amount_min, amount_max),
                "deadline": deadline,
                "application_url": url,
                "website": url,
            })
        i += 1
    return candidates


def parse_sallie(html: str, url: str) -> List[Dict]:
    """Parse Sallie scholarship listing pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    candidates = []
    
    # Look for lines like "Sallie $2,000 No Essay Scholarship"
    pattern = re.compile(r"([A-Za-z][A-Za-z0-9 &'\-\.]+?)\s*\$([0-9,]+)\s*(No Essay)?\s*Scholarship", re.I)
    for m in pattern.finditer(text):
        name = f"{m.group(1).strip()} ${m.group(2).replace(',', '')} {'No Essay ' if m.group(3) else ''}Scholarship"
        amount = int(m.group(2).replace(",", ""))
        candidates.append({
            "scholarship_name": name[:180],
            "organization": m.group(1).strip(),
            "amount_min": amount,
            "amount_max": amount,
            "amount_display": f"${amount:,}",
            "deadline": "",
            "application_url": url,
            "website": url,
        })
    return candidates


def parse_scholarships360(html: str, url: str) -> List[Dict]:
    """Parse Scholarships360 listing pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    candidates = []
    
    # Look for amount + scholarship name patterns
    pattern = re.compile(r"\$([0-9,]+).*?(?:Scholarship|Grant|Award)", re.I)
    for m in pattern.finditer(text):
        context_start = max(0, m.start() - 100)
        context_end = min(len(text), m.end() + 100)
        context = text[context_start:context_end]
        
        amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", context.replace(",", ""))
        amount_min = None
        amount_max = None
        if amounts:
            nums = [int(a) for a in amounts if 10 < int(a) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
        
        # Try to extract name
        name_m = re.search(r"([A-Za-z][A-Za-z0-9 &'\-\.]{10,}?)\s*\$", context)
        name = name_m.group(1).strip() if name_m else "Scholarship"
        if len(name) > 180:
            name = name[:180]
        
        candidates.append({
            "scholarship_name": name,
            "organization": "Scholarships360",
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": "",
            "application_url": url,
            "website": url,
        })
    return candidates


def parse_generic_listing(html: str, url: str, domain: str) -> List[Dict]:
    """Generic parser for unknown listing pages."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    candidates = []
    
    # Look for lines with scholarship keywords and amounts
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines:
        if re.search(r"\b(scholarship|grant|award|fellowship)\b", line, re.I) and len(line) > 10:
            amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", line.replace(",", ""))
            amount_min = None
            amount_max = None
            if amounts:
                nums = [int(a) for a in amounts if 10 < int(a) < 500000]
                if nums:
                    amount_min = min(nums)
                    amount_max = max(nums) if len(nums) > 1 else None
            
            name = line.strip()
            if len(name) > 180:
                name = name[:180]
            
            # Skip very short or generic headers
            if len(name) < 8:
                continue
            skip = ["top", "best", "list of", "how to", "tips", "guide", "introduction", "frequently asked"]
            if any(name.lower().startswith(s) for s in skip):
                continue
            
            candidates.append({
                "scholarship_name": name,
                "organization": domain,
                "amount_min": amount_min,
                "amount_max": amount_max,
                "amount_display": parse_amount_display(amount_min, amount_max),
                "deadline": "",
                "application_url": url,
                "website": url,
            })
    return candidates


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def load_saved_pages() -> List[Tuple[str, str]]:
    """Load all saved HTML files from conversation workspace."""
    pages = []
    if not os.path.isdir(CONV_WORKSPACE):
        return pages
    for fname in sorted(os.listdir(CONV_WORKSPACE)):
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(CONV_WORKSPACE, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
            # Reconstruct URL from filename
            url = "https://" + fname.replace("~~2f", "/").replace("~~", "%")
            pages.append((url, html))
        except Exception as e:
            print(f"Error reading {fname}: {e}")
    return pages


def fetch_additional_pages() -> List[Tuple[str, str]]:
    """Fetch additional high-yield scholarship listing pages."""
    pages = []
    urls = [
        "https://accessscholarships.com/blog/scholarships-for-college-students/",
        "https://accessscholarships.com/blog/scholarships-for-graduate-students/",
        "https://accessscholarships.com/blog/scholarships-for-community-college-students/",
        "https://accessscholarships.com/blog/weird-scholarships/",
        "https://accessscholarships.com/blog/scholarships-for-grad-school/",
        "https://accessscholarships.com/blog/scholarships-for-law-school/",
        "https://accessscholarships.com/blog/scholarships-for-medical-school/",
        "https://www.sallie.com/resources/scholarships/",
        "https://www.mefa.org/resources/scholarships",
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                pages.append((url, r.text))
            time.sleep(random.uniform(*JITTER))
        except Exception as e:
            print(f"Fetch error {url}: {e}")
    return pages


def main():
    limit = 200
    
    # Load saved pages
    saved_pages = load_saved_pages()
    print(f"Loaded {len(saved_pages)} saved pages")
    
    # Fetch additional pages
    additional = fetch_additional_pages()
    print(f"Fetched {len(additional)} additional pages")
    
    all_pages = saved_pages + additional
    all_candidates = []
    
    for url, html in all_pages:
        domain = urllib.parse.urlparse(url).netloc.lower()
        
        if "accessscholarships.com" in domain:
            cands = parse_accessscholarships(html, url)
        elif "mefa.org" in domain:
            cands = parse_mefa(html, url)
        elif "sallie.com" in domain:
            cands = parse_sallie(html, url)
        elif "scholarships360.org" in domain:
            cands = parse_scholarships360(html, url)
        else:
            cands = parse_generic_listing(html, url, domain)
        
        # Tag metadata
        raw_text = html[:5000]
        country = guess_country(url, raw_text)
        state = guess_state(raw_text)
        
        for c in cands:
            c["source"] = f"listing_{domain.replace('.', '_')}"
            c["source_id"] = hashlib.md5(f"{c['scholarship_name']}{url}".encode()).hexdigest()[:12]
            c["category"] = categorize(c.get("description", "") + " " + c.get("scholarship_name", ""))
            c["education_level"] = tag_level(c.get("description", "") + " " + c.get("scholarship_name", ""))
            c["state_restriction"] = state or ""
            c["citizenship"] = "US Citizen" if country == "USA" else ("None" if country == "International" else country)
            c["organization_type"] = ""
            c["eligibility"] = ""
            c["form_url"] = c.get("application_url")
            c["email"] = ""
            c["phone"] = ""
            c["address"] = ""
            c["field_of_study"] = ""
            c["gpa_min"] = None
            c["ethnicity"] = ""
            c["gender"] = ""
            c["military_affiliation"] = ""
            c["link_notes"] = ""
            all_candidates.append(c)
    
    print(f"Extracted {len(all_candidates)} candidates from pages")
    
    # Dedup within candidates
    seen = set()
    unique = []
    for c in all_candidates:
        key = normalize(c["scholarship_name"]) + "||" + normalize(c["organization"])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    print(f"After internal dedup: {len(unique)} unique candidates")
    
    # Verify and insert
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
    errors = []
    verified = []
    
    for c in unique[:limit]:
        dup = False
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            if is_dup(conn, c["scholarship_name"], c["organization"]):
                dup = True
                conn.close()
                break
            conn.close()
        if dup:
            skipped_dup += 1
            continue
        
        # Verify the application URL
        vr = verify_link(c.get("application_url"))
        if not vr.get("ok"):
            skipped_verify += 1
            continue
        
        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]
        
        for path in DB_PATHS:
            try:
                conn = sqlite3.connect(path)
                add_scholarship(conn, c)
                conn.close()
            except Exception as e:
                errors.append(str(e))
        added += 1
        verified.append(c)
    
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
    
    if errors:
        print(f"\nErrors:")
        for e in errors[:10]:
            print(f"  {e}")
    
    # Save verified list for reporting
    with open("/home/.z/workspaces/con_ezJjjBZwcPFeBKED/verified_batch.json", "w") as f:
        json.dump(verified, f, indent=2, default=str)
    
    return added, after, verified, errors


if __name__ == "__main__":
    main()
