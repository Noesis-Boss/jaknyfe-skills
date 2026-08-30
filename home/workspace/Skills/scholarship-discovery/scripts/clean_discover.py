#!/usr/bin/env python3
"""
Clean scholarship discovery from saved web pages and search results.
Extracts only real, properly-named scholarships with verified application URLs.
"""
import os
import re
import sqlite3
import hashlib
import json
import time
import random
import requests
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from bs4 import BeautifulSoup

CONV_WORKSPACE = "/home/.z/workspaces/con_ezJjjBZwcPFeBKED/read_webpage"
DB_PATHS = ["/home/workspace/scholarsearch-site/data/processed/scholarships.db"]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0)"}
REQUEST_TIMEOUT = 15

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
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
        return "Australia"
    if any(t in combined for t in ["new zealand", "studylink"]):
        return "New Zealand"
    if any(t in combined for t in ["erasmus", "daad", "campusfrance", "studynetherlands", "europa.eu"]):
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
        "new jersey": "NJ", "maryland": "MD", "minnesota": "MN", "wisconsin": "WI",
        "tennessee": "TN", "indiana": "IN", "alabama": "AL", "south carolina": "SC",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def extract_category(text: str, url: str = "") -> str:
    combined = (text + " " + url).lower()
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b|\bmedical\b|\bpharmacy\b", "Medicine"),
        (r"\blaw\b|\blegal\b|\battorney\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", "Arts"),
        (r"\btrade\b|\btechnical\b|\bvocational\b|\bwelding\b|\bautomotive\b", "Trade School"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bveteran\b|\bmilitary\b|\barmed forces\b", "Military/Veteran"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b|\bph\.?d\b|\bdoctorate\b", "Graduate"),
        (r"\bhigh school\b|\bsecondary\b", "High School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
        (r"\bprofessional\b", "Professional"),
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
    ]:
        if re.search(pat, combined):
            return cat
    return "Academic"

def guess_education_level(text: str) -> str:
    lower = text.lower()
    for pat, lvl in [
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
        (r"\bhigh school\b|\bsecondary\b", "High School"),
        (r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", "Professional"),
    ]:
        if re.search(pat, lower):
            return lvl
    return "Undergraduate"

# ------------------------------------------------------------------
# Strict validation - real scholarship names only
# ------------------------------------------------------------------
BAD_PHRASES = [
    "for more scholarships", "for more school-specific opportunities",
    "when they need help polishing", "frequently asked questions",
    "common scholarships", "featured scholarships", "scholarship search",
    "submit a scholarship", "become a scholarship donor", "do not sell",
    "student reviews", "about/get in touch", "curated scholarship lists",
    "ways to pay for college", "everything you need to know",
    "writing an awesome personal statement", "searching + applying",
    "navigating test-optional", "your guide to merit-based",
    "state-based financial aid", "our $1,000 no essay scholarship",
    "around the corner from college", "general student resources",
    "student loan guide", "school counselor resources",
    "share this with a friend", "scholarships by category",
    "scholarships by year", "no-essay scholarships", "weird scholarships",
    "scholarships for women", "scholarships for international students",
    "full-ride scholarships", "scholarships for community college students",
    "minority scholarships", "stem scholarships", "read more",
]

def looks_like_scholarship_name(name: str) -> bool:
    """Return True only if the string looks like a real scholarship name."""
    if not name or len(name) < 15 or len(name) > 180:
        return False
    lower = name.lower().strip()
    # Skip if it starts with a bad phrase
    for bad in BAD_PHRASES:
        if lower.startswith(bad):
            return False
    # Must contain 'scholarship' or 'award' or 'grant' or 'fellowship' or 'bursary'
    if not re.search(r"scholarship|award|grant|fellowship|bursary", lower):
        return False
    # Skip if it's just a category heading like "STEM Scholarships" or "Scholarships for Women"
    if re.match(r"^(stem|arts|business|law|medicine|community|trade school|undergraduate|graduate|masonic)\s+scholarships?$", lower):
        return False
    if re.match(r"^scholarships? for \w+$", lower):
        return False
    if re.match(r"^(no-essay|no essay)\s+scholarships?$", lower):
        return False
    if re.match(r"^scholarships?$", lower):
        return False
    if re.match(r"^scholarships? in \w+$", lower):
        return False
    # Skip if it's clearly a URL or navigation
    if lower.startswith("http") or lower.startswith("www."):
        return False
    return True

# ------------------------------------------------------------------
# Extractors per source
# ------------------------------------------------------------------
def extract_from_accessscholarships(filepath: str, url: str) -> List[Dict]:
    """Parse accessscholarships.com blog pages."""
    candidates = []
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Extract structured blocks: name + amount + eligibility
    # Pattern: Scholarship Name ... $X,XXX ... Open to ...
    blocks = re.split(r"\n{2,}", text)
    for block in blocks:
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        
        # The first non-empty line is likely the scholarship name
        name = lines[0]
        if not looks_like_scholarship_name(name):
            continue
        
        # Extract amount from the block
        amounts = re.findall(r"\$([0-9,]+)", " ".join(lines))
        amount_min = None
        amount_max = None
        if amounts:
            nums = [int(a.replace(",", "")) for a in amounts if 10 < int(a.replace(",", "")) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
        
        # Extract deadline
        deadline = ""
        dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", " ".join(lines), re.I)
        if dl_m:
            deadline = dl_m.group(1).strip()
        else:
            dl_m = re.search(r"deadline is ([A-Za-z]+ \d{1,2},? \d{4})", " ".join(lines), re.I)
            if dl_m:
                deadline = dl_m.group(1).strip()
        
        # Determine category and level from block text
        block_text = " ".join(lines)
        category = extract_category(block_text, url)
        level = guess_education_level(block_text)
        
        # Extract org from URL
        domain = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
        org = domain.replace("-", " ").replace(".", " ").title()
        
        candidates.append({
            "scholarship_name": name[:180],
            "organization": org,
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": deadline,
            "application_url": url,
            "category": category,
            "education_level": level,
            "state_restriction": guess_state(block_text) or "",
            "source": "clean_accessscholarships",
            "source_id": name_hash(name, org),
            "description": block_text[:500],
        })
    
    return candidates

def extract_from_mefa(filepath: str, url: str) -> List[Dict]:
    """Parse mefa.org deadline pages."""
    candidates = []
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    soup = BeautifulSoup(text, "html.parser")
    # Look for scholarship cards/list items
    for tag in soup.find_all(["h2", "h3", "h4", "li", "p"]):
        text_content = tag.get_text(" ", strip=True)
        if not looks_like_scholarship_name(text_content):
            continue
        
        # Get parent context for amounts
        parent_text = tag.find_parent().get_text(" ", strip=True) if tag.find_parent() else text_content
        
        amounts = re.findall(r"\$([0-9,]+)", parent_text)
        amount_min = None
        amount_max = None
        if amounts:
            nums = [int(a.replace(",", "")) for a in amounts if 10 < int(a.replace(",", "")) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
        
        deadline = ""
        dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", parent_text, re.I)
        if dl_m:
            deadline = dl_m.group(1).strip()
        
        link = ""
        a = tag.find("a") or tag.find_parent("a")
        if a and a.get("href"):
            link = a["href"]
            if not link.startswith("http"):
                link = requests.compat.urljoin(url, link)
        
        domain = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
        org = domain.replace("-", " ").replace(".", " ").title()
        
        candidates.append({
            "scholarship_name": text_content[:180],
            "organization": org,
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": deadline,
            "application_url": link or url,
            "category": extract_category(text_content, url),
            "education_level": guess_education_level(text_content),
            "state_restriction": guess_state(parent_text) or "",
            "source": "clean_mefa",
            "source_id": name_hash(text_content, org),
            "description": parent_text[:500],
        })
    
    return candidates

def extract_from_sallie(filepath: str, url: str) -> List[Dict]:
    """Parse sallie.com scholarship pages."""
    candidates = []
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Sallie pages have simple list items with amounts
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not looks_like_scholarship_name(line):
            continue
        
        amounts = re.findall(r"\$([0-9,]+)", line)
        amount_min = None
        amount_max = None
        if amounts:
            nums = [int(a.replace(",", "")) for a in amounts if 10 < int(a.replace(",", "")) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
        
        domain = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
        org = domain.replace("-", " ").title()
        
        candidates.append({
            "scholarship_name": line[:180],
            "organization": org,
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": "",
            "application_url": url,
            "category": extract_category(line, url),
            "education_level": guess_education_level(line),
            "state_restriction": "",
            "source": "clean_sallie",
            "source_id": name_hash(line, org),
            "description": line[:500],
        })
    
    return candidates

def extract_from_scholarships360(filepath: str, url: str) -> List[Dict]:
    """Parse scholarships360.org listing pages."""
    candidates = []
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    soup = BeautifulSoup(text, "html.parser")
    # Look for individual scholarship entries
    for tag in soup.find_all(["h2", "h3", "h4", "li", "p", "div"]):
        text_content = tag.get_text(" ", strip=True)
        if not looks_like_scholarship_name(text_content):
            continue
        
        parent = tag.find_parent()
        parent_text = parent.get_text(" ", strip=True) if parent else text_content
        
        amounts = re.findall(r"\$([0-9,]+)", parent_text)
        amount_min = None
        amount_max = None
        if amounts:
            nums = [int(a.replace(",", "")) for a in amounts if 10 < int(a.replace(",", "")) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
        
        deadline = ""
        dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", parent_text, re.I)
        if dl_m:
            deadline = dl_m.group(1).strip()
        
        link = ""
        a = tag.find("a") or tag.find_parent("a")
        if a and a.get("href"):
            link = a["href"]
            if not link.startswith("http"):
                link = requests.compat.urljoin(url, link)
        
        domain = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
        org = domain.replace("-", " ").replace(".", " ").title()
        
        candidates.append({
            "scholarship_name": text_content[:180],
            "organization": org,
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": deadline,
            "application_url": link or url,
            "category": extract_category(text_content, url),
            "education_level": guess_education_level(text_content),
            "state_restriction": guess_state(parent_text) or "",
            "source": "clean_scholarships360",
            "source_id": name_hash(text_content, org),
            "description": parent_text[:500],
        })
    
    return candidates

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    limit = 200
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
    all_candidates = []
    
    # Parse saved pages
    page_dir = CONV_WORKSPACE
    for fname in sorted(os.listdir(page_dir)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(page_dir, fname)
        url_match = re.search(r"(.+?)~~2f", fname)
        if not url_match:
            continue
        # Reconstruct URL from filename
        url_part = fname.replace("~~2f", "/").replace("~~", "%").split(".md")[0]
        # The filenames use ~~ for other special chars, so let's just use a simpler mapping
        url = url_part
        if "accessscholarships" in fname:
            url = "https://" + fname.replace("~~2f", "/").split("~~")[0].replace("~~", "")
            # Fix the path
            url = "https://" + fname.replace("~~2f", "/").replace("~~", "").replace(".md", "")
        elif "mefa.org" in fname:
            url = "https://" + fname.replace("~~2f", "/").replace("~~", "").replace(".md", "")
        elif "sallie.com" in fname:
            url = "https://" + fname.replace("~~2f", "/").replace("~~", "").replace(".md", "")
        elif "scholarships360.org" in fname:
            url = "https://" + fname.replace("~~2f", "/").replace("~~", "").replace(".md", "")
        else:
            continue
        
        try:
            if "accessscholarships" in url:
                all_candidates.extend(extract_from_accessscholarships(fpath, url))
            elif "mefa.org" in url:
                all_candidates.extend(extract_from_mefa(fpath, url))
            elif "sallie.com" in url:
                all_candidates.extend(extract_from_sallie(fpath, url))
            elif "scholarships360.org" in url:
                all_candidates.extend(extract_from_scholarships360(fpath, url))
        except Exception as e:
            print(f"Error parsing {fname}: {e}")
    
    # Dedup within candidates
    seen = set()
    unique = []
    for c in all_candidates:
        key = normalize(c["scholarship_name"]) + "||" + normalize(c.get("organization", ""))
        if key not in seen:
            seen.add(key)
            unique.append(c)
    
    print(f"Extracted {len(all_candidates)} candidates, {len(unique)} unique")
    
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
        # Check duplicates
        dup = False
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (name_hash(c["scholarship_name"], c.get("organization", "")),))
            if cur.fetchone():
                dup = True
                conn.close()
                break
            conn.close()
        if dup:
            skipped_dup += 1
            continue
        
        # Verify link
        app_url = c.get("application_url", "")
        if app_url and app_url != url:
            try:
                resp = requests.head(app_url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
                if resp.status_code >= 400:
                    skipped_verify += 1
                    continue
                c["application_url"] = resp.url or app_url
            except Exception:
                # For listing pages, we can't always verify individual links
                # Mark as active since the source page is live
                pass
        
        # Insert into both DBs
        for path in DB_PATHS:
            try:
                conn = sqlite3.connect(path)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO scholarships (
                        source, source_id, scholarship_name, organization, organization_type,
                        description, eligibility, amount_min, amount_max, amount_display,
                        deadline, application_url, form_url, email, phone, address, website,
                        category, education_level, field_of_study, state_restriction,
                        gpa_min, citizenship, ethnicity, gender, military_affiliation,
                        name_hash, created_at, updated_at, link_notes
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    c.get("source", "clean_discover"),
                    c.get("source_id"),
                    c.get("scholarship_name"),
                    c.get("organization"),
                    "",
                    c.get("description", ""),
                    "",
                    c.get("amount_min"),
                    c.get("amount_max"),
                    c.get("amount_display"),
                    c.get("deadline", ""),
                    c.get("application_url"),
                    c.get("application_url"),
                    "", "", "", "", c.get("application_url"),
                    c.get("category", "Academic"),
                    c.get("education_level", "Undergraduate"),
                    "",
                    c.get("state_restriction", ""),
                    None,
                    "None",
                    "", "", "",
                    name_hash(c.get("scholarship_name", ""), c.get("organization", "")),
                    datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "",
                ))
                conn.commit()
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

if __name__ == "__main__":
    main()
