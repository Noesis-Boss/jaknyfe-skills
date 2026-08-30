"""Safety primitives for ScholarSearch SQLite mutations."""
from __future__ import annotations

import fcntl
import os
import shutil
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path


def _check_database(path: str) -> None:
    p = Path(path)
    if not p.is_file() or p.stat().st_size == 0:
        raise RuntimeError(f"refusing unsafe database: {path}")
    conn = sqlite3.connect(path)
    try:
        result = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if result != "ok":
            raise RuntimeError(f"database integrity check failed for {path}: {result}")
        if conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='scholarships'").fetchone() is None:
            raise RuntimeError(f"missing scholarships table: {path}")
    finally:
        conn.close()


def make_backup(path: str, backup_dir: str | None = None) -> str:
    _check_database(path)
    source = Path(path)
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        conn.close()
    _check_database(path)
    target_dir = Path(backup_dir or source.parent / "discovery-backups")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{source.stem}-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}.db"
    shutil.copy2(source, target)
    _check_database(str(target))
    return str(target)


@contextmanager
def guarded_connection(path: str):
    """Open a validated DB under an exclusive lock and transactional scope."""
    _check_database(path)
    lock_path = f"{path}.lock"
    with open(lock_path, "a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        _check_database(path)
        conn = sqlite3.connect(path, timeout=30)
        conn.execute("PRAGMA busy_timeout=30000")
        conn.execute("PRAGMA journal_mode=WAL")
        try:
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
