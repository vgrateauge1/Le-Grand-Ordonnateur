<script lang="ts">

import ProductForm from "$lib/Product/ProductForm.svelte";
import { getProductById, getProductVersions, upsertProduct, upsertVersion } from '../../../api/products';
import type {Product, Version} from "../../../model/products";
import {goto} from "$app/navigation";
import { page } from '$app/state';
import {onMount} from "svelte";
import { error } from '@sveltejs/kit';
import TabBar from '@smui/tab-bar';
import Tab from "@smui/tab";
import { Label } from '@smui/button';
import VersionForm from "$lib/Product/VersionForm.svelte";

let active = $state('Info');
let title = $state('')

const defaultProduct = {
	name: '',
	description: '',
	is_active: true,
} as unknown as Product;

const defaultVersion = {
	description:'',
	retail_price:0,
	version:'',
	is_active: true,
} as unknown as Version

let product: Product = $state(defaultProduct)
let versions: Version[] = $state([])
let version: Version = $state(defaultVersion)
let isCreation = $state(false)
let id =  $state('')

onMount(() => {
	id = page.url.pathname.split('/').pop() ?? '';
	if (id == 'new') {
		title = 'Create new product'
		isCreation=true
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

		getProductVersions(id).then((value)=>{
				versions=value
				version = {...version,...versions.find(x=>x.is_active),product:parseInt(id)}
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

const handleProductSubmit = async (product: Product) => {
		await upsertProduct(product)
			.catch((reason)=>{console.log(reason)})
			.then((value)=>{
				if(value){
					title=value.name
					goto(`/products/${value.id}`)
				}
			})
}

const handleVersionSubmit = async (version: Version)=>{
	await upsertVersion(version)
			.catch((reason)=>{console.log(reason)})
			.then((value)=>{
				if(value){
					version = value
				}
			})
}
</script>

<div>
	<h3 style="margin:16px">{title}</h3>
	<TabBar tabs={['Info', 'Versioning', 'Bill of material', 'Manufacturing', 'Stock']} bind:active>
    {#snippet tab(tab: String)}
      <Tab {tab}>
        <Label>{tab}</Label>
      </Tab>
    {/snippet}
  </TabBar>
	{#if active === 'Info'}
		<ProductForm onSubmit={handleProductSubmit} product={product}/>
	{/if}
	{#if !isCreation}
		{#if active === 'Versioning'}
			<VersionForm version={version} versions={versions} onSubmit={handleVersionSubmit}/>
		{/if}
	{/if}
</div>
