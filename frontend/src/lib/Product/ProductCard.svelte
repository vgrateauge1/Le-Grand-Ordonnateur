<script lang="ts">
  import Card, { ActionIcons, Actions, Content } from '@smui/card';
  import type { Product } from '../../model/products';
  import IconButton from '@smui/icon-button';
  import { goto } from '$app/navigation';

  export let product: Product;
  export let selectable: boolean = false; // Whether the card is in selection mode
  export let isSelected: boolean = false; // Whether the product is selected
  export let toggleSelection: (product: Product) => void = null; // Callback for selection toggle
  export let deleteTrigger: (product: Product) => void = null; // Optional: only used in the Product page

  function handleToggleSelection() {
    if (toggleSelection) {
      toggleSelection(product);
    }
  }

  function handleDelete() {
    if (deleteTrigger) {
      deleteTrigger(product);
    }
  }
</script>

<Card class="card">
  <Content>
    <div class="flex-row space-between">
      <div>
        <h5 style="margin: 0">{product.name}</h5>
        <div class="mdc-typography--subtitle2">
          Created: {new Date(product.creation_date).toLocaleString()}
        </div>
        <div>
          <h5 style="margin: 0">{product.name}</h5>
          <div>Quantity: {product.quantity}</div>
        </div>
        <div>{product.is_active ? 'active' : 'inactive'}</div>
      </div>

      {#if selectable}
        <!-- Selection Mode: Show `+` button -->
        <Actions style="padding: 0">
          <ActionIcons>
            <IconButton
              class="material-icons"
              style="color: {isSelected ? '#007bff' : '#ccc'}"
              onclick={handleToggleSelection}
              title={isSelected ? 'Deselect' : 'Select'}
            >
              add
            </IconButton>
          </ActionIcons>
        </Actions>
      {:else}
        <!-- Default Mode: Show edit/delete buttons -->
        <Actions style="padding: 0">
          <ActionIcons>
            <IconButton
              class="material-icons"
              onclick={() => { goto(`/products/${product.id}`) }}
              title="Edit">edit</IconButton>
            <IconButton
              class="material-icons"
              onclick={handleDelete}
              title="Delete">delete</IconButton>
            <IconButton
                class="material-icons"
                onclick={() => { goto(`/products/${product.id}/stock`) }}
                title="Manage Stock">inventory</IconButton>

          </ActionIcons>
        </Actions>
      {/if}
    </div>

    <p>{product.description}</p>
  </Content>
</Card>

<style>
  .card {
    margin-bottom: 1em;
  }
</style>
