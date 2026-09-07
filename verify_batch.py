#!/usr/bin/env python3
"""Verify scholarship links with HEAD requests, update url_status in DB."""
import sqlite3, requests, time, sys
from datetime import datetime, timezone

DB = "/home/workspace/scholarsearch/data/processed/scholarships.db"

def verify(url, timeout=8):
    if not url:
        return "no_url", None, None
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code < 400:
            return "ok", r.url, None
        return "inactive", r.url, f"HTTP {r.status_code}"
    except requests.exceptions.Timeout:
        return "inactive", url, "timeout"
    except Exception as e:
        return "inactive", url, str(e)[:80]

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, scholarship_name, application_url FROM scholarships WHERE created_at >= '2026-07-24' AND url_status = 'unchecked'")
    rows = c.fetchall()
    total = len(rows)
    print(f"Verifying {total} unchecked records...")
    verified = 0
    inactive = 0
    no_url = 0
    errors = 0
    for i, (sid, name, url) in enumerate(rows):
        if i % 20 == 0 and i > 0:
            print(f"  ...{i}/{total} done (v={verified}, inv={inactive}, no={no_url})")
            conn.commit()
        if not url:
            no_url += 1
            continue
        status, final_url, reason = verify(url)
        if status == "ok":
            verified += 1
        elif status == "inactive":
            inactive += 1
        else:
            errors += 1
        c.execute("UPDATE scholarships SET url_status=?, last_checked=?, link_notes=? WHERE id=?",
                  (status, datetime.now(timezone.utc).isoformat(), reason or "", sid))
    conn.commit()
    print(f"Done: {verified} ok, {inactive} inactive, {no_url} no-url, {errors} errors out of {total}")
    # Stats
    c.execute("SELECT url_status, COUNT(*) FROM scholarships WHERE created_at >= '2026-07-24' GROUP BY url_status")
    for r in c.fetchall():
        print(f"  {r[0]}: {r[1]}")
    conn.close()

if __name__ == "__main__":
    main()