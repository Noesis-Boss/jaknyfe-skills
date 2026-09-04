#!/usr/bin/env python3
"""Quick scholarship discovery — inserts scholarships into DBs with link verification."""
import json, sqlite3, hashlib, re, requests, sys
from datetime import datetime, timezone

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

def name_hash(name, org):
    raw = re.sub(r"[^a-z0-9]+", " ", (name or "").lower()).strip() + "||" + re.sub(r"[^a-z0-9]+", " ", (org or "").lower()).strip()
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def verify_link(url, timeout=8):
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "ScholarBot/1.0"})
        if r.status_code == 200:
            return {"ok": True, "final_url": url}
        if r.status_code in (301, 302, 307, 308):
            return {"ok": True, "final_url": r.headers.get("Location", url)}
        return {"ok": False, "reason": f"HTTP {r.status_code}", "final_url": url}
    except Exception as e:
        return {"ok": False, "reason": str(e)[:80], "final_url": url}

def insert_scholarship(s):
    for db_path in DBS:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""INSERT OR IGNORE INTO scholarships (
            source, source_id, scholarship_name, organization, organization_type,
            description, eligibility, amount_min, amount_max, amount_display,
            deadline, application_url, form_url, email, phone, address, website,
            category, education_level, field_of_study, state_restriction,
            gpa_min, citizenship, ethnicity, gender, military_affiliation,
            name_hash, link_notes, url_status)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (s.get("source","web_discovery"), s.get("source_id",""), s.get("scholarship_name",""),
             s.get("organization",""), s.get("organization_type",""), s.get("description",""),
             s.get("eligibility",""), s.get("amount_min"), s.get("amount_max"),
             s.get("amount_display",""), s.get("deadline",""), s.get("application_url",""),
             s.get("form_url",""), s.get("email",""), s.get("phone",""), s.get("address",""),
             s.get("website",""), s.get("category",""), s.get("education_level",""),
             s.get("field_of_study",""), s.get("state_restriction",""), s.get("gpa_min"),
             s.get("citizenship",""), s.get("ethnicity",""), s.get("gender",""),
             s.get("military_affiliation",""), s["name_hash"], s.get("link_notes",""),
             s.get("url_status","unchecked"))
        )
        conn.commit()
        conn.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: quick_discover.py <json_file>")
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        candidates = json.load(f)
    
    added = 0
    skipped_dup = 0
    skipped_link = 0
    failed_links = []
    
    for i, s in enumerate(candidates):
        s["name_hash"] = name_hash(s.get("scholarship_name",""), s.get("organization",""))
        
        dup = False
        for db_path in DBS:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM scholarships WHERE name_hash = ?", (s["name_hash"],))
            if cur.fetchone()[0] > 0:
                dup = True
            conn.close()
            if dup:
                break
        
        if dup:
            skipped_dup += 1
            continue
        
        app_url = s.get("application_url")
        if app_url:
            v = verify_link(app_url)
            if not v["ok"]:
                skipped_link += 1
                s["url_status"] = "inactive"
                s["link_notes"] = v.get("reason","link_failed")
                failed_links.append((s.get("scholarship_name",""), v.get("reason","")))
                s["application_url"] = v.get("final_url", app_url)
            else:
                s["application_url"] = v.get("final_url", app_url)
                s["url_status"] = "active"
        
        insert_scholarship(s)
        added += 1
        
        if (i+1) % 10 == 0:
            print(f"Processed {i+1}/{len(candidates)}: added={added}, dups={skipped_dup}, bad_links={skipped_link}")
    
    print(f"\n=== DONE ===")
    print(f"Added: {added}")
    print(f"Skipped duplicates: {skipped_dup}")
    print(f"Skipped bad links: {skipped_link}")
    if failed_links:
        print(f"\nFailed links:")
        for name, reason in failed_links[:10]:
            print(f"  {name[:50]}: {reason}")

if __name__ == "__main__":
    main()
