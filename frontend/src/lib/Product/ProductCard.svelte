<script lang="ts">
  import Card, { ActionButtons, ActionIcons, Actions, Content } from '@smui/card';
  import Chip from '@smui/chips';
  import { Label } from '@smui/common';
  import type { Product } from '../../model/products';
  import Button, { Icon } from '@smui/button';
  import IconButton from '@smui/icon-button';
  import { goto } from '$app/navigation';

  export let product: Product;
  export let deleteTrigger: (product: Product) => void;

  function handleDelete() {
      deleteTrigger(product);
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
          </div>
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
              </ActionIcons>
          </Actions>
      </div>

      <p >{product.description}</p>
      <p >€{product.retail_price.toFixed(2)}</p>
  </Content>
</Card>
