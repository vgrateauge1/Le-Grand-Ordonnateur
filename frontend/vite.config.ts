import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
  ssr: {
    noExternal: [
      '@smui/button',
      '@smui/card',
      '@smui/form-field',
      '@smui/icon-button',
      '@smui/layout-grid',
      '@smui/paper',
      '@smui/switch',
      '@smui/tab',
      '@smui/tab-bar',
      '@smui/textfield',
      '@smui/top-app-bar',
      '@smui/common',
      '@material/typography',
    ]
  }
});
