<script lang="ts">
  import Textfield from '@smui/textfield';
  import Switch from '@smui/switch';
  import FormField from '@smui/form-field';
  import Paper from '@smui/paper';
  import HelperText from '@smui/textfield/helper-text';
  import type { Product } from '../../model/products';
  import { updateStock } from '../../api/products';
  import Button, { Icon, Label } from '@smui/button';

  export let onSubmit: (product: Product) => void;
  export let product: Product;
  product.quantity = 0;

  let errors: Partial<Record<keyof Product, string>> = {};
  
  // Validate the product form fields
  function validateForm(): boolean {
    errors = {};

    if (product.name.trim().length <= 0) {
      errors.name = 'Name is required';
    }

    if (product.description.trim().length <= 0) {
      errors.description = 'Description is required';
    }
    if (product.quantity === undefined || product.quantity < 0) {
      errors.quantity = 'Stock quantity must be a positive number';
    } 

    return Object.keys(errors).length === 0;
  }

  // Handle form submission
  async function handleSubmit() {
    if (validateForm()) {
      try {
        const createdProduct = await onSubmit(product); // Crée le produit
        if (product.id) {
          // Initialise le stock
          await updateStock(product.id, product.quantity || 0);
        }
      } catch (error) {
        console.error('Error creating product or updating stock:', error);
      }
    }
  }
</script>

<Paper elevation={2} class="p-4">
  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <!-- Product Name -->
    <Textfield
      label="Product Name"
      bind:value={product.name}
      required
      invalid={!!errors.name}
    >
    </Textfield>

    <!-- Product Description -->
    <Textfield
      label="Description"
      textarea
      bind:value={product.description}
      invalid={!!errors.description}
    >
    </Textfield>

    <Textfield
    label="Stock Quantity"
    type="number"
    bind:value={product.quantity}
    invalid={!!errors.quantity}
    > </Textfield>


    <!-- Product Active Status -->
    <FormField>
      <Switch bind:checked={product.is_active} />
      <Label>Active</Label>
    </FormField>

    <!-- Submit Button -->
    <div class="flex-row end">
      <Button variant="unelevated" type="submit" class="button-shaped-round">
        <Icon class="material-icons">save</Icon>
        <Label>Save</Label>
      </Button>
    </div>
  </form>
</Paper>

<style>
  form :global(.mdc-text-field) {
    width: 100%;
    margin-bottom: 1rem;
  }
</style>