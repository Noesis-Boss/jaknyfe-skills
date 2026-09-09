#!/usr/bin/env python3
"""HeyGen voice clone + TTS for the youtube-auto-posting skill.

Requires HEYGEN_API_KEY in the environment (Zo secret).

Commands:
  clone <audio-file> --name "Don"     Upload a voice sample, start cloning.
  status <voice_id>                   Poll clone status until complete.
  speech <voice_id> <script.md> --out <dir> [--speed 1.0]
                                      Generate narration audio from a script
                                      (strips stage directions, chunks text
                                      to the 5000-char API limit, downloads
                                      and concatenates audio with ffmpeg).
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

API = "https://api.heygen.com"
KEY = os.environ.get("HEYGEN_API_KEY")
if not KEY:
    sys.exit("HEYGEN_API_KEY not set (Settings > Advanced > Secrets)")


def req(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(
        f"{API}{path}", data=data, method=method,
        headers={"x-api-key": KEY, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(r, timeout=600) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def cmd_clone(args):
    mt = mimetypes.guess_type(args.audio)[0] or "audio/mpeg"
    with open(args.audio, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        "audio": {"type": "base64", "media_type": mt, "data": b64},
        "voice_name": args.name,
    }
    d = req("POST", "/v3/voices/clone", payload)
    print(json.dumps(d, indent=2))
    data = d.get("data", {})
    vid = data.get("voice_clone_id") or data.get("voice_id")
    if vid:
        print(f"VOICE_ID: {vid}")
        print(f"Next: python3 heygen-voice.py status {vid}")


def cmd_status(args):
    d = req("GET", f"/v3/voices/{args.voice_id}")
    print(json.dumps(d, indent=2))


def script_to_text(path):
    """Read script.md and keep only spoken text."""
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("*"):
                continue
            if line.startswith("**[") or set(line) <= set("-_"):
                continue
            line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)  # bold vocab words
            lines.append(line)
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def chunk_text(text, limit=4800):
    chunks, cur = [], ""
    for para in text.split("\n") if False else text.split(". "):
        piece = para if not cur else ". " + para
        if len(cur) + len(piece) > limit and cur:
            chunks.append(cur)
            cur = para
        else:
            cur += piece
    if cur:
        chunks.append(cur)
    return chunks


def download(url, dest):
    with urllib.request.urlopen(url, timeout=300) as r, open(dest, "wb") as f:
        f.write(r.read())


def cmd_speech(args):
    text = script_to_text(args.script)
    if not text:
        sys.exit("No spoken text found in script")
    chunks = chunk_text(text)
    print(f"Script: {len(text)} chars -> {len(chunks)} chunk(s)")
    paths = []
    for i, chunk in enumerate(chunks, 1):
        payload = {
            "text": chunk,
            "voice_id": args.voice_id,
            "input_type": "text",
            "speed": args.speed,
        }
        if args.locale:
            payload["locale"] = args.locale
        d = req("POST", "/v3/voices/speech", payload)
        data = d.get("data", {})
        url = data.get("url") or data.get("audio_url")
        if not url:
            print(json.dumps(d, indent=2))
            sys.exit(f"No audio URL in response for chunk {i}")
        dur = data.get("duration_ms") or data.get("duration")
        print(f"chunk {i}/{len(chunks)} generated (duration: {dur})")
        fd, p = tempfile.mkstemp(suffix=f".mp3", prefix=f"chunk{i}_")
        os.close(fd)
        download(url, p)
        paths.append(p)

    os.makedirs(args.out, exist_ok=True)
    out_file = os.path.join(args.out, "narration.mp3")
    if len(paths) == 1:
        os.replace(paths[0], out_file)
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as lst:
            lst.write("\n".join(f"file '{p}'" for p in paths))
            list_path = lst.name
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
             "-c", "copy", out_file],
            check=True, capture_output=True,
        )
        os.unlink(list_path)
        for p in paths:
            os.unlink(p)
    print(f"OUTPUT: {out_file}")
    subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", out_file],
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("clone", help="clone a voice from an audio sample")
    c.add_argument("audio")
    c.add_argument("--name", default="Don")
    c.set_defaults(fn=cmd_clone)

    s = sub.add_parser("status", help="poll voice clone status")
    s.add_argument("voice_id")
    s.set_defaults(fn=cmd_status)

    t = sub.add_parser("speech", help="generate narration audio from script")
    t.add_argument("voice_id")
    t.add_argument("script")
    t.add_argument("--out", default=".")
    t.add_argument("--speed", type=float, default=1.0)
    t.add_argument("--locale", default=None)
    t.set_defaults(fn=cmd_speech)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
