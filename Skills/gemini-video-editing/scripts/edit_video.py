#!/usr/bin/env python3
"""Upload a video to Gemini Omni Flash, apply an edit prompt, and save the result."""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.request

API_ROOT = "https://generativelanguage.googleapis.com"


def request(url, method="GET", headers=None, data=None):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=300) as response:
        return response.status, response.headers, response.read()


def upload(path, api_key):
    raw = open(path, "rb").read()
    mime = mimetypes.guess_type(path)[0] or "video/mp4"
    start_headers = {
        "x-goog-api-key": api_key,
        "X-Goog-Upload-Protocol": "resumable",
        "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(len(raw)),
        "X-Goog-Upload-Header-Content-Type": mime,
        "Content-Type": "application/json",
    }
    _, headers, _ = request(
        f"{API_ROOT}/upload/v1beta/files",
        method="POST",
        headers=start_headers,
        data=json.dumps({"file": {"display_name": os.path.basename(path)}}).encode(),
    )
    upload_url = headers.get("X-Goog-Upload-URL")
    if not upload_url:
        raise RuntimeError("Gemini did not return an upload URL")
    _, _, body = request(
        upload_url,
        method="POST",
        headers={
            "Content-Length": str(len(raw)),
            "X-Goog-Upload-Offset": "0",
            "X-Goog-Upload-Command": "upload, finalize",
        },
        data=raw,
    )
    return json.loads(body)["file"]


def main():
    parser = argparse.ArgumentParser(description="Edit a local video with Gemini Omni Flash")
    parser.add_argument("video", help="source video path")
    parser.add_argument("prompt", help="focused edit instruction")
    parser.add_argument("output", help="destination MP4 path")
    parser.add_argument("--model", default="gemini-omni-1.1-flash")
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY in the environment before running this command")
    uploaded = upload(args.video, api_key)
    file_name = uploaded["name"]
    while True:
        _, _, body = request(f"{API_ROOT}/v1beta/{file_name}", headers={"x-goog-api-key": api_key})
        status = json.loads(body)
        if status.get("state") == "ACTIVE":
            break
        if status.get("state") == "FAILED":
            raise RuntimeError("Gemini video processing failed")
        time.sleep(5)
    payload = {
        "model": args.model,
        "input": [
            {"type": "video", "uri": uploaded["uri"], "mime_type": uploaded.get("mimeType", "video/mp4")},
            {"type": "text", "text": args.prompt},
        ],
        "response_format": {"type": "video", "delivery": "uri"},
    }
    _, _, body = request(
        f"{API_ROOT}/v1beta/interactions",
        method="POST",
        headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
        data=json.dumps(payload).encode(),
    )
    interaction = json.loads(body)
    output_video = interaction.get("output_video", {})
    if output_video.get("data"):
        import base64
        open(args.output, "wb").write(base64.b64decode(output_video["data"]))
    elif output_video.get("uri"):
        uri = output_video["uri"]
        file_id = uri.rsplit("/", 1)[-1]
        while True:
            _, _, body = request(f"{API_ROOT}/v1beta/files/{file_id}", headers={"x-goog-api-key": api_key})
            state = json.loads(body)
            if state.get("state") == "ACTIVE":
                break
            if state.get("state") == "FAILED":
                raise RuntimeError("Gemini output processing failed")
            time.sleep(5)
        _, _, data = request(uri, headers={"x-goog-api-key": api_key})
        open(args.output, "wb").write(data)
    else:
        raise RuntimeError("Gemini response contained no video output")
    print(os.path.abspath(args.output))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")
        print(f"Gemini API error {error.code}: {detail}", file=sys.stderr)
        raise SystemExit(1)
