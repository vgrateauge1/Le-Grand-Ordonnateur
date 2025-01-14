<script lang="ts">
    import Textfield from '@smui/textfield';
    import Button from '@smui/button';
    import { onMount } from 'svelte';
	  import type { Material } from '../../model/material';
	import Paper from '@smui/paper';
  
    export let id: number | null = null; // ID for editing a Material (null means create mode)
    export let onSubmit: (material: Material) => void;
  
    let material: Material = { name: '', description: ''};
    let errors: Partial<Record<keyof Material, string>> = {};
  
    onMount(async () => {
      if (id) {
        // Fetch the material details for editing
        const response = await fetch(`/api/materials/${id}`);
        if (response.ok) {
          material = await response.json();
        }
      }
    });
  
    function validateForm(): boolean {
      errors = {};
  
      if (!material.name.trim()) {
        errors.name = 'Name is required';
      }
      return Object.keys(errors).length === 0;
    }
  
    function handleSubmit() {
      if (validateForm()) {
        onSubmit(material);
      }
    }
  </script>
  
  <Paper elevation={2} class="p-4">
      <form on:submit|preventDefault={handleSubmit}>
        <Textfield
          label="Name"
          bind:value={material.name}
          required
          invalid={!!errors.name}
          class="m4"
        >
        </Textfield>
      
        <Textfield
          label="Description"
          textarea
          bind:value={material.description}
          class="m4"
        >
        </Textfield>
      
        <Button type="submit" variant="raised" class="m4">
          {id ? 'Update Material' : 'Add Material'}
        </Button>
      </form>
  </Paper>

  