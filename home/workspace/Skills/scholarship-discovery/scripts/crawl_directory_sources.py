#!/usr/bin/env python3
"""Crawl scholarship directory pages and ingest linked individual scholarships."""
import argparse
import hashlib
import re
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DB_PATHS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0)"}
SCHOLARSHIP_WORDS = re.compile(r"scholarship|bursary|fellowship|grant|award", re.I)
SKIP_LINKS = re.compile(r"facebook|instagram|linkedin|twitter|youtube|mailto:|tel:|\.pdf$", re.I)
INDEX_TITLE = re.compile(r"browse|manage|database|scholarship sites|scholarship info|scholarship scams|foundation$|association$", re.I)


def normalize(value):
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def name_hash(name, organization):
    return hashlib.sha1(f"{normalize(name)}||{normalize(organization)}".encode()).hexdigest()[:12]


def fetch(url):
    response = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
    response.raise_for_status()
    return response.url, response.text


def individual_links(index_url, html):
    base = urlparse(index_url)
    soup = BeautifulSoup(html, "html.parser")
    results = []
    seen = set()
    for anchor in soup.select("a[href]"):
        href = urljoin(index_url, anchor["href"]).split("#", 1)[0]
        text = " ".join(anchor.get_text(" ", strip=True).split())
        parsed = urlparse(href)
        if parsed.scheme not in {"http", "https"} or SKIP_LINKS.search(href):
            continue
        if href.rstrip("/") == index_url.rstrip("/") or href in seen:
            continue
        if not text or len(text) < 8 or not SCHOLARSHIP_WORDS.search(text):
            continue
        if parsed.netloc == base.netloc and parsed.path.rstrip("/") in {base.path.rstrip("/"), "/scholarships"}:
            continue
        seen.add(href)
        results.append((href, text))
    return results


def parse_detail(url, link_text, html, source_domain):
    soup = BeautifulSoup(html, "html.parser")
    text = " ".join(soup.get_text(" ", strip=True).split())
    title_node = soup.find("h1") or soup.find("title")
    title = " ".join(title_node.get_text(" ", strip=True).split()) if title_node else link_text
    if not SCHOLARSHIP_WORDS.search(f"{title} {text}"):
        return None
    title = re.sub(r"\s*[|·-]\s*[^|·-]+$", "", title).strip()[:180] or link_text[:180]
    if INDEX_TITLE.search(title):
        return None
    domain = urlparse(url).netloc.lower()
    organization = source_domain.replace("www.", "").split(".")[0].replace("financialaid", "").strip("-").title()
    if "western" in text.lower() or "wwu" in text.lower():
        organization = "Western Washington University"
    amount = re.search(r"\$\s*([0-9][0-9,]*)", text)
    deadline = re.search(r"(?:deadline|due date|apply by|applications due)[:\s]+([A-Za-z]+\s+\d{1,2},?\s+\d{4}|\d{1,2}/\d{1,2}/\d{4})", text, re.I)
    application_url = url
    for anchor in soup.select("a[href]"):
        label = anchor.get_text(" ", strip=True).lower()
        href = urljoin(url, anchor["href"])
        if re.search(r"apply|application|submit", label) and urlparse(href).netloc.lower() != domain:
            application_url = href.split("#", 1)[0]
            break
    return {
        "source": f"directory_{source_domain.replace('.', '_')}",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "scholarship_name": title,
        "organization": organization,
        "organization_type": "University",
        "description": text[:1000],
        "eligibility": "",
        "amount_min": int(amount.group(1).replace(",", "")) if amount else None,
        "amount_max": None,
        "amount_display": f"${amount.group(1)}" if amount else "Varies",
        "deadline": deadline.group(1) if deadline else "",
        "application_url": application_url,
        "website": url,
        "category": "Academic",
        "education_level": "Undergraduate" if "undergraduate" in text.lower() else "Graduate" if "graduate" in text.lower() else "Undergraduate",
        "state_restriction": "WA" if "washington" in text.lower() or "wwu" in text.lower() else None,
        "link_notes": f"Discovered from directory {source_domain}; detail page scraped.",
    }


def insert(record):
    inserted = 0
    for db_path in DB_PATHS:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        nh = name_hash(record["scholarship_name"], record["organization"])
        cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
        if cur.fetchone():
            conn.close()
            continue
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO scholarships
            (source, source_id, scholarship_name, organization, organization_type, description,
             eligibility, amount_min, amount_max, amount_display, deadline, application_url,
             website, category, education_level, state_restriction, name_hash, created_at,
             updated_at, link_notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (record["source"], record["source_id"], record["scholarship_name"], record["organization"],
              record["organization_type"], record["description"], record["eligibility"], record["amount_min"],
              record["amount_max"], record["amount_display"], record["deadline"], record["application_url"],
              record["website"], record["category"], record["education_level"], record["state_restriction"],
              nh, now, now, record["link_notes"]))
        conn.commit()
        conn.close()
        inserted += 1
    return inserted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="Directory/index URLs")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    total = 0
    for index_url in args.urls:
        final_url, html = fetch(index_url)
        links = individual_links(final_url, html)[: args.limit]
        print(f"{index_url}: {len(links)} individual links")
        for detail_url, link_text in links:
            try:
                detail_final, detail_html = fetch(detail_url)
                record = parse_detail(detail_final, link_text, detail_html, urlparse(final_url).netloc)
                if not record:
                    continue
                added = insert(record)
                total += added
                print(f"  {'added' if added else 'duplicate'}: {record['scholarship_name'][:90]}")
            except requests.RequestException as exc:
                print(f"  skipped {detail_url}: {exc}")
    print(f"Inserted records across databases: {total}")


if __name__ == "__main__":
    main()
