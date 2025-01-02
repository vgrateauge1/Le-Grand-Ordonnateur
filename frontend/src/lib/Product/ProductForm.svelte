<script lang="ts">
  import Textfield from '@smui/textfield';
  import Switch from '@smui/switch';
  import FormField from '@smui/form-field';
  import Paper from '@smui/paper';
  import HelperText from '@smui/textfield/helper-text';
  import type { Product } from '../../model/products';
  import Button, { Icon, Label } from '@smui/button';
  import IconButton from '@smui/icon-button';


  export let onSubmit: (product: Product) => void;
  export let product: Product;

  let errors: Partial<Record<keyof Product, string>> = {};

  function validateForm(): boolean {
    errors = {};

    if (product.name.trim().length<=0) {
      errors.name = 'Name is required';
    }

    if (product.description.trim().length<=0) {
      errors.description = 'Description is required';
      console.log('error')
    }

    if (product.retail_price <= 0) {
      errors.retail_price = 'Price must be greater than 0';
    }

    if (product.version.trim().length<=0) {
      errors.version = 'Version is required';
    }

    return Object.keys(errors).length === 0;
  }

  function handleSubmit() {
    if (validateForm()) {
      onSubmit(product!);
    }
  }

</script>

<Paper elevation={2} class="p-4">

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <Textfield
      label="Product Name"
      bind:value={product.name}
      required
      invalid={!!errors.name}
    >
      <HelperText slot="helper">{errors.name || ''}</HelperText>
    </Textfield>

    <Textfield
      label="Description"
      textarea
      bind:value={product.description}
      invalid={!!errors.description}
    >
    </Textfield>

    <Textfield
      label="Retail Price"
      bind:value={product.retail_price}
      required
    >
      <HelperText slot="helper">{errors.retail_price || ''}</HelperText>
    </Textfield>

    <Textfield
      label="Version"
      bind:value={product.version}
      required
      invalid={!!errors.version}
    >
      <HelperText slot="helper">{errors.version || ''}</HelperText>
    </Textfield>

    <FormField>
      <Switch
        bind:checked={product.is_active}
      />
      {#snippet label()}
        Active
      {/snippet}
    </FormField>

  </form>
  <div class="flex-row end">
      <div class="flex-row align-center">
          <Button
            variant="unelevated"
            type="submit"
            class="button-shaped-round"
          >
            <Icon class="material-icons">save</Icon>
            <Label>Save</Label>
          </Button>
      </div>
  </div>
</Paper>


<style>
  form :global(.mdc-text-field) {
    width: 100%;
    margin-bottom: 1rem;
  }
</style>