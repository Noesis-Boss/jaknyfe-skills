#!/usr/bin/env python3
"""Hermes AgentOS Mission Control Dashboard backend.

Python stdlib only. Read-only SQLite access to Hermes data sources.
Read-write SQLite for the personal operator task board (board.db).

Single-file server: ThreadingHTTPServer on 127.0.0.1:51763.
Serves /, /api/snapshot, /events (SSE), /api/board (CRUD).
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HOST = "127.0.0.1"
PORT = 51763
HERMES_HOME = os.environ.get("HERMES_HOME", "/root/.hermes")
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DB_PATH = os.path.join(PROJECT_DIR, "board.db")
INDEX_HTML_PATH = os.path.join(PROJECT_DIR, "index.html")

GATEWAY_STATE_PATH = os.path.join(HERMES_HOME, "gateway_state.json")
AGENT_LOGS_DB_PATH = os.path.join(HERMES_HOME, "agent-logs.db")
STATE_DB_PATH = os.path.join(HERMES_HOME, "state.db")
KANBAN_DB_PATH = os.path.join(HERMES_HOME, "kanban.db")

CRON_PATHS = [
    ("/var/spool/cron/crontabs/root", "user", False),
    ("/etc/crontab", "system", True),
    ("/etc/cron.d/", "system", True),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe(fn, default=None):
    try:
        return fn()
    except Exception as e:  # noqa: BLE001
        return {"error": str(e), **({} if default is None else {"value": default})}


def open_readonly(db_path: str) -> sqlite3.Connection:
    """Open a SQLite database in read-only mode with query_only=1."""
    uri = f"file:{db_path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only=1")
    return conn


def row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


# ---------------------------------------------------------------------------
# Data functions
# ---------------------------------------------------------------------------


def gateway_data() -> dict:
    if not os.path.exists(GATEWAY_STATE_PATH):
        return {"state": "unknown", "platforms": {}, "active_agents": 0, "uptime_seconds": None}

    with open(GATEWAY_STATE_PATH, "r") as f:
        data = json.load(f)

    start_time = data.get("start_time")
    uptime = None
    if isinstance(start_time, (int, float)):
        # start_time may be a process counter (e.g. boot-relative), not Unix
        # seconds. Only treat it as a Unix epoch if it looks like one
        # (i.e. is large enough to be after 2001).
        if float(start_time) > 1_000_000_000:
            uptime = max(0, int(time.time() - float(start_time)))
        else:
            # Fall back to the PID's actual start time in /proc
            pid = data.get("pid")
            if pid and os.path.exists(f"/proc/{pid}"):
                try:
                    with open(f"/proc/{pid}/stat", "r") as pf:
                        parts = pf.read().split()
                    # field 22 is starttime in clock ticks since boot
                    clk_tck = os.sysconf("SC_CLK_TCK")
                    with open("/proc/stat", "r") as sf:
                        btime = 0
                        for ln in sf:
                            if ln.startswith("btime "):
                                btime = int(ln.split()[1])
                                break
                    if btime:
                        started = btime + int(parts[21]) / clk_tck
                        uptime = max(0, int(time.time() - started))
                except Exception:
                    pass

    return {
        "state": data.get("gateway_state", "unknown"),
        "platforms": data.get("platforms", {}),
        "active_agents": data.get("active_agents", 0),
        "pid": data.get("pid"),
        "argv": data.get("argv"),
        "start_time": start_time,
        "uptime_seconds": uptime,
        "restart_requested": data.get("restart_requested", False),
        "updated_at": data.get("updated_at"),
    }


def activity_data() -> dict:
    if not os.path.exists(AGENT_LOGS_DB_PATH):
        return {
            "recent": [],
            "per_agent": {},
            "totals": {"total": 0, "completed": 0, "failed": 0},
            "daily_7d": [],
        }

    conn = open_readonly(AGENT_LOGS_DB_PATH)
    try:
        cur = conn.cursor()

        # Recent 50
        cur.execute(
            "SELECT id, agent_name, task_description, model_used, status, created_at "
            "FROM agent_logs ORDER BY created_at DESC, id DESC LIMIT 50"
        )
        recent = [row_to_dict(r) for r in cur.fetchall()]

        # Per-agent stats
        cur.execute(
            "SELECT agent_name, COUNT(*) AS total, "
            "SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) AS completed, "
            "SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed, "
            "MAX(created_at) AS last_seen "
            "FROM agent_logs GROUP BY agent_name"
        )
        per_agent_raw = [row_to_dict(r) for r in cur.fetchall()]

        cur.execute(
            "SELECT agent_name, task_description, created_at FROM agent_logs al "
            "WHERE id IN (SELECT id FROM agent_logs al2 "
            "  WHERE al2.agent_name = al.agent_name "
            "  ORDER BY created_at DESC, id DESC LIMIT 1)"
        )
        last_tasks = {r["agent_name"]: {"task": r["task_description"], "at": r["created_at"]}
                      for r in cur.fetchall()}

        cur.execute(
            "SELECT agent_name, model_used, COUNT(*) c FROM agent_logs "
            "WHERE model_used IS NOT NULL AND model_used != '' "
            "GROUP BY agent_name, model_used ORDER BY agent_name, c DESC"
        )
        model_rows = list(cur.fetchall())
        models_by_agent: dict[str, str] = {}
        for r in model_rows:
            if r["agent_name"] not in models_by_agent:
                models_by_agent[r["agent_name"]] = r["model_used"]

        per_agent: dict[str, dict] = {}
        for r in per_agent_raw:
            per_agent[r["agent_name"]] = {
                "total": r["total"] or 0,
                "completed": r["completed"] or 0,
                "failed": r["failed"] or 0,
                "last_seen": r["last_seen"],
                "last_task": (last_tasks.get(r["agent_name"], {}) or {}).get("task"),
                "model": models_by_agent.get(r["agent_name"]),
            }

        # Overall totals
        cur.execute("SELECT COUNT(*) total FROM agent_logs")
        total = cur.fetchone()["total"] or 0
        cur.execute("SELECT COUNT(*) c FROM agent_logs WHERE status='completed'")
        completed = cur.fetchone()["c"] or 0
        cur.execute("SELECT COUNT(*) c FROM agent_logs WHERE status='failed'")
        failed = cur.fetchone()["c"] or 0

        # 7-day daily breakdown
        cur.execute(
            "SELECT substr(created_at,1,10) AS day, COUNT(*) c "
            "FROM agent_logs "
            "WHERE created_at >= datetime('now','-7 days') "
            "GROUP BY day ORDER BY day ASC"
        )
        daily_7d = [{"day": r["day"], "count": r["c"]} for r in cur.fetchall()]

        return {
            "recent": recent,
            "per_agent": per_agent,
            "totals": {"total": total, "completed": completed, "failed": failed},
            "daily_7d": daily_7d,
        }
    finally:
        conn.close()


def sessions_data() -> dict:
    if not os.path.exists(STATE_DB_PATH):
        return {"session_count": 0, "message_count": 0, "tokens": {}, "recent": []}

    conn = open_readonly(STATE_DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) c FROM sessions")
        session_count = cur.fetchone()["c"] or 0

        cur.execute(
            "SELECT COALESCE(SUM(message_count),0) m, "
            "COALESCE(SUM(input_tokens),0) i, "
            "COALESCE(SUM(output_tokens),0) o, "
            "COALESCE(SUM(cache_read_tokens),0) cr, "
            "COALESCE(SUM(cache_write_tokens),0) cw "
            "FROM sessions"
        )
        r = cur.fetchone()
        tokens = {
            "input": r["i"] or 0,
            "output": r["o"] or 0,
            "cache_read": r["cr"] or 0,
            "cache_write": r["cw"] or 0,
        }

        cur.execute(
            "SELECT id, source, model, started_at, ended_at, "
            "message_count, input_tokens, output_tokens "
            "FROM sessions ORDER BY started_at DESC LIMIT 25"
        )
        recent = []
        for row in cur.fetchall():
            d = row_to_dict(row)
            # timestamps are Unix float seconds — pass through as-is
            recent.append(d)

        return {
            "session_count": session_count,
            "message_count": r["m"] or 0,
            "tokens": tokens,
            "recent": recent,
        }
    finally:
        conn.close()


def vps_health() -> dict:
    # CPU: two /proc/stat samples
    def read_cpu():
        with open("/proc/stat", "r") as f:
            line = f.readline()
        parts = line.split()
        nums = [int(x) for x in parts[1:]]
        idle = nums[3] + (nums[4] if len(nums) > 4 else 0)
        total = sum(nums)
        return idle, total

    cpu_pct = None
    try:
        idle1, total1 = read_cpu()
        time.sleep(0.2)
        idle2, total2 = read_cpu()
        dt = total2 - total1
        cpu_pct = round((1.0 - (idle2 - idle1) / dt) * 100, 1) if dt > 0 else None
    except Exception:
        pass

    # RAM
    ram = {"total_mb": None, "available_mb": None, "used_pct": None}
    try:
        info = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                k, _, v = line.partition(":")
                info[k.strip()] = v.strip()
        total_kb = int(info.get("MemTotal", "0").split()[0])
        avail_kb = int(info.get("MemAvailable", "0").split()[0])
        ram["total_mb"] = round(total_kb / 1024, 1)
        ram["available_mb"] = round(avail_kb / 1024, 1)
        if total_kb:
            ram["used_pct"] = round((1 - avail_kb / total_kb) * 100, 1)
    except Exception:
        pass

    # Disk
    disk = {"path": "/", "total_gb": None, "used_gb": None, "used_pct": None}
    try:
        st = os.statvfs("/")
        total = st.f_blocks * st.f_frsize
        free = st.f_bfree * st.f_frsize
        used = total - free
        disk["total_gb"] = round(total / 1024 ** 3, 2)
        disk["used_gb"] = round(used / 1024 ** 3, 2)
        disk["used_pct"] = round(used / total * 100, 1) if total else None
    except Exception:
        pass

    # Load average
    load = None
    try:
        with open("/proc/loadavg", "r") as f:
            parts = f.read().split()
        load = {"1m": float(parts[0]), "5m": float(parts[1]), "15m": float(parts[2])}
    except Exception:
        pass

    # Uptime
    up_sec = None
    try:
        with open("/proc/uptime", "r") as f:
            up_sec = int(float(f.read().split()[0]))
    except Exception:
        pass

    return {"cpu_pct": cpu_pct, "ram": ram, "disk": disk, "load": load, "uptime_seconds": up_sec}


def _parse_cron_line(line: str, strip_user: bool):
    """Parse a single crontab line into schedule + command. Returns dict or None."""
    line = line.rstrip("\n")
    if not line.strip() or line.strip().startswith("#"):
        return None
    # Skip env / variable assignments
    if re.match(r"^[A-Z_][A-Z0-9_]*\s*=", line):
        return None

    parts = line.split()
    if len(parts) < 6:
        return None

    if strip_user and parts[0] != "*" and not parts[0].startswith("@"):
        # First field is username in system files
        parts = parts[1:]

    schedule_parts = parts[:5]
    command = " ".join(parts[5:])

    # Handle shortcuts
    shortcuts = {
        "@reboot": "at reboot",
        "@hourly": "0 * * * *",
        "@daily": "0 0 * * *",
        "@midnight": "0 0 * * *",
        "@weekly": "0 0 * * 0",
        "@monthly": "0 0 1 * *",
        "@yearly": "0 0 1 1 *",
        "@annually": "0 0 1 1 *",
    }
    if schedule_parts[0] in shortcuts:
        schedule = shortcuts[schedule_parts[0]]
        return {"schedule_raw": " ".join(schedule_parts), "schedule_english": shortcuts[schedule_parts[0]],
                "command": command}

    schedule = " ".join(schedule_parts)
    english = _cron_to_english(schedule_parts)
    return {"schedule_raw": schedule, "schedule_english": english, "command": command}


def _cron_to_english(parts) -> str:
    minute, hour, dom, month, dow = parts

    if minute.startswith('*/') and hour == dom == month == dow == '*':
        return f"every {minute[2:]} minutes"
    if minute == '0' and hour.startswith('*/') and dom == month == dow == '*':
        return f"every {hour[2:]} hours at minute 0"
    if minute == hour == dom == month == dow == '*':
        return 'every minute'

    def simple(v: str, label: str) -> str:
        if v == '*':
            return ''
        if v.isdigit():
            return f"{label} {v}"
        return f"{label} {v}"

    bits = []
    if minute != '*':
        bits.append(simple(minute, 'minute'))
    if hour != '*':
        bits.append(simple(hour, 'hour'))
    if dom != '*':
        bits.append(simple(dom, 'day'))
    if month != '*':
        bits.append(simple(month, 'month'))
    if dow != '*':
        bits.append(simple(dow, 'weekday'))
    return ' '.join(bits) if bits else 'manual'


def cron_jobs() -> list:
    jobs = []
    for path, label, strip_user in CRON_PATHS:
        if os.path.isdir(path):
            try:
                for entry in sorted(os.listdir(path)):
                    fp = os.path.join(path, entry)
                    if not os.path.isfile(fp):
                        continue
                    try:
                        with open(fp, "r") as f:
                            for line in f:
                                parsed = _parse_cron_line(line, strip_user)
                                if parsed:
                                    parsed["source"] = entry
                                    parsed["origin"] = label
                                    jobs.append(parsed)
                    except Exception:
                        continue
            except Exception:
                continue
        elif os.path.isfile(path):
            try:
                with open(path, "r") as f:
                    for line in f:
                        parsed = _parse_cron_line(line, strip_user)
                        if parsed:
                            parsed["source"] = os.path.basename(path)
                            parsed["origin"] = label
                            jobs.append(parsed)
            except Exception:
                continue
    return jobs


def snapshot() -> dict:
    return {
        "generated_at": utcnow_iso(),
        "hermes_home": HERMES_HOME,
        "gateway": safe(gateway_data, {"state": "error"}),
        "activity": safe(activity_data, {"recent": [], "per_agent": {}, "totals": {}, "daily_7d": []}),
        "sessions": safe(sessions_data, {"session_count": 0, "message_count": 0, "tokens": {}, "recent": []}),
        "vps_health": safe(vps_health, {}),
        "cron_jobs": safe(cron_jobs, []),
    }


# ---------------------------------------------------------------------------
# Operator task board (board.db) — read-write
# ---------------------------------------------------------------------------


_BOARD_LOCK = threading.Lock()


def board_init():
    os.makedirs(PROJECT_DIR, exist_ok=True)
    with _BOARD_LOCK:
        conn = sqlite3.connect(BOARD_DB_PATH, timeout=5)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS tasks ("
                "id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT DEFAULT 'pending',"
                "priority TEXT DEFAULT 'medium', notes TEXT DEFAULT '',"
                "created_at TEXT NOT NULL, updated_at TEXT)"
            )
            conn.commit()
            cur = conn.execute("SELECT COUNT(*) c FROM tasks")
            if cur.fetchone()["c"] == 0:
                now = utcnow_iso()
                seed = [
                    ("Review Discord agent bindings", "in_progress", "high",
                     "Verify each of the 4 agents only listens to its own channel."),
                    ("Draft weekly newsletter draft", "in_progress", "medium",
                     "Outline 3 sections: wins, learnings, asks."),
                    ("Set up cron retention policy", "pending", "medium",
                     "30-day log cleanup, runs 1st of month at 03:00."),
                    ("Audit OpenRouter API keys", "pending", "high",
                     "Some keys have zero balance — rotate or top up."),
                    ("Migrate kanban DB to v2 schema", "completed", "low",
                     "Backfilled consecutive_failures column."),
                    ("Ship syndicate task modal", "completed", "high",
                     "PATCH endpoint + shadcn dialog done."),
                    ("Reply to investor intro email", "pending", "high",
                     "Drafted reply pending sign-off."),
                    ("Triage Support inbox", "completed", "low",
                     "Cleared 14 tickets; 3 escalated."),
                ]
                for title, status, priority, notes in seed:
                    conn.execute(
                        "INSERT INTO tasks (id,title,status,priority,notes,created_at,updated_at)"
                        " VALUES (?,?,?,?,?,?,?)",
                        (str(uuid.uuid4()), title, status, priority, notes, now, now),
                    )
                conn.commit()
        finally:
            conn.close()


def board_list() -> list:
    with _BOARD_LOCK:
        conn = sqlite3.connect(BOARD_DB_PATH, timeout=5)
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.execute(
                "SELECT id,title,status,priority,notes,created_at,updated_at "
                "FROM tasks ORDER BY "
                "CASE status WHEN 'in_progress' THEN 0 WHEN 'pending' THEN 1 "
                "WHEN 'completed' THEN 2 ELSE 3 END, "
                "CASE priority WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END, "
                "created_at DESC"
            )
            return [row_to_dict(r) for r in cur.fetchall()]
        finally:
            conn.close()


def board_create(payload: dict) -> dict:
    title = (payload.get("title") or "").strip()
    if not title:
        return {"error": "title is required"}
    status = payload.get("status", "pending")
    priority = payload.get("priority", "medium")
    notes = payload.get("notes", "")
    now = utcnow_iso()
    task_id = str(uuid.uuid4())
    with _BOARD_LOCK:
        conn = sqlite3.connect(BOARD_DB_PATH, timeout=5)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute(
                "INSERT INTO tasks (id,title,status,priority,notes,created_at,updated_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (task_id, title, status, priority, notes, now, now),
            )
            conn.commit()
        finally:
            conn.close()
    return {"id": task_id, "title": title, "status": status, "priority": priority,
            "notes": notes, "created_at": now, "updated_at": now}


def board_update(task_id: str, payload: dict) -> dict:
    fields = []
    values: list = []
    for key in ("title", "status", "priority", "notes"):
        if key in payload and payload[key] is not None:
            fields.append(f"{key}=?")
            values.append(payload[key])
    if not fields:
        return {"error": "no fields to update"}
    fields.append("updated_at=?")
    values.append(utcnow_iso())
    values.append(task_id)
    with _BOARD_LOCK:
        conn = sqlite3.connect(BOARD_DB_PATH, timeout=5)
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id=?", values)
            conn.commit()
            if cur.rowcount == 0:
                return {"error": "task not found"}
            cur = conn.execute(
                "SELECT id,title,status,priority,notes,created_at,updated_at FROM tasks WHERE id=?",
                (task_id,),
            )
            row = cur.fetchone()
            return row_to_dict(row) if row else {"error": "task not found"}
        finally:
            conn.close()


def board_delete(task_id: str) -> dict:
    with _BOARD_LOCK:
        conn = sqlite3.connect(BOARD_DB_PATH, timeout=5)
        try:
            cur = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            return {"deleted": cur.rowcount}
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# HTTP layer
# ---------------------------------------------------------------------------


class Handler(BaseHTTPRequestHandler):
    server_version = "AgentMissionControl/1.0"

    def log_message(self, format, *args):  # noqa: A002
        # Quiet logging
        pass

    def _send_json(self, code: int, payload):
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: str, content_type: str):
        try:
            with open(path, "rb") as f:
                body = f.read()
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            return self._send_file(INDEX_HTML_PATH, "text/html; charset=utf-8")
        if url.path == "/api/snapshot":
            return self._send_json(200, snapshot())
        if url.path == "/api/board":
            return self._send_json(200, board_list())
        if url.path == "/events":
            return self._stream_sse()
        if url.path == "/healthz":
            return self._send_json(200, {"ok": True})
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"not found")

    def do_POST(self):  # noqa: N802
        url = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:
            payload = {}

        if url.path == "/api/board":
            return self._send_json(200, board_create(payload))
        if url.path == "/api/board/update":
            qs = parse_qs(url.query)
            task_id = (qs.get("id") or [""])[0]
            if not task_id:
                return self._send_json(400, {"error": "id query param required"})
            return self._send_json(200, board_update(task_id, payload))
        if url.path == "/api/board/delete":
            qs = parse_qs(url.query)
            task_id = (qs.get("id") or [""])[0]
            if not task_id:
                return self._send_json(400, {"error": "id query param required"})
            return self._send_json(200, board_delete(task_id))

        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"not found")

    def _stream_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        last_payload = None
        try:
            while True:
                snap = snapshot()
                payload = json.dumps(snap, default=str)
                if payload != last_payload:
                    self.wfile.write(b"event: snapshot\n")
                    self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    last_payload = payload
                # heartbeat
                self.wfile.write(b": ping\n\n")
                self.wfile.flush()
                time.sleep(5)
        except (BrokenPipeError, ConnectionResetError):
            return


class ThreadingHTTPServerImpl(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    board_init()
    if not os.path.exists(INDEX_HTML_PATH):
        print(f"WARNING: index.html not found at {INDEX_HTML_PATH}")
    server = ThreadingHTTPServerImpl((HOST, PORT), Handler)
    print(f"Agent Mission Control listening on http://{HOST}:{PORT}")
    print(f"HERMES_HOME = {HERMES_HOME}")
    print(f"Project dir  = {PROJECT_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
