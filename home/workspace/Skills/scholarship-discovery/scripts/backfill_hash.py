#!/usr/bin/env python3
import sqlite3, hashlib

DBS = [
    '/home/workspace/scholarsearch-site/data/processed/scholarships.db',
    '/home/workspace/scholarsearch-site/data/processed/scholarships.db',
]

def name_hash(name, org=''):
    key = f"{name}|{org or ''}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]

for db in DBS:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE scholarships ADD COLUMN name_hash TEXT')
    except Exception:
        pass
    rows = c.execute('SELECT id, scholarship_name, organization FROM scholarships').fetchall()
    updates = []
    for rid, name, org in rows:
        updates.append((name_hash(name, org), rid))
    c.executemany('UPDATE scholarships SET name_hash=? WHERE id=?', updates)
    conn.commit(); conn.close()
    print('backfilled', db)