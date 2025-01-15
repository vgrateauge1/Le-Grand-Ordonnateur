<script lang="ts">
  import { onMount } from 'svelte';
	import '../app.css';
  import Navbar from '$lib/navbar.svelte';
	import Login from '$lib/login.svelte';
	import { connect, deconnect, getCsrfToken } from '../api/user';
  import CircularProgress from '@smui/circular-progress';

  let connected: boolean = $state(false)
  let csrf = $state('')
  let load = $state(true)

  onMount(()=>{
    if(document.cookie.includes('csrftoken')){
      connected=true
    }
    load=false
  })

  const handleLogin = async (username:string ,password: string) => {
    csrf = await getCsrfToken()
    connected = await connect(username, password, csrf)
  }

  const removeAllCookies = () => {
      const cookies = document.cookie.split("; ");

      for (const cookie of cookies) {
          const [name] = cookie.split("="); // Get the cookie name
          document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
      }
  };

  const handleLogout = async() => {
    csrf = await getCsrfToken()
    const ok  = await deconnect(csrf)
    if(ok){
      removeAllCookies()
      connected=false
    }
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
  {#if load}
    <div class="min-h-screen flex flex-row" style="justify-content: center;align-items: center;height: 100vh;">
      <CircularProgress  style="height: 32px; width: 32px;" indeterminate />
    </div>
  {:else}
    <div class="min-h-screen flex flex-row" style="justify-content: center;align-items: center;height: 100vh;">
      <Login handleLogin={handleLogin}/>
    </div>
  {/if}
{/if}


