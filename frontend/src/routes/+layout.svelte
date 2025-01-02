<script lang="ts">
	import '../app.css';
  import Navbar from '$lib/navbar.svelte';
</script>

<div class="min-h-screen flex flex-col">
  <Navbar />
  <main class="flex-grow">
    <slot />
  </main>
</div>

