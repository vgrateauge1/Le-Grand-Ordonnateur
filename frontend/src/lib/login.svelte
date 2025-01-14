<!-- src/Login.svelte -->
<script>
	import Button from "@smui/button";
	import Paper from "@smui/paper";
	import Textfield from "@smui/textfield";

    
    let username = '';
    let password = '';
    let errorMessage = '';
  
    // Handle login logic
    export let handleLogin;

    const onSubmit = () => { handleLogin(username,password) }
  </script>

  
<Paper>
    <h2 class="text-center">Login</h2>
  
    <form on:submit|preventDefault={onSubmit}>
      <Textfield
        label="Username"
        bind:value={username}
        required
        outlined
        fullwidth
        class="mb-4"
      />
      <Textfield
        type="password"
        label="Password"
        bind:value={password}
        required
        outlined
        fullwidth
        class="mb-4"
      />
      <Button raised on:click={handleLogin} class="w-full">Login</Button>
    </form>
  
    {#if errorMessage}
      <div class="error-message">{errorMessage}</div>
    {/if}
</Paper>
  