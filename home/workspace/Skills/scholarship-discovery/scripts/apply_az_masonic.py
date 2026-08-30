#!/usr/bin/env python3
"""Apply Arizona Masonic scholarship discovery to a given scholarships DB.

Idempotent: enriches known existing AZ Masonic rows and inserts new real
scholarships found via web research (June 2026). Run for both the working
DB and the live site DB so they stay consistent.
"""
import sqlite3
import sys
from datetime import datetime


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def apply(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    ts = now()
    added = 0
    updated = 0

    # 1) Enrich the existing Grand Lodge of Arizona / Masonic Charities entry
    cur.execute(
        "SELECT id FROM scholarships WHERE scholarship_name='Arizona Masonic Charities Scholarship'"
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE scholarships SET
                organization='Masonic Charities of Arizona / Grand Lodge of Free & Accepted Masons of Arizona',
                organization_type='Masonic Organization',
                description='Arizona Grand Lodge scholarship administered by Masonic Charities of Arizona and the Order of the Eastern Star (OES). Open to Arizona students; eligibility and award amounts set per the Masonic Charities / OES application process.',
                eligibility='Arizona residents. Apply via Masonic Charities of Arizona and/or the Order of the Eastern Star (OES) respective application processes.',
                amount_display='Varies (contact Masonic Charities of Arizona)',
                deadline='June 18 (postmarked)',
                application_url='https://www.phoenixritecare.org/grand-lodge-scholarship',
                website='https://www.masoniccharitiesaz.com/',
                email='Grants@MasonicCharitiesAZ.com',
                state_restriction='AZ',
                category='undergraduate',
                education_level='Undergraduate',
                url_status='active',
                updated_at=?
            WHERE id=?
            """,
            (ts, row["id"]),
        )
        updated += 1

    # 2) Enrich the Arizona Eastern Star (OES) entry
    cur.execute(
        "SELECT id FROM scholarships WHERE scholarship_name='Arizona Eastern Star Scholarship'"
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE scholarships SET
                organization_type='Masonic (Order of the Eastern Star)',
                description='Scholarship from the Order of the Eastern Star, Grand Chapter of Arizona, administered alongside Masonic Charities of Arizona.',
                eligibility='Arizona residents; apply via the Order of the Eastern Star (OES) application process coordinated with Masonic Charities of Arizona.',
                amount_display='Varies (contact Masonic Charities of Arizona)',
                deadline='June 18 (postmarked)',
                application_url='https://www.phoenixritecare.org/grand-lodge-scholarship',
                website='https://www.masoniccharitiesaz.com/',
                email='Grants@MasonicCharitiesAZ.com',
                state_restriction='AZ',
                category='undergraduate',
                education_level='Undergraduate',
                url_status='active',
                updated_at=?
            WHERE id=?
            """,
            (ts, row["id"]),
        )
        updated += 1

    # 3) Enrich the Castellano (Glendale Lodge #23) entry
    cur.execute(
        "SELECT id FROM scholarships WHERE scholarship_name LIKE 'Robert William Castellano%' OR scholarship_name='Castellano Scholarship'"
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE scholarships SET
                scholarship_name='Robert William Castellano Scholarship Fund',
                organization='Glendale Lodge #23 F&AM',
                organization_type='Masonic Lodge',
                description='Established by bequest from Brother Robert W. Castellano (d. 2002). Provides scholarships for deserving young men and women to attend any accredited educational institution in the country. Renewable for up to 4 years.',
                eligibility='Deserving students with high ideals, ability, and strong academic performance. Open to any student (no Masonic affiliation required).',
                amount_min=5000,
                amount_max=5000,
                amount_display='Up to $5,000 per school year (renewable up to 4 years)',
                deadline='Annual (check site for current cycle)',
                application_url='https://www.glendaleaz23.com/castellano-scholarship',
                form_url='http://www.glendaleaz23.com/wp-content/uploads/2025/11/CastellanoApplication06-25.doc',
                phone='623-937-0782',
                address='6831 N. 58th Ave, Glendale, AZ 85301',
                website='https://www.glendaleaz23.com',
                state_restriction='AZ',
                category='undergraduate',
                education_level='Undergraduate',
                url_status='active',
                updated_at=?
            WHERE id=?
            """,
            (ts, row["id"]),
        )
        updated += 1

    # 4) Insert genuinely new real AZ Masonic scholarships (dedup by name+org)
    new_scholarships = [
        {
            "source": "az_masonic_discovery",
            "source_id": "az_masonic_flagstaff7",
            "scholarship_name": "H. Gordon Beckley, Jack O'Hara & Ray Hirni Memorial Scholarship",
            "organization": "Flagstaff Lodge No. 7, F&AM",
            "organization_type": "Masonic Lodge",
            "description": "Memorial scholarship from Flagstaff Lodge No. 7, Free & Accepted Masons of Arizona, recognizing the value of higher education.",
            "eligibility": "Members in good standing of Flagstaff Masonic Lodge No. 7 or Grand Canyon OES Chapter No. 4, their children, and grandchildren. Must be admitted/enrolled in an accredited institution of higher learning. Minimum 2.5 GPA.",
            "amount_min": None,
            "amount_max": None,
            "amount_display": "Varies (contact lodge)",
            "deadline": "April 15 (received in lodge)",
            "application_url": "https://flagstaff7.org/",
            "form_url": "https://flagstaff7.org/wp-content/uploads/2021/12/Scholarship-Application-2022-2023.pdf",
            "email": "inquiry@flagstaff7.org",
            "phone": "(928) 833-1888",
            "address": "107 E Birch Ave, Flagstaff, AZ 86001",
            "website": "https://flagstaff7.org",
            "category": "undergraduate",
            "education_level": "Undergraduate",
            "state_restriction": "AZ",
            "gpa_min": 2.5,
        },
        {
            "source": "az_masonic_discovery",
            "source_id": "az_masonic_phxrite",
            "scholarship_name": "Phoenix Scottish Rite Foundation Arizona Scholarship",
            "organization": "Phoenix Scottish Rite Foundation, Inc.",
            "organization_type": "Masonic (Scottish Rite)",
            "description": "Partial scholarships for Arizona students administered by the Phoenix Scottish Rite Foundation (Rite Care). No Masonic affiliation required.",
            "eligibility": "Arizona students; no Masonic affiliation required.",
            "amount_min": None,
            "amount_max": None,
            "amount_display": "Partial scholarship (varies)",
            "deadline": "Varies (check site)",
            "application_url": "https://www.phoenixritecare.org/",
            "form_url": "",
            "email": "",
            "phone": "",
            "address": "",
            "website": "https://www.phoenixritecare.org",
            "category": "undergraduate",
            "education_level": "Undergraduate",
            "state_restriction": "AZ",
            "gpa_min": None,
        },
    ]

    for s in new_scholarships:
        cur.execute(
            "SELECT id FROM scholarships WHERE scholarship_name=? AND organization=?",
            (s["scholarship_name"], s["organization"]),
        )
        if cur.fetchone():
            continue
        cur.execute(
            """
            INSERT INTO scholarships (
                source, source_id, scholarship_name, organization, organization_type,
                description, eligibility, amount_min, amount_max, amount_display,
                deadline, application_url, form_url, email, phone, address, website,
                category, education_level, state_restriction, gpa_min, url_status, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'active', ?, ?)
            """,
            (
                s["source"], s["source_id"], s["scholarship_name"], s["organization"],
                s["organization_type"], s["description"], s["eligibility"], s["amount_min"],
                s["amount_max"], s["amount_display"], s["deadline"], s["application_url"],
                s["form_url"], s["email"], s["phone"], s["address"], s["website"],
                s["category"], s["education_level"], s["state_restriction"], s["gpa_min"],
                ts, ts,
            ),
        )
        added += 1

    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    conn.close()
    print(f"[{db_path}] Added: {added} | Updated: {updated} | Total: {total}")


if __name__ == "__main__":
    dbs = sys.argv[1:] or [
        "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
        "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
    ]
    for db in dbs:
        apply(db)
