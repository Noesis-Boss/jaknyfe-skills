#!/usr/bin/env python3
"""Supplemental scholarship discovery from scholarshipregion.com category pages."""

import json, re, sqlite3, hashlib, os, sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

CATEGORY_URLS = [
    "https://www.scholarshipregion.com/category/scholarships-for-americans/scholarships-for-high-school-seniors/",
    "https://www.scholarshipregion.com/category/scholarships/undergraduate-scholarships/",
    "https://www.scholarshipregion.com/category/scholarships/women/",
    "https://www.scholarshipregion.com/category/scholarships-in-usa/",
    "https://www.scholarshipregion.com/category/scholarships-in-canada/",
    "https://www.scholarshipregion.com/category/scholarships-in-uk/",
    "https://www.scholarshipregion.com/category/scholarships-in-australia/",
    "https://www.scholarshipregion.com/category/scholarships-in-europe/",
]

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ZoBot/1.0)"}


def get_existing_hashes():
    hashes = set()
    for db in DBS:
        conn = sqlite3.connect(db)
        try:
            rows = conn.execute("SELECT name_hash FROM scholarships WHERE name_hash IS NOT NULL").fetchall()
            hashes.update(r[0] for r in rows)
        except Exception:
            pass
        finally:
            conn.close()
    return hashes


def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"fetch error {url}: {e}", file=sys.stderr)
        return None


def extract_articles(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    seen = set()
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = urljoin(base_url, a["href"])
        if not text or len(text) < 15:
            continue
        if "scholarshipregion.com" not in href:
            continue
        if any(skip in href for skip in ["/category/", "/feed", "wp-content", "wp-json", "tag/", "author/"]):
            continue
        if href in seen:
            continue
        # Only keep if title mentions scholarship/fellowship/grant/award/bursary
        if not re.search(r"scholarship|fellowship|grant|award|bursary", text, re.I):
            continue
        seen.add(href)
        articles.append({"title": text, "url": href})
    return articles


def parse_article(url):
    html = fetch(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    # Name from h1
    h1 = soup.find("h1")
    name = h1.get_text(strip=True) if h1 else ""
    # Clean common suffixes
    name = re.sub(r"\s*\|.*$", "", name).strip()
    name = re.sub(r"\s*-\s*How To Apply.*$", "", name, flags=re.I).strip()
    name = re.sub(r"\s*2026|2027|2028", "", name).strip()
    name = name.strip("| -")
    if not name:
        return None

    # Application URL: find a tag with "click here to apply" or similar
    apply_url = None
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True).lower()
        href = a["href"]
        if "click here to apply" in text or "apply now" in text or "official website" in text:
            apply_url = href
            break
    if not apply_url:
        # fallback: first external link
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http") and "scholarshipregion.com" not in href:
                apply_url = href
                break
    if not apply_url:
        return None

    # Amount
    amount_min = None
    amount_max = None
    amount_display = None
    text = soup.get_text(separator=" ")
    amounts = re.findall(r"\$\s*([\d,]+(?:\.\d+)?)\s*(?:USD|million|M)?", text, re.I)
    if amounts:
        nums = [float(a.replace(",", "")) for a in amounts if a.replace(",", "").replace(".", "").isdigit()]
        if nums:
            amount_min = int(min(nums))
            amount_max = int(max(nums))
            amount_display = f"${amount_min:,}" + (f" - ${amount_max:,}" if amount_max > amount_min else "")
    if not amount_display:
        if re.search(r"fully funded", text, re.I):
            amount_display = "Fully Funded"
            amount_min = 0
            amount_max = 0

    # Deadline
    deadline = None
    m = re.search(r"(?:deadline|closes|ends|due date)[\s:]+([A-Za-z]+\s+\d{1,2},?\s*\d{4})", text, re.I)
    if m:
        deadline = m.group(1)
    else:
        m = re.search(r"([A-Za-z]+\s+\d{1,2},?\s*\d{4})", text)
        if m:
            deadline = m.group(1)

    # Organization: try to extract from text or use domain of apply_url
    org = ""
    m = re.search(r"(?:by|from|sponsored by|offered by)\s+([A-Za-z0-9&;,.\s]+?)(?:\s+for|\s+in|\s+to|\s*\.|\s*\|)", text, re.I)
    if m:
        org = m.group(1).strip()
    if not org:
        parsed = urlparse(apply_url)
        org = parsed.netloc.replace("www.", "")

    # Category / education level inference from title/category
    category = "Academic"
    education_level = "Undergraduate"
    residency = "US"
    combined = (name + " " + text).lower()
    if re.search(r"\bgraduate\b|\bmasters?\b|\bph\.?d\b", combined):
        education_level = "Graduate"
    if re.search(r"\bhigh school\b|\bhighschool\b|\bgrade 12\b", combined):
        education_level = "High School"
    if re.search(r"\bassociate\b|\bcommunity college\b", combined):
        education_level = "Associate"
    if re.search(r"\btrade\b|\bvocational\b|\btechnical\b", combined):
        education_level = "Trade School"
    if re.search(r"\bwomen\b|\bfemale\b", combined):
        category = "Women"
    if re.search(r"\bstem\b|\bengineering\b|\bcomputer science\b|\bmath\b|\btechnology\b", combined):
        category = "STEM"
    if re.search(r"\bmedicine\b|\bnursing\b|\bhealth\b", combined):
        category = "Medicine"
    if re.search(r"\blaw\b|\blegal\b", combined):
        category = "Law"
    if re.search(r"\bbusiness\b|\bentrepreneur\b", combined):
        category = "Business"
    if re.search(r"\bart\b|\bhumanities\b|\bcreative\b", combined):
        category = "Arts"
    if re.search(r"\bmasonic\b|\bfreemason\b", combined):
        category = "Masonic"
    if re.search(r"\bmilitary\b|\bveteran\b", combined):
        category = "Military/Veteran"
    if re.search(r"\bcommunity\b|\bservice\b", combined):
        category = "Community"
    if re.search(r"\bcanada\b|\bcanadian\b", combined):
        residency = "Canada"
    elif re.search(r"\buk\b|\bunited kingdom\b|\bbritish\b", combined):
        residency = "UK"
    elif re.search(r"\baustralia\b|\baustralian\b", combined):
        residency = "Australia"
    elif re.search(r"\beurope\b|\bgerman\b|\bfrench\b|\bdutch\b|\bnorway\b|\bsweden\b|\bswiss\b", combined):
        residency = "EU"
    elif re.search(r"\binternational\b|\bglobal\b", combined):
        residency = "International"

    state_restriction = None
    m = re.search(r"\b([A-Z]{2})\b(?:\s+resident|\s+citizen)?", text)
    if m and m.group(1) in {
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    }:
        state_restriction = m.group(1)

    # Verify link (HEAD)
    link_status = "unchecked"
    final_url = apply_url
    try:
        r = requests.head(apply_url, headers=HEADERS, timeout=15, allow_redirects=True)
        link_status = str(r.status_code)
        final_url = r.url
    except Exception as e:
        link_status = f"error: {e}"

    return {
        "source": "supplement_scholarshipregion",
        "source_id": f"supplement_{hashlib.md5(url.encode()).hexdigest()[:8]}_{re.sub(r'[^a-z0-9]','', name)[:20]}",
        "scholarship_name": name,
        "organization": org,
        "organization_type": "",
        "description": "",
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "application_url": final_url,
        "form_url": "",
        "email": "",
        "phone": "",
        "address": "",
        "website": "",
        "category": category,
        "education_level": education_level,
        "field_of_study": "",
        "residency_requirement": residency,
        "state_restriction": state_restriction,
        "gpa_min": None,
        "citizenship": "",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "created_at": "2026-07-15",
        "updated_at": "2026-07-15",
        "url_status": link_status,
        "last_checked": "2026-07-15",
        "link_notes": "",
        "name_hash": hashlib.sha256((name + org).encode()).hexdigest(),
        "active": 1 if link_status.startswith("2") or link_status.startswith("3") else 0,
    }


def main():
    existing = get_existing_hashes()
    print(f"Existing name_hashes: {len(existing)}")
    results = []
    seen_hashes = set()
    for cat_url in CATEGORY_URLS:
        print(f"\nFetching category: {cat_url}")
        html = fetch(cat_url)
        if not html:
            continue
        articles = extract_articles(html, cat_url)
        print(f"  Found {len(articles)} candidate articles")
        for art in articles:
            data = parse_article(art["url"])
            if not data:
                continue
            if data["name_hash"] in existing or data["name_hash"] in seen_hashes:
                continue
            seen_hashes.add(data["name_hash"])
            results.append(data)
            if len(results) >= 120:  # target a bit above 90 to account for failures
                break
        if len(results) >= 120:
            break

    print(f"\nPrepared {len(results)} new scholarships")
    out_path = "/home/workspace/scholarship-discovery/scripts/supplement_input.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
