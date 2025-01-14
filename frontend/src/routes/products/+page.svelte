<script lang="ts">
  import ProductCard from "$lib/Product/ProductCard.svelte";
  import LayoutGrid, {Cell} from '@smui/layout-grid'
  import {onMount} from "svelte";
  import { deleteProduct, getAllProducts } from '../../api/products.js';
  import type {Product} from "../../model/products";
  import Button, { Icon } from '@smui/button';
  import YesNoDialog from '$lib/shared/YesNoDialog.svelte';

  let products : Product[] = []
  let product: Partial<Product> = {}
  let dialogOpen = false;
  onMount(() => {
      getAllProducts()
        .then((value)=>{
          if(value){
            products=value
          }
        });
  });

  const handleDelete = (p: Product)=>{
    product=p
    dialogOpen=true
  }

  const cancelDelete = ()=>{product={};dialogOpen=false}

  const deleteItem = (id: number)=>{
    deleteProduct(id)
      .then(()=>{
        getAllProducts()
        .then((value)=>{
          if(value){
            products=value
          }
        });
      })
  }
</script>

<div class="p4">

  <div class="flex-row space-between">
    <h2>Product Dashboard</h2>
    <Button onclick={() => window.location.href = '/products/new'} variant="raised" color="primary">
      <Icon class="material-icons" >add</Icon>Product
    </Button>

  </div>

  <LayoutGrid>
    {#each products as product}
      <Cell span={4}>
        <ProductCard product={product} deleteTrigger={handleDelete}/>
      </Cell>
    {/each}
  </LayoutGrid>
</div>


<YesNoDialog
  bind:open={dialogOpen}
  title="Delete Product"
  message="Are you sure you want to delete {product.name}?"
  onConfirm={()=>{ deleteItem(product.id??-1) }}
  onCancel={cancelDelete}
/>