#!/usr/bin/env python3
"""
Parse saved scholarship pages and insert into DBs.
"""
import os
import sys
import json
import re
import sqlite3
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin

DATA_DIR = "/home/workspace/scholarsearch/data"
DB_PATH = f"{DATA_DIR}/processed/scholarships.db"
SITE_DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"
CONV_WORKSPACE = "/home/.z/workspaces/con_c8vlyHChdMPruaB5/read_webpage"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}

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
    m = re.search(r"[\$\€\£]?\s*([0-9,]+)", str(val).replace(",", ""))
    return int(m.group(1)) if m else None

def is_dup(conn, name, org):
    nh = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

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
        s.get("source", "parse_discovery"), s.get("source_id"),
        s.get("scholarship_name"), s.get("organization"), s.get("organization_type"),
        s.get("description"), s.get("eligibility"),
        s.get("amount_min"), s.get("amount_max"), s.get("amount_display"),
        s.get("deadline"), s.get("application_url"), s.get("form_url"),
        s.get("email"), s.get("phone"), s.get("address"), s.get("website"),
        s.get("category"), s.get("education_level"), s.get("field_of_study"),
        s.get("state_restriction"), s.get("gpa_min"),
        s.get("citizenship"), s.get("ethnicity"), s.get("gender"), s.get("military_affiliation"),
        name_hash(s.get("scholarship_name", ""), s.get("organization", "")),
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        s.get("link_notes"),
    ))
    conn.commit()
    return cur.lastrowid

def verify_link(url, timeout=15):
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout, headers=HEADERS)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}

def extract_from_ncstate(html, base_url):
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    # h2/h4 with class ncsc-simpletext__headline are scholarship names
    for tag in soup.find_all(["h2", "h4"], class_="ncsc-simpletext__headline"):
        name = tag.get_text(strip=True)
        if not name or len(name) < 5:
            continue
        # Find nearby link
        link = None
        parent = tag.find_parent()
        if parent:
            a = parent.find("a", href=True)
            if a:
                link = urljoin(base_url, a["href"])
        if not link:
            # Check next sibling
            nxt = tag.find_next_sibling()
            if nxt:
                a = nxt.find("a", href=True)
                if a:
                    link = urljoin(base_url, a["href"])
        # Find amount in nearby text
        amount = "Varies"
        parent_text = ""
        if tag.parent:
            parent_text = tag.parent.get_text(" ", strip=True)
        amt_match = re.search(r"\$[\d,]+(?:\.\d+)?", parent_text)
        if amt_match:
            amount = f"${amt_match.group(0).replace('$','').replace(',','')}"
        candidates.append({
            "scholarship_name": name[:180],
            "organization": "North Central State College",
            "application_url": link,
            "amount_display": amount,
            "deadline": "",
            "source": "ncstate_parse",
            "category": "Academic",
            "education_level": "Undergraduate",
            "state_restriction": "OH",
        })
    return candidates

def extract_from_utah(html, base_url):
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    # Look for h2/h3 with scholarship names
    for tag in soup.find_all(["h2", "h3"]):
        text = tag.get_text(strip=True)
        if "scholarship" not in text.lower() or len(text) < 10:
            continue
        # Get the next siblings until next heading
        detail_text = ""
        for sibling in tag.find_next_siblings():
            if sibling.name in ["h2", "h3", "h4"]:
                break
            detail_text += " " + sibling.get_text(" ", strip=True)
        # Extract amount
        amt_match = re.search(r"\$[\d,]+(?:\.\d+)?", detail_text)
        amount = f"${amt_match.group(0).replace('$','').replace(',','')}" if amt_match else "Varies"
        # Extract link
        link = None
        a = tag.find_next("a", href=True)
        if a:
            link = urljoin(base_url, a["href"])
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "University of Utah",
            "application_url": link,
            "amount_display": amount,
            "deadline": "",
            "source": "utah_parse",
            "category": "Academic",
            "education_level": "Undergraduate",
            "state_restriction": "UT",
        })
    return candidates

def extract_from_maldef(html, base_url):
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    # MALDEF guide has tables or lists of scholarships
    # Look for strong/bold text followed by links
    for tag in soup.find_all(["strong", "b", "td", "th", "li"]):
        text = tag.get_text(" ", strip=True)
        if "scholarship" not in text.lower() or len(text) < 10:
            continue
        link = None
        a = tag.find("a", href=True)
        if a:
            link = urljoin(base_url, a["href"])
        amt_match = re.search(r"\$[\d,]+(?:\.\d+)?", text)
        amount = f"${amt_match.group(0).replace('$','').replace(',','')}" if amt_match else "Varies"
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "MALDEF",
            "application_url": link,
            "amount_display": amount,
            "deadline": "",
            "source": "maldef_parse",
            "category": "Minority",
            "education_level": "Undergraduate",
        })
    return candidates

def extract_generic(html, base_url, source_name, org_name):
    """Generic parser: finds elements with 'scholarship' keyword."""
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    seen = set()
    for tag in soup.find_all(["h2", "h3", "h4", "h5", "li", "a", "td", "th", "div", "p", "span"]):
        text = tag.get_text(" ", strip=True)
        if not text or len(text) < 15 or len(text) > 300:
            continue
        if "scholarship" not in text.lower() and "bursary" not in text.lower() and "fellowship" not in text.lower():
            continue
        # Skip obvious navigation/footer
        if any(x in text.lower() for x in ["skip to main", "cookie policy", "privacy policy", "terms of service", "all rights reserved"]):
            continue
        key = normalize(text)
        if key in seen:
            continue
        seen.add(key)
        link = None
        a = tag.find("a", href=True) if tag.name != "a" else tag
        if tag.name == "a" and tag.get("href"):
            link = urljoin(base_url, tag["href"])
        elif a:
            link = urljoin(base_url, a["href"])
        amt_match = re.search(r"\$[\d,]+(?:\.\d+)?", text)
        amount = f"${amt_match.group(0).replace('$','').replace(',','')}" if amt_match else "Varies"
        candidates.append({
            "scholarship_name": text[:180],
            "organization": org_name,
            "application_url": link,
            "amount_display": amount,
            "deadline": "",
            "source": source_name,
            "category": "Academic",
            "education_level": "Undergraduate",
        })
    return candidates[:50]

def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    all_candidates = []
    
    # Parse saved HTML files
    files = [
        ("ncstatecollege.edu~~2fadmissions-and-aid~~2ffinancial-aid~~2fgrants-and-scholarships.html", 
         "https://ncstatecollege.edu/admissions-and-aid/financial-aid/grants-and-scholarships",
         "ncstate_parse", "North Central State College", extract_from_ncstate),
        ("studentresources.utah.edu~~2fourscholarships.php.html",
         "https://studentresources.utah.edu/ourscholarships.php",
         "utah_parse", "University of Utah", extract_from_utah),
        ("maldef.org~~2fresources~~2fscholarship-resource-guide-2026-2027.html",
         "https://www.maldef.org/resources/scholarship-resource-guide-2026-2027",
         "maldef_parse", "MALDEF", extract_from_maldef),
    ]
    
    for fname, base_url, src, org, extractor in files:
        path = os.path.join(CONV_WORKSPACE, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
            candidates = extractor(html, base_url)
            all_candidates.extend(candidates)
            print(f"Parsed {fname}: {len(candidates)} candidates")
    
    # Generic parse on all saved files
    generic_files = [
        ("accessscholarships.com~~2fblog~~2f50-scholarships-for-college-students.html", "Access Scholarships", "access_parse"),
        ("fastweb.com~~2fcollege-scholarships~~2farticles~~2ftop-scholarships-for-2026.html", "Fastweb", "fastweb_parse"),
        ("scholarships.com~~2ffinancial-aid~~2fcollege-scholarships~~2fscholarship-directory~~2fschool-year~~2fhigh-school-senior.html", "Scholarships.com", "scholarships_com_parse"),
    ]
    for fname, org, src in generic_files:
        path = os.path.join(CONV_WORKSPACE, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
            candidates = extract_generic(html, base_url, src, org)
            all_candidates.extend(candidates)
            print(f"Generic parsed {fname}: {len(candidates)} candidates")
    
    print(f"\nTotal candidates before dedup: {len(all_candidates)}")
    
    # Dedup and insert
    dbs = [DB_PATH, SITE_DB_PATH]
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    
    for candidate in all_candidates:
        if added >= limit:
            break
        name = candidate.get("scholarship_name", "")
        org = candidate.get("organization", "")
        url = candidate.get("application_url")
        
        # Skip junk
        if not name or len(name) < 5:
            continue
        if any(junk in name.lower() for junk in ["cItimes", "cray", "ctpl", "cf_chl", "cloudflare", "enable javascript"]):
            continue
        
        # Verify link if present
        if url:
            v = verify_link(url)
            if not v.get("ok"):
                skipped_verify += 1
                continue
            candidate["application_url"] = v.get("final_url", url)
        
        # Insert
        for db_path in dbs:
            conn = sqlite3.connect(db_path)
            if not is_dup(conn, name, org):
                add_scholarship(conn, candidate)
                added += 1
            else:
                skipped_dup += 1
            conn.close()
    
    print(f"Added: {added}, Skipped dup: {skipped_dup}, Skipped verify: {skipped_verify}")
    
    # Stats
    for db_path in dbs:
        conn = sqlite3.connect(db_path)
        total = conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
        print(f"{db_path}: {total}")
        conn.close()

if __name__ == "__main__":
    main()
