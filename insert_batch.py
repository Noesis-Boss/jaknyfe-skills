import sqlite3
import json
import hashlib
from datetime import datetime, timezone

DB_PATHS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

def name_hash(name, org):
    raw = f"{(name or '').strip().lower()}|{(org or '').strip().lower()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def main():
    with open("/home/workspace/scholarship_batch.json") as f:
        scholarships = json.load(f)

    today = datetime.now(timezone.utc).date().isoformat()
    added = 0
    skipped_dup = 0
    errors = 0

    for s in scholarships:
        s["name_hash"] = name_hash(s.get("scholarship_name", ""), s.get("organization", ""))
        s["created_at"] = today
        s["updated_at"] = today
        s.setdefault("active", 1)
        s.setdefault("link_notes", "")

        for db_path in DB_PATHS:
            conn = sqlite3.connect(db_path)
            try:
                cur = conn.cursor()
                cur.execute("SELECT id FROM scholarships WHERE source=? AND source_id=?", (s.get("source"), s.get("source_id")))
                if cur.fetchone():
                    skipped_dup += 1
                    continue

                cur.execute("""INSERT INTO scholarships (
                    source, source_id, scholarship_name, organization, organization_type,
                    description, eligibility, amount_min, amount_max, amount_display,
                    deadline, application_url, form_url, email, phone, address, website,
                    category, education_level, field_of_study, state_restriction,
                    gpa_min, citizenship, ethnicity, gender, military_affiliation,
                    name_hash, created_at, updated_at, link_notes, active
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                    s.get("source", "global_discovery"),
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
                    s["name_hash"],
                    s["created_at"],
                    s["updated_at"],
                    s.get("link_notes", ""),
                    1,
                ))
                conn.commit()
                added += 1
            except Exception as e:
                errors += 1
                print(f"ERROR: {str(e)[:100]} | {s.get('scholarship_name','')[:40]}")
            finally:
                conn.close()

    print(f"Added: {added} (to both DBs)")
    print(f"Skipped duplicates: {skipped_dup}")
    print(f"Errors: {errors}")
    print(f"Total in batch: {len(scholarships)}")

if __name__ == "__main__":
    main()
