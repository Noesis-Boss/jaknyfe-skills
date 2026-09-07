#!/usr/bin/env python3
"""Batch scholarship discovery from web_search results."""
import json, sqlite3, hashlib, re, requests
from datetime import datetime, timezone

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

def name_hash(name, org):
    raw = re.sub(r"[^a-z0-9]+", " ", (name or "").lower().strip()) + "||" + re.sub(r"[^a-z0-9]+", " ", (org or "").lower().strip())
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def is_dup(conn, name, org):
    nh = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

def insert_scholarship(conn, s):
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO scholarships (
            source, source_id, scholarship_name, organization, organization_type,
            description, eligibility, amount_min, amount_max, amount_display,
            deadline, application_url, form_url, email, phone, address, website,
            category, education_level, field_of_study, state_restriction,
            gpa_min, citizenship, ethnicity, gender, military_affiliation,
            name_hash, link_notes, url_status
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        s.get("source", "web_search"),
        s.get("source_id", ""),
        s.get("scholarship_name", ""),
        s.get("organization", ""),
        s.get("organization_type", ""),
        s.get("description", ""),
        s.get("eligibility", ""),
        s.get("amount_min"),
        s.get("amount_max"),
        s.get("amount_display", ""),
        s.get("deadline", ""),
        s.get("application_url", ""),
        s.get("form_url", ""),
        s.get("email", ""),
        s.get("phone", ""),
        s.get("address", ""),
        s.get("website", ""),
        s.get("category", "Academic"),
        s.get("education_level", "Undergraduate"),
        s.get("field_of_study", ""),
        s.get("state_restriction", ""),
        s.get("gpa_min"),
        s.get("citizenship", "None"),
        s.get("ethnicity", ""),
        s.get("gender", ""),
        s.get("military_affiliation", ""),
        name_hash(s.get("scholarship_name", ""), s.get("organization", "")),
        s.get("link_notes", ""),
        s.get("url_status", "unchecked"),
    ))
    conn.commit()
    return cur.lastrowid

def main():
    with open("/home/workspace/quick_candidates.json") as f:
        candidates = json.load(f)

    # Connect to both DBs
    conn_main = sqlite3.connect(DBS[0])
    conn_site = sqlite3.connect(DBS[1])

    added = 0
    skipped_dup = 0
    for s in candidates:
        if is_dup(conn_main, s.get("scholarship_name", ""), s.get("organization", "")):
            skipped_dup += 1
            continue
        s.setdefault("source_id", f"web_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{added:03d}")
        s.setdefault("scholarship_name", s.get("title", "Unnamed"))
        s.setdefault("organization", s.get("provider", "Unknown"))
        s.setdefault("category", "Academic")
        s.setdefault("education_level", "Undergraduate")
        s.setdefault("source", "web_search")
        try:
            insert_scholarship(conn_main, s)
            insert_scholarship(conn_site, s)
            added += 1
        except Exception as e:
            print(f"  ERROR: {s.get('scholarship_name','?')}: {e}")
        if added % 50 == 0:
            print(f"  ... {added} inserted so far")

    conn_main.close()
    conn_site.close()

    print(f"\n=== Results ===")
    print(f"Added: {added}")
    print(f"Skipped (dup): {skipped_dup}")
    print(f"Total candidates examined: {len(candidates)}")

if __name__ == "__main__":
    main()