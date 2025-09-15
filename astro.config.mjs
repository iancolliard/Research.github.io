// astro.config.mjs
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import lit from '@astrojs/lit';
import sitemap from '@astrojs/sitemap';
import icon from 'astro-icon';

// --- DEV SETTINGS (easier):
// While developing locally, DO NOT set `base` so fonts/assets work at "/"
export default defineConfig({
  site: 'https://iancolliard.github.io',   // keep as your main domain
  integrations: [sitemap(), mdx(), lit(), icon()],
});
