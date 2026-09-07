#!/usr/bin/env python3
"""Gather scholarships from web search results and insert into both DBs."""
import json, sqlite3, hashlib, re
from datetime import datetime, timezone

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

def normalize(text):
    if not text: return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def name_hash(name, org):
    raw = normalize(name) + "||" + normalize(org)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def is_dup(conn, name, org):
    h = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (h,))
    return cur.fetchone() is not None

def insert_scholarship(conn, s):
    cur = conn.cursor()
    cur.execute("""INSERT INTO scholarships (
        source, source_id, scholarship_name, organization, organization_type,
        description, eligibility, amount_min, amount_max, amount_display,
        deadline, application_url, form_url, email, phone, address, website,
        category, education_level, field_of_study, state_restriction,
        gpa_min, citizenship, ethnicity, gender, military_affiliation,
        name_hash, link_notes, url_status, active, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (s.get('source','web_search'), s.get('source_id',''), s.get('scholarship_name',''),
         s.get('organization',''), '', s.get('description',''), s.get('eligibility',''),
         s.get('amount_min'), s.get('amount_max'), s.get('amount_display',''),
         s.get('deadline',''), s.get('application_url',''), s.get('form_url',''),
         '', '', '', '', s.get('category','Academic'), s.get('education_level','Undergraduate'),
         s.get('field_of_study',''), s.get('state_restriction',''), None,
         s.get('citizenship','None'), '', '', '',
         name_hash(s.get('scholarship_name',''), s.get('organization','')),
         '', 'unchecked', 1,
         datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
         datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

# Load candidates from quick_candidates.json
with open('/home/workspace/quick_candidates.json') as f:
    candidates = json.load(f)

new_count = 0
dup_count = 0

for db_path in DBS:
    conn = sqlite3.connect(db_path)
    for c in candidates:
        if not is_dup(conn, c.get('scholarship_name',''), c.get('organization','')):
            insert_scholarship(conn, c)
            new_count += 1
        else:
            dup_count += 1
    conn.close()

print(f"Inserted {new_count} new scholarships across both DBs ({dup_count} duplicates skipped)")
