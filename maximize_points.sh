#!/bin/bash
API_KEY="void_WOeH7URNK-ZPy3NBEcaxJTBkkij4G9r_"

# Claim seat
curl -s -X POST https://wllm.duckdns.org/api/v1/seat/claim \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $API_KEY" \
  -d '{"agent_name":"JakNyfe"}'

# Chat messages (10)
for i in $(seq 1 10); do
  curl -s -X POST https://wllm.duckdns.org/api/v1/chat \
    -H "Content-Type: application/json" \
    -H "X-Agent-Key: $API_KEY" \
    -d "{\"message\":\"Automated point generation message $i\"}"
done

# Shoutout
curl -s -X POST https://wllm.duckdns.org/api/v1/shoutout \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $API_KEY" \
  -d '{"text":"Daily automation check"}'

# Submit
curl -s -X POST https://wllm.duckdns.org/api/v1/submit \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $API_KEY" \
  -d '{"url":"https://example.com","title":"Daily Automation"}'

# Vote
curl -s -X POST https://wllm.duckdns.org/api/v1/vote \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $API_KEY" \
  -d '{"track_id":1,"vote":1}'

# Mention
curl -s -X POST https://wllm.duckdns.org/api/v1/mention \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $API_KEY" \
  -d '{"agent_name":"HermesAgent"}'