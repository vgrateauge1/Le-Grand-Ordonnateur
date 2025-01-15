<script lang="ts">
    import Textfield from '@smui/textfield';
    import Paper from '@smui/paper';
    import Button, { Icon, Label } from '@smui/button';
    import type { Stock } from '../../model/products';
    import { updateStock } from '../../api/products';
  
    export let productStock: Stock;
    export let onRefresh: () => void;
  
    let newQuantity = productStock?.quantity || 0;
    let errors: { quantity?: string } = {};
  
    // Validate the stock quantity
    function validateForm(): boolean {
      errors = {};
      if (newQuantity < 0) {
        errors.quantity = 'Quantity must be a positive number';
        return false;
      }
      return true;
    }
  
    // Handle stock update
    async function handleSubmit() {
      if (validateForm()) {
        try {
          await updateStock(productStock.product, newQuantity);
          alert('Stock updated successfully!');
          onRefresh(); // Refresh the parent data
        } catch (error) {
          console.error('Error updating stock:', error);
        }
      }
    }
  </script>
  
  <Paper elevation={2} class="p-4">
    <h3 class="mb-4">Stock Management</h3>
    <form on:submit|preventDefault={handleSubmit} class="space-y-4">

         <!-- Display current stock info -->
        <div class="stock-info">
            <p><strong>Last saved Quantity:</strong> {productStock.quantity}</p>
            <p><strong>Last Updated:</strong> {new Date(productStock.last_updated).toLocaleString()}</p>
        </div>
      <!-- Current Stock Quantity -->
      <Textfield
        label="Stock Quantity"
        type="number"
        bind:value={newQuantity}
        invalid={!!errors.quantity}
      >
      </Textfield>
  
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
    .p-4 {
      padding: 16px;
    }
  
    .mb-4 {
      margin-bottom: 16px;
    }
  
    form :global(.mdc-text-field) {
      width: 100%;
      margin-bottom: 1rem;
    }
  
    .flex-row.end {
      display: flex;
      justify-content: flex-end;
    }
  
    .button-shaped-round {
      border-radius: 50px;
    }
  </style>
  