<script lang="ts">
  import { onMount } from 'svelte';
	import '../app.css';
  import Navbar from '$lib/navbar.svelte';
	import Login from '$lib/login.svelte';
	import { connect, deconnect, getCsrfToken } from '../api/user';

  let connected: boolean = $state(false)
  let csrf = $state('')

  onMount(async ()=>{
    csrf = await getCsrfToken()
  });

  const handleLogin = async (username:string ,password: string) => {
    connected = await connect(username, password, csrf)
  }

  const handleLogout = async() => {
    connected = await deconnect(csrf)
  }
</script>


{#if connected}
  <div class="min-h-screen flex flex-col">
    <Navbar handleLogout={handleLogout}/>
    <main class="flex-grow">
      <slot />
    </main>
  </div>
{:else}
  <div class="min-h-screen flex flex-row" style="justify-content: center;align-items: center;height: 100vh;">
    <Login handleLogin={handleLogin}/>
  </div>
{/if}


