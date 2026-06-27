    bash
    #!/bin/bash
    kilocode acp &
    sleep 5
    hermes config set acp.server_url "http://localhost:4242"
    hermes mcp add kilocode-acp
    hermes
