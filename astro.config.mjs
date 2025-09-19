import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import lit from '@astrojs/lit';
import sitemap from '@astrojs/sitemap';
import icon from 'astro-icon';

import react from '@astrojs/react';

export default defineConfig({
  site: 'https://iancolliard.github.io/Research.github.io', 
  base: '/Research.github.io',                              
  integrations: [sitemap(), mdx(), lit(), icon(), react()],
});