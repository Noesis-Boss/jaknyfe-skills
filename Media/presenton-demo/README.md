# Presenton demo configuration

This configuration is ready for a machine that supports Docker. Zo's infrastructure does not provide a Docker daemon, so Presenton cannot run locally inside Zo.

## Run on a Docker-capable machine

```bash
docker compose up -d
```

Open `http://localhost:5000`, or point the workspace runner at a reachable Presenton instance:

```bash
PRESENTON_URL=http://localhost:5000 \
  bun run /home/workspace/Skills/presenton/scripts/presenton.ts \
  --content /home/workspace/Media/presenton-demo/presenton-demo.md \
  --slides 7 --output pptx
```

Repeat with `--output pdf` for a PDF.

## Zo usage

Use a remote or separately hosted Presenton instance and set `PRESENTON_URL` to its address. Set `PRESENTON_API_KEY` only when that instance requires authentication. Keep the API key in Zo Secrets, never in the command or frontend code.
