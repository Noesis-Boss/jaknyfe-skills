# Knights of St. Andrew — Tucson Scottish Rite

Standalone Vite + React site for the Knights of St. Andrew chapter. The development server binds to Zo's injected `PORT` so the preview iframe and local runtime use the configured site port.

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run index.ts
```

## Project Notes

- `vite.config.ts` uses `PORT` when available and binds to `0.0.0.0`; this is required for Zo Site preview routing.
- Production builds remain under `dist/` and use `/` as the asset base.
- Set `DEPLOY_SUBPATH=ksatucson` for nested deployment builds so assets resolve under `/ksatucson/`.
