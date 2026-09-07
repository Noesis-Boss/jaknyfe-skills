#!/usr/bin/env python3
"""Targeted scholarship discovery using web search results."""
import json, sys, os, re, hashlib, sqlite3, time
from datetime import datetime, timezone

sys.path.insert(0, "/home/workspace/Skills/scholarship-discovery/scripts")
from discover import normalize, name_hash, clean_num, verify_link, is_dup, add_scholarship, get_db_connection, DBS

CANDIDATES_FILE = "/home/workspace/scholarship_candidates.json"

def load_candidates(path):
    with open(path) as f:
        return json.load(f)

def dedup_by_name_hash(scholarships, db_conn):
    """Remove scholarships that already exist in DB by name_hash."""
    cur = db_conn.cursor()
    cur.execute("SELECT name_hash FROM scholarships")
    existing_hashes = set(r[0] for r in cur.fetchall())
    cur.close()
    result = []
    for s in scholarships:
        h = name_hash(s.get("scholarship_name", ""), s.get("organization", ""))
        if h not in existing_hashes:
            result.append(s)
    return result

def main():
    candidates = load_candidates(CANDIDATES_FILE)
    print(f"Loaded {len(candidates)} candidates from JSON")

    # Dedup against DB
    conn = get_db_connection(DBS[0])
    unique = dedup_by_name_hash(candidates, conn)
    conn.close()
    print(f"After DB dedup: {len(unique)} unique scholarships")

    # Verify links and insert
    added = 0
    skipped_link = 0
    skipped_dup = 0
    errors = []

    for s in unique:
        app_url = s.get("application_url") or s.get("form_url") or s.get("website")
        if app_url:
            v = verify_link(app_url)
            if not v["ok"]:
                s["status"] = "inactive"
                s["link_notes"] = v.get("reason", "link_failed")
                if v.get("final_url"):
                    s["application_url"] = v["final_url"]
                    s["website"] = v["final_url"]
                skipped_link += 1
                # Still insert inactive ones
                s.setdefault("source_id", s.get("source_id", f"web_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{added}"))

        conn = get_db_connection(DBS[0])
        if is_dup(conn, s):
            skipped_dup += 1
            conn.close()
            continue

        s.setdefault("scholarship_name", s.get("title", "Unnamed Scholarship"))
        s.setdefault("organization", s.get("provider", "Unknown"))
        s.setdefault("category", s.get("category", "Academic"))
        s.setdefault("education_level", s.get("education_level", "Undergraduate"))
        s.setdefault("source", s.get("source", "web_search"))

        try:
            add_scholarship(conn, s)
            added += 1
        except Exception as e:
            errors.append(f"{s.get('scholarship_name','?')}: {e}")
        finally:
            conn.close()

        if added % 10 == 0 and added > 0:
            print(f"  ... {added} inserted so far")

    print(f"\n=== Results ===")
    print(f"Added: {added}")
    print(f"Skipped (dup): {skipped_dup}")
    print(f"Skipped (link): {skipped_link}")
    print(f"Errors: {len(errors)}")
    for e in errors[:5]:
        print(f"  - {e}")

if __name__ == "__main__":
    main()