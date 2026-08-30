#!/usr/bin/env python3
"""Focused discovery: Arizona Masonic-related scholarships.

Adds/updates real Arizona Masonic scholarships sourced from web research
(Grand Lodge of Arizona / Masonic Charities of Arizona, Phoenix Rite Care
Foundation / Scottish Rite, local lodges such as Glendale #23 and Flagstaff #7).
Run: python3 discover_az_masonic.py
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"

# Scholarship records discovered via web search (2026-07-10).
# Each record: (scholarship_name, organization, organization_type, description,
# eligibility, amount_min, amount_max, amount_display, deadline, application_url,
# form_url, email, phone, address, website, category, state_restriction, gpa_min)
SCHOLARSHIPS = [
    (
        "Arizona Grand Lodge Scholarship (Masonic Charities of Arizona)",
        "Masonic Charities of Arizona / Grand Lodge of Free & Accepted Masons of Arizona",
        "Masonic Organization",
        "Scholarship for Arizona students administered by Masonic Charities of Arizona "
        "and the Order of the Eastern Star. Apply through Masonic Charities of Arizona "
        "(or OES) for their respective application process. No Masonic affiliation "
        "required to apply through the charities programs.",
        "Arizona resident student; contact Masonic Charities of Arizona or Order of the "
        "Eastern Star for the specific application process and eligibility.",
        None, None, "Varies (contact for details)",
        "June 18 (postmarked)",
        "https://www.phoenixritecare.org/grand-lodge-scholarship",
        "https://www.masoniccharitiesaz.com/",
        "Grants@MasonicCharitiesAZ.com", "",
        "Kingman Lodge No. 22, 212 N. 4th Street Ste. 4, Kingman, AZ 86401",
        "https://www.masoniccharitiesaz.com/",
        "undergraduate", "AZ", None,
    ),
    (
        "H. Gordon Beckley, Jack O'Hara & Ray Hirni Memorial Scholarship",
        "Flagstaff Lodge No. 7, F&AM",
        "Masonic Lodge",
        "Memorial scholarship from Flagstaff Lodge No. 7, Free & Accepted Masons of "
        "Arizona, recognizing the value of higher education. Awarded per academic year, "
        "payable in advance of the semester of enrollment.",
        "Members in good standing of Flagstaff Masonic Lodge No. 7 or Grand Canyon OES "
        "Chapter No. 4, their children, and grandchildren. Must be admitted or enrolled "
        "in an accredited institution of higher learning. Minimum 2.5 cumulative GPA.",
        None, None, "Varies (contact lodge)",
        "April 15 (received in lodge)",
        "https://flagstaff7.org/",
        "https://flagstaff7.org/wp-content/uploads/2021/12/Scholarship-Application-2022-2023.pdf",
        "inquiry@flagstaff7.org", "(928) 833-1888",
        "107 E Birch Ave, Flagstaff, AZ 86001",
        "https://flagstaff7.org",
        "undergraduate", "AZ", 2.5,
    ),
    (
        "Phoenix Scottish Rite Foundation Arizona Scholarship",
        "Phoenix Scottish Rite Foundation, Inc.",
        "Masonic (Scottish Rite)",
        "Partial scholarships for Arizona students offered through the Phoenix Scottish "
        "Rite Foundation / Rite Care. No Masonic affiliation needed.",
        "Arizona students; no Masonic affiliation required.",
        None, None, "Partial scholarship (varies)",
        "Varies (check website)",
        "https://www.phoenixritecare.org/",
        "", "", "",
        "Phoenix, AZ",
        "https://www.phoenixritecare.org",
        "undergraduate", "AZ", None,
    ),
]


def get_conn():
    return sqlite3.connect(DB_PATH)


def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def upsert(conn):
    cur = conn.cursor()
    added = 0
    updated = 0
    for rec in SCHOLARSHIPS:
        name = rec[0]
        cur.execute(
            "SELECT id FROM scholarships WHERE scholarship_name = ? AND organization = ?",
            (name, rec[1]),
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                """
                UPDATE scholarships SET
                    organization_type = ?,
                    description = ?,
                    eligibility = ?,
                    amount_min = ?,
                    amount_max = ?,
                    amount_display = ?,
                    deadline = ?,
                    application_url = ?,
                    form_url = ?,
                    email = ?,
                    phone = ?,
                    address = ?,
                    website = ?,
                    category = ?,
                    state_restriction = ?,
                    gpa_min = ?,
                    updated_at = ?,
                    url_status = 'active'
                WHERE id = ?
                """,
                (
                    rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8],
                    rec[9], rec[10], rec[11], rec[12], rec[13], rec[14],
                    rec[15], rec[16], rec[17], now(), row[0],
                ),
            )
            updated += 1
        else:
            cur.execute(
                """
                INSERT INTO scholarships (
                    source, source_id, scholarship_name, organization, organization_type,
                    description, eligibility, amount_min, amount_max, amount_display,
                    deadline, application_url, form_url, email, phone, address, website,
                    category, education_level, state_restriction, gpa_min,
                    created_at, updated_at, url_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "az_masonic_discovery",
                    f"az_masonic_{now()}",
                    name, rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7],
                    rec[8], rec[9], rec[10], rec[11], rec[12], rec[13], rec[14],
                    rec[15], "Undergraduate", rec[16], rec[17],
                    now(), now(), "active",
                ),
            )
            added += 1
    conn.commit()
    return added, updated


def main():
    if not os.path.exists(DB_PATH):
        print(f"DB not found: {DB_PATH}")
        return
    conn = get_conn()
    before = conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    added, updated = upsert(conn)
    after = conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    conn.close()
    print(f"AZ Masonic discovery complete.")
    print(f"Added: {added} | Updated: {updated}")
    print(f"Total scholarships: {before} -> {after}")


if __name__ == "__main__":
    main()
