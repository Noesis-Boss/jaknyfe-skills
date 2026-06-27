#!/bin/bash
# Heartbeat script for Void competition seat keeping
API_KEY="void_WOeH7URNK-ZPy3NBEcaxJTBkkij4G9r_"

# Claim seat (ensure we have a seat)
echo "Claiming seat at $(date)" >> /home/workspace/heartbeat.log
curl -s -X POST https://wllm.duckdns.org/api/v1/seat/claim \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $API_KEY" \
  -d '{"agent_name":"JakNyfe"}' >> /home/workspace/heartbeat.log 2>&1

echo "" >> /home/workspace/heartbeat.log

# Send heartbeat
echo "Sending heartbeat at $(date)" >> /home/workspace/heartbeat.log
curl -s -X POST https://wllm.duckdns.org/api/v1/seat/heartbeat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $API_KEY" >> /home/workspace/heartbeat.log 2>&1

echo "" >> /home/workspace/heartbeat.log