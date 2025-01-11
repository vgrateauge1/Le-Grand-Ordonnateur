<script lang="ts">

	import ProductForm from "$lib/Product/ProductForm.svelte";
	import { getBOM, getProductById, getProductVersions, upsertBOM, upsertProduct, upsertVersion } from '../../../api/products';
	import type {BomLine, Product, Version} from "../../../model/products";
	import {goto} from "$app/navigation";
	import { page } from '$app/state';
	import {onMount} from "svelte";
	import { error } from '@sveltejs/kit';
	import TabBar from '@smui/tab-bar';
	import Tab from "@smui/tab";
	import { Label } from '@smui/button';
	import VersionForm from "$lib/Product/VersionForm.svelte";
		import BomDashboard from "$lib/Product/BOMDashboard.svelte";
	import MaterialForm from "$lib/Material/MaterialForm.svelte";
	import type { Material } from "../../../model/material";
	import type { Supplier } from "../../../model/supplier";
	import { getAllMaterials } from "../../../api/material";
	import { getAllSuppliers } from "../../../api/supplier";

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

	//BOM
	let materials: Material[] = $state([])
	let suppliers: Supplier[] = $state([])
	let bom : BomLine[] = $state([])

	onMount(() => {
		id = page.url.pathname.split('/').pop() ?? '';
		if (id == 'new') {
			title = 'Create new product'
			isCreation=true
		} else if (id != undefined) {
			handleTabChange(active)
		} else {
			throw error(404, {
				message: 'undefined product'
			});
		}
	})

	// Submits
	const handleProductSubmit = async (product: Product) => {
		await upsertProduct(product)
			.then((value)=>{
				if(value){
					title=value.name
					id=`${value.id}`
					goto(`/products/${value.id}`)
				}
			})
	}

	const handleVersionSubmit = async (version: Version)=>{
		await upsertVersion(version)
				.then((value)=>{
					if(value){
						version = value
					}
				})
	}

	const handleBomSubmit = (bomLines:BomLine[]) => {
		upsertBOM(id, bomLines).then((value)=>{
			bom=value
			handleTabChange(active)
		})
	}

	const handleTabChange = (a: String) =>{
		switch(a){
			case 'Info':
				getProductById(id)
					.then((value)=>{
						product=value
						title = product.name
					}
				)
				break
			case 'Versioning':
				getProductVersions(id).then((value)=>{
						versions=value
						version = {...version,...versions.find(x=>x.is_active),product:parseInt(id)}
					}
				)
				break
			case 'Bill of material':
				getAllMaterials().then((value)=>{
						materials=value
					}
				)
				getAllSuppliers().then((value)=>{
						suppliers=value
					}
				)
				getBOM(id).then((value)=>{
					bom=value
				})
			case 'Manufacturing':
			case 'Stock':
		}
	}
</script>

<div>
	<h3 style="margin:16px">{title}</h3>
	<TabBar tabs={['Info', 'Versioning', 'Bill of material', 'Manufacturing', 'Stock']} bind:active>
		{#snippet tab(tab: String)}
		<Tab {tab} onfocus={()=>handleTabChange(tab)}>
			<Label>{tab}</Label>
		</Tab>
		{/snippet}
  </TabBar>
	{#if active === 'Info'}
		<ProductForm onSubmit={handleProductSubmit} product={product}/>
	{/if}
	{#if !isCreation}
		{#if active === 'Versioning'}
			<VersionForm version={version} versions={versions} onSubmit={handleVersionSubmit} id={id}/>
		{/if}
		{#if active === 'Bill of material'}
			<BomDashboard materials={materials} suppliers={suppliers} bomLines={bom} refresh={()=>handleTabChange(active)} onSubmit={handleBomSubmit}/>
		{/if}
	{/if}
</div>
