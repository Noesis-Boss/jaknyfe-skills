#!/usr/bin/env python3
"""
Read individual scholarship pages, extract structured data, verify, and insert.
"""
import os
import sys
import json
import re
import sqlite3
import hashlib
import time
import random
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

SITE_DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"
CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP/read_webpage"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 20


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


def guess_state(text):
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


def guess_country(url):
    if ".edu" in url or ".gov" in url:
        if any(t in url for t in [".edu/uk", ".ac.uk", "ucas", "scholarships.org.uk"]):
            return "UK"
        if any(t in url for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
            return "Canada"
        if any(t in url for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
            return "Australia"
        return "USA"
    return "International"


def is_dup(conn, name, org):
    nh = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None


def verify_link(url):
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


def add_scholarship(conn, s):
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
        s.get("source", "page_discovery"),
        s.get("source_id"),
        s.get("scholarship_name"),
        s.get("organization"),
        s.get("organization_type"),
        s.get("description"),
        s.get("eligibility"),
        s.get("amount_min"),
        s.get("amount_max"),
        s.get("amount_display"),
        s.get("deadline"),
        s.get("application_url"),
        s.get("form_url"),
        s.get("email"),
        s.get("phone"),
        s.get("address"),
        s.get("website"),
        s.get("category"),
        s.get("education_level"),
        s.get("field_of_study"),
        s.get("state_restriction"),
        s.get("gpa_min"),
        s.get("citizenship"),
        s.get("ethnicity"),
        s.get("gender"),
        s.get("military_affiliation"),
        name_hash(s.get("scholarship_name", ""), s.get("organization", "")),
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        s.get("link_notes"),
    ))
    conn.commit()
    return cur.lastrowid


def extract_from_studentscholarships(html, base_url):
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    
    # Find scholarship cards - look for h1/h2 with "Scholarship Application"
    for tag in soup.find_all(["h1", "h2"]):
        text = tag.get_text(strip=True)
        if not text or len(text) < 5:
            continue
        
        # Look for amount in nearby text
        amount_min = None
        amount_max = None
        amount_display = "Varies"
        
        # Get all text in the card
        card_text = text
        parent = tag.find_parent()
        if parent:
            card_text = parent.get_text(" ", strip=True)
        
        # Extract amount
        amt_match = re.search(r"\$([0-9,]+)(?:\s*-\s*\$([0-9,]+))?", card_text)
        if amt_match:
            amount_min = int(amt_match.group(1).replace(",", ""))
            amount_max = int(amt_match.group(2).replace(",", "")) if amt_match.group(2) else None
            if amount_min and amount_max and amount_min == amount_max:
                amount_display = f"${amount_min:,}"
            elif amount_min and amount_max:
                amount_display = f"${amount_min:,} - ${amount_max:,}"
            elif amount_min:
                amount_display = f"${amount_min:,}+"
            elif amount_max:
                amount_display = f"Up to ${amount_max:,}"
        
        # Extract deadline
        deadline = ""
        dl_match = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4})", card_text, re.I)
        if dl_match:
            deadline = dl_match.group(1)
        
        # Extract organization
        org = ""
        org_match = re.search(r"(?:provided by|offered by|from|by)\s+([A-Za-z0-9 &]+)", card_text, re.I)
        if org_match:
            org = org_match.group(1).strip()
            if len(org) > 100:
                org = org[:100]
        
        # Find application link
        app_url = base_url
        a_tag = tag.find_next("a", href=True)
        if a_tag:
            app_url = urljoin(base_url, a_tag["href"])
        
        candidates.append({
            "scholarship_name": text[:180],
            "organization": org or "Unknown",
            "organization_type": "Unknown",
            "description": card_text[:500],
            "eligibility": "",
            "amount_min": amount_min,
            "amount_max": amount_max,
            "amount_display": amount_display,
            "deadline": deadline,
            "application_url": app_url,
            "form_url": app_url,
            "email": "",
            "phone": "",
            "address": "",
            "website": base_url,
            "category": "Academic",
            "education_level": "Undergraduate",
            "field_of_study": "",
            "state_restriction": guess_state(card_text) or "",
            "gpa_min": None,
            "citizenship": "None",
            "ethnicity": "",
            "gender": "",
            "military_affiliation": "",
            "source": "studentscholarships",
            "source_id": hashlib.md5((text + base_url).encode()).hexdigest()[:12],
            "link_notes": "",
        })
    
    return candidates


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    
    # Load all search result files
    search_files = []
    if os.path.exists(CONV_WORKSPACE):
        for f in os.listdir(CONV_WORKSPACE):
            if f.startswith("web_search") and f.endswith(".json"):
                search_files.append(os.path.join(CONV_WORKSPACE, f))
    
    print(f"Found {len(search_files)} search result files")
    
    # Extract URLs from search results
    urls = set()
    for sf in search_files:
        try:
            with open(sf, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            items = data if isinstance(data, list) else data.get("results", data.get("data", []))
            for item in items:
                url = item.get("url", "")
                if url and url.startswith("http"):
                    urls.add(url)
        except Exception as e:
            print(f"Error reading {sf}: {e}")
    
    print(f"Found {len(urls)} unique URLs")
    
    # Process each URL
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    errors = 0
    verified = []
    
    conn = sqlite3.connect(SITE_DB_PATH)
    
    for url in list(urls)[:limit * 3]:  # Fetch more than needed
        if added >= limit:
            break
        
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            if resp.status_code != 200:
                continue
            
            html = resp.text
            base_url = resp.url
            
            # Try to extract scholarships
            candidates = []
            
            # Pattern 1: studentscholarships.org
            if "studentscholarships.org" in base_url:
                candidates = extract_from_studentscholarships(html, base_url)
            
            # Pattern 2: scholarships360.org
            elif "scholarships360.org" in base_url:
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup.find_all(["h2", "h3", "h4"]):
                    text = tag.get_text(strip=True)
                    if "scholarship" in text.lower() and len(text) > 10:
                        # Find nearby link
                        link = None
                        parent = tag.find_parent()
                        if parent:
                            a = parent.find("a", href=True)
                            if a:
                                link = urljoin(base_url, a["href"])
                        
                        # Find amount
                        amount_display = "Varies"
                        amount_min = None
                        amount_max = None
                        detail = ""
                        for sibling in tag.find_next_siblings():
                            if sibling.name in ["h2", "h3", "h4"]:
                                break
                            detail += " " + sibling.get_text(" ", strip=True)
                        
                        amt_match = re.search(r"\$([0-9,]+)(?:\s*-\s*\$([0-9,]+))?", detail)
                        if amt_match:
                            amount_min = int(amt_match.group(1).replace(",", ""))
                            amount_max = int(amt_match.group(2).replace(",", "")) if amt_match.group(2) else None
                            if amount_min == amount_max:
                                amount_display = f"${amount_min:,}"
                            elif amount_min and amount_max:
                                amount_display = f"${amount_min:,} - ${amount_max:,}"
                            elif amount_min:
                                amount_display = f"${amount_min:,}+"
                        
                        candidates.append({
                            "scholarship_name": text[:180],
                            "organization": "Scholarships360",
                            "organization_type": "Platform",
                            "description": detail[:500],
                            "eligibility": "",
                            "amount_min": amount_min,
                            "amount_max": amount_max,
                            "amount_display": amount_display,
                            "deadline": "",
                            "application_url": link or base_url,
                            "form_url": link or base_url,
                            "email": "",
                            "phone": "",
                            "address": "",
                            "website": base_url,
                            "category": "Academic",
                            "education_level": "Undergraduate",
                            "field_of_study": "",
                            "state_restriction": guess_state(detail) or "",
                            "gpa_min": None,
                            "citizenship": "None",
                            "ethnicity": "",
                            "gender": "",
                            "military_affiliation": "",
                            "source": "scholarships360",
                            "source_id": hashlib.md5((text + base_url).encode()).hexdigest()[:12],
                            "link_notes": "",
                        })
            
            # Dedup candidates from this page
            seen = set()
            for c in candidates:
                key = normalize(c["scholarship_name"]) + "||" + normalize(c["organization"])
                if key in seen:
                    continue
                seen.add(key)
                
                if is_dup(conn, c["scholarship_name"], c["organization"]):
                    skipped_dup += 1
                    continue
                
                # Verify link
                vr = verify_link(c.get("application_url"))
                if not vr.get("ok"):
                    skipped_verify += 1
                    continue
                
                if vr.get("final_url"):
                    c["application_url"] = vr["final_url"]
                    c["form_url"] = vr["final_url"]
                
                add_scholarship(conn, c)
                added += 1
                verified.append(c)
                
                if added % 10 == 0:
                    print(f"Progress: added={added}, skipped_dup={skipped_dup}, skipped_verify={skipped_verify}")
                
                time.sleep(0.2)  # Be polite
                
        except Exception as e:
            errors += 1
    
    conn.close()
    
    # Final stats
    conn2 = sqlite3.connect(SITE_DB_PATH)
    cur = conn2.cursor()
    cur.execute("SELECT COUNT(*) FROM scholarships")
    total = cur.fetchone()[0]
    conn2.close()
    
    print(f"\nFinal Results:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: {errors}")
    print(f"  DB total: {total}")
    
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
