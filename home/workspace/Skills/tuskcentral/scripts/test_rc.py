#!/usr/bin/env python3
import subprocess, sys, time, json

SESSION = "tuskcentral"
TUSK_CHAT_URL = "https://tuskcentral.ai/chat"

def run_ab(args, timeout=60):
    cmd = ["agent-browser", "--session", SESSION] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        print(f"TIMEOUT after {timeout}s", file=sys.stderr)
        return -1, "", f"timeout: {e}"

rc, out, err = run_ab(["get", "url"], timeout=10)
print(f"get url: rc={rc}, out={repr(out.strip())}, err={repr(err.strip())}")
