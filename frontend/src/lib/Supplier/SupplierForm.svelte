<script lang="ts">
    import Textfield from '@smui/textfield';
    import Button from '@smui/button';
    import { onMount } from 'svelte';
	import type { Supplier } from '../../model/supplier';
	import Paper from '@smui/paper';
  
    export let id: number | null = null; // ID for editing a Supplier (null means create mode)
    export let onSubmit: (supplier: Supplier) => void;
  
    let supplier: Supplier = { name: '', mail: '', tel: '' };
    let errors: Partial<Record<keyof Supplier, string>> = {};
  
    onMount(async () => {
      if (id) {
        // Fetch the supplier details for editing
        const response = await fetch(`/api/suppliers/${id}`);
        if (response.ok) {
          supplier = await response.json();
        }
      }
    });
  
    function validateForm(): boolean {
      errors = {};
  
      if (!supplier.name.trim()) {
        errors.name = 'Name is required';
      }
  
      if (!supplier.mail.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(supplier.mail)) {
        errors.mail = 'Valid email is required';
      }
  
      if (!supplier.tel.trim()) {
        errors.tel = 'Phone number is required';
      }
  
      return Object.keys(errors).length === 0;
    }
  
    function handleSubmit() {
      if (validateForm()) {
        onSubmit(supplier);
      }
    }
  </script>

<Paper elevation={2} class="p-4">
  <form on:submit|preventDefault={handleSubmit}>
    <Textfield
      label="Name"
      bind:value={supplier.name}
      required
      class="m4"
      invalid={!!errors.name}
    >
    </Textfield>

    <Textfield
      label="Email"
      type="email"
      bind:value={supplier.mail}
      invalid={!!errors.mail}
      class="m4"
    >
    </Textfield>

    <Textfield
      label="Phone Number"
      bind:value={supplier.tel}
      required
      invalid={!!errors.tel}
      class="m4"
    >
    </Textfield>

    <Button type="submit" variant="raised" class="m4">
      {id ? 'Update Supplier' : 'Add Supplier'}
    </Button>
  </form>
</Paper>
