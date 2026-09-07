import asyncio
import json
from urllib.parse import parse_qs, urlsplit

from twscrape import gather
from twscrape_twitter_mcp.pool import get_api, list_accounts


async def handle(reader, writer):
    request = await reader.read(8192)
    line = request.split(b"\r\n", 1)[0].decode("utf-8", "replace")
    path = line.split(" ")[1] if len(line.split(" ")) > 1 else "/"
    parsed = urlsplit(path)
    query = parse_qs(parsed.query)
    if parsed.path == "/status":
        rows = await list_accounts()
        payload = {"ready": any(row["active"] for row in rows), "accounts": len(rows)}
    elif parsed.path == "/search":
        text = query.get("q", [""])[0].strip()
        limit = min(max(int(query.get("limit", [10])[0]), 1), 40)
        if not text:
            payload = {"error": "q is required"}
        else:
            results = await gather(get_api().search(text, limit=limit, kv={"product": "Latest"}))
            payload = {"results": [{"id": str(item.id), "text": item.rawContent, "url": f"https://x.com/i/status/{item.id}", "date": item.date.isoformat(), "likes": item.likeCount, "reposts": item.retweetCount} for item in results]}
    else:
        payload = {"error": "not found"}
    body = json.dumps(payload).encode()
    status = b"200 OK" if "error" not in payload else b"400 Bad Request"
    writer.write(b"HTTP/1.1 " + status + b"\r\nContent-Type: application/json\r\nContent-Length: " + str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle, "127.0.0.1", 8098)
    async with server:
        await server.serve_forever()


asyncio.run(main())
