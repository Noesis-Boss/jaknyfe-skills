# Local Presenton demo

This configuration runs Presenton on port 5000 and uses the local Ollama service at port 11434. It does not require a Presenton API key. Generated files persist under `app_data/`.

## Start

```bash
docker compose up -d
```

Open `http://localhost:5000`, or generate from the workspace runner:

```bash
PRESENTON_URL=http://localhost:5000 \
  bun run /home/workspace/Skills/presenton/scripts/presenton.ts \
  --content /home/workspace/Media/presenton-demo/presenton-demo.md \
  --slides 7 --output pptx
```

Repeat with `--output pdf` for a PDF.

## Current host requirement

Docker Engine must be running. The Docker CLI is installed on Zo, but this host currently has no Docker daemon socket at `/var/run/docker.sock`.
