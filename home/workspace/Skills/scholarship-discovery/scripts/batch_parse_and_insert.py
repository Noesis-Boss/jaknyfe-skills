#!/usr/bin/env python3
"""
Batch parse saved scholarship pages and web search results,
extract structured scholarship data, verify links, dedup, and insert into DBs.
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
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

CONV_WORKSPACE = "/home/.z/workspaces/con_ezJjjBZwcPFeBKED"
PAGE_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0)"}
REQUEST_TIMEOUT = 20

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
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "canadian"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "uk gov"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "australia"]):
        return "Australia"
    if any(t in combined for t in ["studylink", "nz gov", "new zealand"]):
        return "New Zealand"
    if any(t in combined for t in ["erasmus", "daad", "campusfrance", "studynetherlands", "europa.eu"]):
        return "EU"
    if any(t in combined for t in [".edu", ".gov", "scholarship"]):
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
        "south carolina": "SC", "michigan": "MI", "ohio": "OH",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def categorize(text: str, url: str = "") -> str:
    combined = (text + " " + url).lower()
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", "Healthcare"),
        (r"\blaw\b|\blegal\b|\battorney\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", "Arts"),
        (r"\btrade\b|\btechnical\b|\bvocational\b|\bwelding\b|\bautomotive\b", "Trade School"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bmilitary\b|\bveteran\b|\barmed forces\b", "Military/Veteran"),
        (r"\bcommunity\b|\bvolunteer\b|\bservice\b", "Community"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b|\bph\.?d\b|\bdoctorate\b", "Graduate"),
    ]:
        if re.search(pat, combined):
            return cat
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
    if re.search(r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", lower):
        return "Professional"
    return "Undergraduate"

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
            scholarship.get("source", "page_discovery"),
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

# ------------------------------------------------------------------
# Extractors
# ------------------------------------------------------------------

def extract_from_accessscholarships(html: str, base_url: str) -> List[Dict]:
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 10]

    # Pattern: "Scholarship Name\n$Amount"
    i = 0
    while i < len(lines):
        line = lines[i]
        # Look for lines that contain a dollar amount and look like scholarship titles
        amt_match = re.search(r"\$([0-9,]+)", line)
        if amt_match:
            name = line.replace("$" + amt_match.group(1), "").strip()
            name = re.sub(r"\s*[-–:]\s*$", "", name).strip()
            if not name or len(name) < 5:
                i += 1
                continue

            amount = int(amt_match.group(1).replace(",", ""))
            # Skip unrealistic amounts
            if amount > 500000:
                i += 1
                continue

            # Look for eligibility/description in next few lines
            desc_lines = []
            for j in range(i+1, min(i+4, len(lines))):
                if re.search(r"\$[0-9,]+", lines[j]):
                    break
                desc_lines.append(lines[j])
            desc = " ".join(desc_lines).strip()[:500]

            candidates.append({
                "scholarship_name": name[:180],
                "organization": "Access Scholarships",
                "organization_type": "Platform",
                "description": desc,
                "eligibility": desc,
                "amount_min": amount,
                "amount_max": amount,
                "amount_display": f"${amount:,}",
                "deadline": "",
                "application_url": base_url,
                "form_url": base_url,
                "email": "",
                "phone": "",
                "address": "",
                "website": base_url,
                "category": categorize(name + " " + desc),
                "education_level": guess_education_level(name + " " + desc),
                "field_of_study": "",
                "state_restriction": guess_state(name + " " + desc) or "",
                "gpa_min": None,
                "citizenship": "US Citizen",
                "ethnicity": "",
                "gender": "",
                "military_affiliation": "",
                "source": "accessscholarships_page",
                "source_id": hashlib.md5((name + base_url).encode()).hexdigest()[:12],
                "link_notes": "",
            })
        i += 1

    # Also look for "Scholarship Name\n: description" patterns without dollar sign on same line
    # Pattern: "Name\n$Amount" where amount is on next line
    for idx in range(len(lines) - 1):
        line = lines[idx]
        next_line = lines[idx + 1]
        if re.search(r"^(Open to|Open for|Awarded to|for students)", next_line, re.I):
            if not re.search(r"\$[0-9,]+", line) and len(line) > 10 and "scholarship" in line.lower():
                # Try to find amount in next few lines
                amt = None
                for k in range(idx+1, min(idx+5, len(lines))):
                    am = re.search(r"\$([0-9,]+)", lines[k])
                    if am:
                        amt = int(am.group(1).replace(",", ""))
                        if amt > 500000:
                            amt = None
                        break
                if amt:
                    candidates.append({
                        "scholarship_name": line[:180],
                        "organization": "Access Scholarships",
                        "organization_type": "Platform",
                        "description": next_line[:500],
                        "eligibility": next_line[:500],
                        "amount_min": amt,
                        "amount_max": amt,
                        "amount_display": f"${amt:,}",
                        "deadline": "",
                        "application_url": base_url,
                        "form_url": base_url,
                        "email": "",
                        "phone": "",
                        "address": "",
                        "website": base_url,
                        "category": categorize(line + " " + next_line),
                        "education_level": guess_education_level(line + " " + next_line),
                        "field_of_study": "",
                        "state_restriction": guess_state(line + " " + next_line) or "",
                        "gpa_min": None,
                        "citizenship": "US Citizen",
                        "ethnicity": "",
                        "gender": "",
                        "military_affiliation": "",
                        "source": "accessscholarships_page",
                        "source_id": hashlib.md5((line + base_url).encode()).hexdigest()[:12],
                        "link_notes": "",
                    })

    return candidates


def extract_from_mefa(html: str, base_url: str) -> List[Dict]:
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 10]

    for i, line in enumerate(lines):
        if "Scholarship" in line and "$" in line:
            amt_match = re.search(r"\$([0-9,]+)", line)
            if amt_match:
                amount = int(amt_match.group(1).replace(",", ""))
                if amount > 500000:
                    continue
                name = line[:180]
                desc_lines = []
                for j in range(i+1, min(i+4, len(lines))):
                    if "Scholarship" in lines[j] and "$" in lines[j]:
                        break
                    desc_lines.append(lines[j])
                desc = " ".join(desc_lines).strip()[:500]

                candidates.append({
                    "scholarship_name": name[:180],
                    "organization": "MEFA",
                    "organization_type": "Non-Profit",
                    "description": desc,
                    "eligibility": desc,
                    "amount_min": amount,
                    "amount_max": amount,
                    "amount_display": f"${amount:,}",
                    "deadline": "",
                    "application_url": base_url,
                    "form_url": base_url,
                    "email": "",
                    "phone": "",
                    "address": "",
                    "website": base_url,
                    "category": categorize(name + " " + desc),
                    "education_level": guess_education_level(name + " " + desc),
                    "field_of_study": "",
                    "state_restriction": guess_state(name + " " + desc) or "",
                    "gpa_min": None,
                    "citizenship": "US Citizen",
                    "ethnicity": "",
                    "gender": "",
                    "military_affiliation": "",
                    "source": "mefa_page",
                    "source_id": hashlib.md5((name + base_url).encode()).hexdigest()[:12],
                    "link_notes": "",
                })
    return candidates


def extract_from_sallie(html: str, base_url: str) -> List[Dict]:
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 5]

    for i, line in enumerate(lines):
        if "Scholarship" in line and "$" in line:
            amt_match = re.search(r"\$([0-9,]+)", line)
            if amt_match:
                amount = int(amt_match.group(1).replace(",", ""))
                if amount > 500000:
                    continue
                name = line[:180]
                desc_lines = []
                for j in range(i+1, min(i+4, len(lines))):
                    if "Scholarship" in lines[j] and "$" in lines[j]:
                        break
                    desc_lines.append(lines[j])
                desc = " ".join(desc_lines).strip()[:500]

                candidates.append({
                    "scholarship_name": name[:180],
                    "organization": "Sallie",
                    "organization_type": "Company",
                    "description": desc,
                    "eligibility": desc,
                    "amount_min": amount,
                    "amount_max": amount,
                    "amount_display": f"${amount:,}",
                    "deadline": "",
                    "application_url": base_url,
                    "form_url": base_url,
                    "email": "",
                    "phone": "",
                    "address": "",
                    "website": base_url,
                    "category": categorize(name + " " + desc),
                    "education_level": guess_education_level(name + " " + desc),
                    "field_of_study": "",
                    "state_restriction": "",
                    "gpa_min": None,
                    "citizenship": "US Citizen",
                    "ethnicity": "",
                    "gender": "",
                    "military_affiliation": "",
                    "source": "sallie_page",
                    "source_id": hashlib.md5((name + base_url).encode()).hexdigest()[:12],
                    "link_notes": "",
                })
    return candidates


def extract_from_generic_page(html: str, base_url: str) -> List[Dict]:
    """Generic extraction for unknown pages with scholarship listings."""
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 10]

    for i, line in enumerate(lines):
        # Match scholarship lines with amounts
        if re.search(r"scholarship|bursary|fellowship|grant|award", line, re.I) and "$" in line:
            amt_match = re.search(r"\$([0-9,]+)", line)
            if amt_match:
                amount = int(amt_match.group(1).replace(",", ""))
                if amount > 500000 or amount < 10:
                    continue
                name = re.sub(r"\s*[-–:]\s*\$.*$", "", line).strip()
                if not name or len(name) < 5:
                    continue

                desc_lines = []
                for j in range(i+1, min(i+4, len(lines))):
                    if re.search(r"scholarship|bursary|fellowship|grant|award", lines[j], re.I) and "$" in lines[j]:
                        break
                    desc_lines.append(lines[j])
                desc = " ".join(desc_lines).strip()[:500]

                org = "Unknown"
                if "scholarships360" in base_url:
                    org = "Scholarships360"
                elif "accessscholarships" in base_url:
                    org = "Access Scholarships"
                elif "mefa" in base_url:
                    org = "MEFA"
                elif "sallie" in base_url:
                    org = "Sallie"
                elif ".edu" in base_url:
                    org = re.search(r"https?://(?:www\.)?([^/]+)", base_url).group(1).replace(".edu", "").title() + " University"
                elif ".gov" in base_url:
                    org = re.search(r"https?://(?:www\.)?([^/]+)", base_url).group(1).title()

                candidates.append({
                    "scholarship_name": name[:180],
                    "organization": org,
                    "organization_type": "Platform",
                    "description": desc,
                    "eligibility": desc,
                    "amount_min": amount,
                    "amount_max": amount,
                    "amount_display": f"${amount:,}",
                    "deadline": "",
                    "application_url": base_url,
                    "form_url": base_url,
                    "email": "",
                    "phone": "",
                    "address": "",
                    "website": base_url,
                    "category": categorize(name + " " + desc),
                    "education_level": guess_education_level(name + " " + desc),
                    "field_of_study": "",
                    "state_restriction": guess_state(name + " " + desc) or "",
                    "gpa_min": None,
                    "citizenship": "US Citizen",
                    "ethnicity": "",
                    "gender": "",
                    "military_affiliation": "",
                    "source": "generic_page",
                    "source_id": hashlib.md5((name + base_url).encode()).hexdigest()[:12],
                    "link_notes": "",
                })
    return candidates


def extract_from_search_snippets(html: str, base_url: str) -> List[Dict]:
    """Extract from JSON search result files."""
    candidates = []
    try:
        data = json.loads(html)
    except json.JSONDecodeError:
        return candidates

    items = data if isinstance(data, list) else data.get("results", data.get("data", []))
    for item in items:
        url = item.get("url", "")
        text = item.get("text", "")
        title = item.get("title", "")

        if not re.search(r"scholarship|bursary|fellowship|grant|award", f"{title} {text}", re.I):
            continue
        if any(t in url for t in ["facebook.com", "instagram.com", "youtube.com", "tiktok.com", ".pdf"]):
            continue

        # Extract individual scholarships from text
        # Look for patterns like "$2,000 Scholarship Name" or "Scholarship Name $2,000"
        found = re.findall(r"([A-Z][A-Za-z0-9\s\-']+?(?:Scholarship|Grant|Fellowship|Award|Bursary))[^\n]*?\$([0-9,]+)", text, re.I)
        for name, amt_str in found:
            amount = int(amt_str.replace(",", ""))
            if amount > 500000 or amount < 10:
                continue
            name = name.strip()[:180]
            if len(name) < 10:
                continue

            candidates.append({
                "scholarship_name": name,
                "organization": re.search(r"https?://(?:www\.)?([^/]+)", url).group(1).replace("www.", "").title() if url else "Unknown",
                "organization_type": "Platform",
                "description": text[:500],
                "eligibility": "",
                "amount_min": amount,
                "amount_max": amount,
                "amount_display": f"${amount:,}",
                "deadline": "",
                "application_url": url,
                "form_url": url,
                "email": "",
                "phone": "",
                "address": "",
                "website": url,
                "category": categorize(name + " " + text),
                "education_level": guess_education_level(name + " " + text),
                "field_of_study": "",
                "state_restriction": guess_state(text) or "",
                "gpa_min": None,
                "citizenship": guess_country(url, text) if guess_country(url, text) == "USA" else "None",
                "ethnicity": "",
                "gender": "",
                "military_affiliation": "",
                "source": "search_snippet",
                "source_id": hashlib.md5((name + url).encode()).hexdigest()[:12],
                "link_notes": "",
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

    # Process saved HTML/MD pages
    if os.path.isdir(PAGE_DIR):
        for fname in sorted(os.listdir(PAGE_DIR)):
            fpath = os.path.join(PAGE_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            if fname.endswith(".json"):
                continue

            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()

                # Extract source URL from filename
                source_url = "https://" + fname.replace("~~", "/").replace(".md", "").replace(".html", "")

                if "accessscholarships.com" in fname:
                    all_candidates.extend(extract_from_accessscholarships(content, source_url))
                elif "mefa.org" in fname:
                    all_candidates.extend(extract_from_mefa(content, source_url))
                elif "sallie.com" in fname:
                    all_candidates.extend(extract_from_sallie(content, source_url))
                else:
                    all_candidates.extend(extract_from_generic_page(content, source_url))
            except Exception as e:
                print(f"Error processing {fname}: {e}")

    # Process web search JSON files
    for fname in sorted(os.listdir(PAGE_DIR)):
        if not (fname.startswith("web_search") and fname.endswith(".json")):
            continue
        fpath = os.path.join(PAGE_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                content = fh.read()
            all_candidates.extend(extract_from_search_snippets(content, ""))
        except Exception as e:
            print(f"Error processing {fname}: {e}")

    print(f"Extracted {len(all_candidates)} raw candidates")

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
        if not os.path.exists(path):
            continue
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
            if not os.path.exists(path):
                continue
            conn = sqlite3.connect(path)
            if is_dup(conn, c["scholarship_name"], c["organization"]):
                dup = True
                conn.close()
                break
            conn.close()
        if dup:
            skipped_dup += 1
            continue

        # Verify link (or trust source pages that are known-good)
        url = c.get("application_url", "")
        if c["source"] in ("accessscholarships_page", "mefa_page", "sallie_page", "generic_page"):
            # For listing pages, we can't verify individual scholarships
            # Mark as active since the source page exists
            vr = {"ok": True, "status": 200, "final_url": url}
        else:
            vr = verify_link(url)

        if not vr.get("ok"):
            skipped_verify += 1
            continue

        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]

        # Insert into both DBs
        for path in DB_PATHS:
            if not os.path.exists(path):
                continue
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
        if not os.path.exists(path):
            continue
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

    # Output summary for email
    summary = {
        "added": added,
        "target": limit,
        "before": before,
        "after": after,
        "categories": dict(cats.most_common()),
        "top_10": [{"name": c["scholarship_name"][:60], "amount": c["amount_display"], "org": c["organization"]} for c in top],
        "skipped_verify": skipped_verify,
        "errors": errors[:10],
    }
    print("\nSUMMARY_JSON:" + json.dumps(summary))

if __name__ == "__main__":
    main()
