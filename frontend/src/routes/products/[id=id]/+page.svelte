<script lang="ts">

import ProductForm from "$lib/Product/ProductForm.svelte";
import { getProductById, upsertProduct } from '../../../api/products';
import type {Product} from "../../../model/products";
import {goto} from "$app/navigation";
import { page } from '$app/state';
import {onMount} from "svelte";
import { error } from '@sveltejs/kit';
import TabBar from '@smui/tab-bar';
import Tab from "@smui/tab";
import { Label } from '@smui/button';

let active = $state('Info');
let title = $state('')
const defaultProduct = {
	name: '',
	description: '',
	retail_price: 0,
	version: '1.0.0',
	is_active: true
};
let product: Product = $state(defaultProduct)

onMount(() => {
	const id: string | undefined = page.url.pathname.split('/').pop();
	if (id == 'new') {
		title = 'Create new product'
	} else if (id != undefined) {
		getProductById(id)
			.then((value)=>{
				product=value
				title = product.name
			})
			.catch((reason)=>{
			throw error(reason.id, {
				message: reason.message
			});
		})
	} else {
		throw error(404, {
			message: 'undefined product'
		});
	}
})

const HandleSubmit = async (product: Product) => {
		await upsertProduct(product)
			.catch((reason)=>{console.log(reason)})
			.then((value)=>{
				if(value){
					title=value.name
					goto(`/products/${value.id}`)
				}
			})
}
</script>

<div>
		<h3 style="margin:16px">{title}</h3>
	  <TabBar tabs={['Info', 'Versioning', 'Bill of material', 'Manufacturing', 'Stock', ]} bind:active>
    {#snippet tab(tab)}
      <!-- Note: the `tab` property is required! -->
      <Tab {tab}>
        <Label>{tab}</Label>
      </Tab>
    {/snippet}
  </TabBar>
	{#if active === 'Info'}
		<ProductForm onSubmit={HandleSubmit} product={product}/>
	{/if}
</div>
