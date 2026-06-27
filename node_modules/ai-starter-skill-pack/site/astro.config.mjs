// @ts-check
import { defineConfig } from 'astro/config';

// Served from GitHub Pages at https://jeff-kazzee.github.io/ai-starter-skill-pack/
// `site` is the origin and `base` is the repository subpath. Raw files in
// `public/` must be referenced with the base prefix (see BASE_URL usage in
// the layout); imported assets and CSS are rewritten automatically.
// https://docs.astro.build/en/guides/deploy/github/
export default defineConfig({
  site: 'https://jeff-kazzee.github.io',
  base: '/ai-starter-skill-pack',
});
