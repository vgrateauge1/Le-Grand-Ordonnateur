<script>
  import { onMount } from 'svelte';
  import {goto} from "$app/navigation";

  // Perform redirection on mount
  onMount(() => {
    goto('/products');
  });
</script>
