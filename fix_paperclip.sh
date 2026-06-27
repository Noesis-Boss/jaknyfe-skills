#!/bin/bash

# Clear old PGlite database file
rm -f /home/workspace/paperclip/dev.db

# Start the server in the background
cd /home/workspace/paperclip
nohup npm run dev > server.log 2>&1 &

# Wait for health endpoint (adjust port if necessary)
echo "Waiting for health endpoint to respond..."
timeout=30
while ! curl -s http://localhost:3000/health > /dev/null; do
  sleep 2
  ((timeout--))
  if [ $timeout -le 0 ]; then
    echo "Health check failed after $timeout seconds."
    echo "Diagnostic info:" >> server.log
    echo "Last 50 lines of server log:" >> server.log
    tail -n 50 server.log >> server.log
    exit 1
  fi
done

echo "Server is healthy!"