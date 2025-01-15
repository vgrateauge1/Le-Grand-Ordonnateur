<script lang="ts">
  import { onMount } from 'svelte';
  import LayoutGrid, { Cell } from '@smui/layout-grid';
  import Pagination from '$lib/shared/Pagination.svelte';
  import ProductCard from '$lib/Product/ProductCard.svelte';

  import { getActiveProducts, getProductVersions } from '../../api/products';
  import type { Product, Version } from '../../model/products';

  // ======================
  //      COMPONENT STATE
  // ======================
  let products: Product[] = [];
  let productMap: { [key: number]: Product } = {};
  let productVersionsMap: { [key: number]: Version[] } = {};

  let currentPage = 1;
  let pageSize = 2;
  let totalProducts = 0;

  // For the search bar
  let searchQuery = '';

  interface SelectedItem {
    productId: number;
    version: string;
  }
  let selectedItems: SelectedItem[] = [];

  // ======================
  //         MOUNT
  // ======================
  onMount(async () => {
    loadStateFromLocalStorage();
    await fetchActiveProducts(currentPage, pageSize, searchQuery);
  });

  // ======================
  //       FETCH
  // ======================
  async function fetchActiveProducts(page: number, size: number, search: string) {
    try {
      const result = await getActiveProducts(page, size, search);
      if (result) {
        products = result.data;
        totalProducts = result.total;
        mapProducts(products);
        await fetchVersionsForProducts(products);
      }
    } catch (err) {
      console.error('Error fetching active products:', err);
    }
  }

  function mapProducts(productList: Product[]) {
    for (const p of productList) {
      if (p.id != null) {
        productMap[p.id] = p;
      }
    }
  }

  async function fetchVersionsForProducts(prods: Product[]) {
    const fetchPromises = prods.map(async (prod) => {
      if (!prod.id) return;
      try {
        const versions = await getProductVersions(String(prod.id));
        productVersionsMap[prod.id] = versions;
      } catch (err) {
        console.error('Error fetching product versions for:', prod.id, err);
        productVersionsMap[prod.id] = [];
      }
    });
    await Promise.all(fetchPromises);
  }

  // ======================
  //      SELECTION
  // ======================
  function isProductSelected(productId: number) {
    return selectedItems.some((item) => item.productId === productId);
  }

  function getSelectedVersion(productId: number) {
    const found = selectedItems.find((item) => item.productId === productId);
    return found ? found.version : '';
  }

  function toggleSelection(product: Product) {
    if (!product.id) return;
    const productId = product.id;

    if (isProductSelected(productId)) {
      // Remove
      selectedItems = selectedItems.filter((item) => item.productId !== productId);
    } else {
      // Add
      const versions = productVersionsMap[productId] || [];
      let defaultVersion = '';
      if (versions.length === 1) {
        defaultVersion = versions[0].version;
      }
      selectedItems = [...selectedItems, { productId, version: defaultVersion }];
    }
    saveStateToLocalStorage();
  }

  function handleVersionChange(productId: number, newVersion: string) {
    selectedItems = selectedItems.map((item) => {
      if (item.productId === productId) {
        return { ...item, version: newVersion };
      }
      return item;
    });
    saveStateToLocalStorage();
  }

  // ======================
  //       REMOVE ITEM
  // ======================
  function removeSelectedItem(productId: number) {
    const product = productMap[productId];
    if (product && isProductSelected(productId)) {
      toggleSelection(product);
    } else {
      selectedItems = selectedItems.filter((item) => item.productId !== productId);
      saveStateToLocalStorage();
    }
  }

  // ======================
  //    PRICE + DISCOUNT
  // ======================
  $: totalPrice = selectedItems.reduce((sum, sel) => {
    const versions = productVersionsMap[sel.productId] || [];
    const chosenVersion = versions.find((v) => v.version === sel.version);
    return sum + (chosenVersion?.retail_price || 0);
  }, 0);

  $: discountRate = (
    selectedItems.length >= 20 ? 0.25 :
    selectedItems.length >= 15 ? 0.20 :
    selectedItems.length >= 5  ? 0.10 :
    0
  );
  $: finalPrice = totalPrice * (1 - discountRate);

  // ======================
  //    LOCAL STORAGE
  // ======================
  function loadStateFromLocalStorage() {
    const savedItems = localStorage.getItem('selectedProductVersions');
    if (savedItems) {
      const data = JSON.parse(savedItems);
      selectedItems = data.map((x: any) => ({
        productId: +x.productId,
        version: x.version
      }));
    }
  }

  function saveStateToLocalStorage() {
    const data = selectedItems.map((x) => ({
      productId: +x.productId,
      version: x.version
    }));
    localStorage.setItem('selectedProductVersions', JSON.stringify(data));
  }

  // ======================
  //     PAGINATION
  // ======================
  async function handlePageChange(page: number) {
    currentPage = page;
    products = [];
    await fetchActiveProducts(currentPage, pageSize, searchQuery);
  }

  // ======================
  //       SEARCH
  // ======================
  async function handleSearch() {
    // Reset to page 1 when searching
    currentPage = 1;
    products = [];
    await fetchActiveProducts(currentPage, pageSize, searchQuery);
  }
</script>

<!-- ==================== -->
<!--      PAGE LAYOUT     -->
<!-- ==================== -->
<div class="p-4">
  <div class="flex-row space-between mb-4">
    <h2>Price Simulation</h2>

    <!-- SEARCH BAR -->
    <div class="search-bar">
      <input
        type="text"
        placeholder="Search products name..."
        bind:value={searchQuery}
        on:keydown={(e) => {
          // Optionally trigger search on Enter key
          if (e.key === 'Enter') handleSearch();
        }}
      />
      <button on:click={handleSearch}>Search</button>
    </div>

    <div class="receipt-container">
      <h4>Receipt</h4>
      <ul>
        {#each selectedItems as sel}
          <li>
            <strong>{productMap[sel.productId]?.name ?? 'Unknown Product'}</strong>
            {#if sel.version}
              (v{sel.version})
            {/if}
            -
            ${
              productVersionsMap[sel.productId]
                ?.find((v) => v.version === sel.version)
                ?.retail_price || 0
            }
            <button class="remove-btn" on:click={() => removeSelectedItem(sel.productId)}>
              Remove
            </button>
          </li>
        {/each}
      </ul>

      {#if discountRate > 0}
        <p>Original Price: ${totalPrice.toFixed(2)}</p>
        <p>Discount Applied: {(discountRate * 100).toFixed(0)}%</p>
        <h4>Final Price: ${finalPrice.toFixed(2)}</h4>
      {:else}
        <h4>Total Price: ${totalPrice.toFixed(2)}</h4>
      {/if}
    </div>
  </div>

  <!-- GRID OF PRODUCTS (Search + Pagination) -->
  <LayoutGrid>
    {#each products as product}
      <Cell span={4}>
        <ProductCard
          {product}
          selectable={true}
          isSelected={isProductSelected(product.id!)}
          toggleSelection={toggleSelection}
        />
        {#if isProductSelected(product.id!)}
          {#if productVersionsMap[product.id!] && productVersionsMap[product.id!].length > 0}
            <select
              class="version-dropdown"
              value={getSelectedVersion(product.id!)}
              on:change={(e) =>
                handleVersionChange(product.id!, (e.target as HTMLSelectElement).value)
              }
            >
              <option disabled value="">
                -- Select a version --
              </option>
              {#each productVersionsMap[product.id!] as ver}
                <option value={ver.version}>
                  {ver.version} — ${ver.retail_price}
                </option>
              {/each}
            </select>
          {:else}
            <p style="color: #999; margin-top: 8px;">
              No versions found for this product.
            </p>
          {/if}
        {/if}
      </Cell>
    {/each}
  </LayoutGrid>

  <!-- PAGINATION -->
  <Pagination
    {currentPage}
    pageSize={pageSize}
    totalItems={totalProducts}
    onPageChange={handlePageChange}
  />
</div>

<style>
  /* Basic layout styling */
  .flex-row {
    display: flex;
    align-items: center;
  }
  .space-between {
    justify-content: space-between;
  }
  .mb-4 {
    margin-bottom: 1rem;
  }

  /* Search bar styling */
  .search-bar {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-right: 1rem;
  }
  .search-bar input {
    padding: 0.5rem;
    font-size: 1rem;
  }
  .search-bar button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
  }

  .receipt-container {
    background: #f9f9f9;
    padding: 1em;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 300px;
    max-height: 300px;
    overflow-y: auto;
  }

  .receipt-container ul {
    list-style: none;
    padding: 0;
  }

  .receipt-container ul li {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5em;
  }

  .remove-btn {
    background: #eee;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0.25em 0.5em;
    cursor: pointer;
    font-size: 0.9rem;
    margin-left: 0.75em;
  }

  .remove-btn:hover {
    background: #ddd;
  }

  .version-dropdown {
    margin-top: 8px;
    padding: 4px;
    width: 100%;
    font-size: 0.9rem;
  }
</style>
