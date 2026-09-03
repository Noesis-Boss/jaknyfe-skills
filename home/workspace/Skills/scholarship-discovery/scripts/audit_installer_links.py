"""Fail-closed audit for installer URLs in active scholarship listings."""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from db_safety import guarded_connection, make_backup
from verification import is_installer_url

DEFAULT_DATABASES = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]


def audit_database(path: str, commit: bool) -> dict:
    rows = []
    with sqlite3.connect(path) as conn:
        rows = conn.execute(
            "SELECT id, scholarship_name, application_url, form_url FROM scholarships WHERE active=1"
        ).fetchall()
    bad = [r for r in rows if is_installer_url(r[2] or "") or is_installer_url(r[3] or "")]
    changed = 0
    backup = None
    if commit and bad:
        backup = make_backup(path)
        with guarded_connection(path) as conn:
            for row in bad:
                conn.execute(
                    "UPDATE scholarships SET active=0, url_status='rejected', last_status='installer_url', last_checked=? WHERE id=?",
                    (datetime.now(timezone.utc).isoformat(), row[0]),
                )
                changed += 1
    return {"database": path, "active_before": len(rows), "installer_rows": len(bad), "deactivated": changed, "backup": backup}


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit active listings for App Store, Play Store, and binary installer URLs.")
    parser.add_argument("--database", action="append", dest="databases")
    parser.add_argument("--commit", action="store_true", help="deactivate confirmed installer rows")
    args = parser.parse_args()
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "commit": args.commit,
              "results": [audit_database(p, args.commit) for p in (args.databases or DEFAULT_DATABASES)]}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
