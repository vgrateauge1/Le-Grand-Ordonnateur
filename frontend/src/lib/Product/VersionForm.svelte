<script lang="ts">
    import Textfield from '@smui/textfield';
    import Button from '@smui/button';
    import Card, { Content, Actions } from '@smui/card';
	  import type { Version } from '../../model/products';
    import Select, {Option} from '@smui/select'

  


    export let onSubmit: (version: Version) => void;
    export let versions: Version[] = [];
    export let version: Version

    let vl = versions.map(x=>x.version)
    vl.push('other')
    let selected = version.version
    let price = version.retail_price ?? 0
  
    let errors: Partial<Record<keyof Version, string>> = {};
  
    function validateForm(): boolean {
      errors = {};
  
      if (version.version=='' ||version.version=='other') {
        errors.version = 'Version is required';
      }
  
      if (version.retail_price <= 0) {
        errors.retail_price = 'Price must be greater than 0';
      }
  
      return Object.keys(errors).length === 0;
    }
  
    function handleSubmit() {
      if (validateForm()) {
        onSubmit({version:selected=='other'?version.version:selected, retail_price:version.retail_price, product:version.product, is_active:true} as Version);
      }
    }
  
    function handlePriceInput(event: Event) {
      const input = event.target as HTMLInputElement;
      const value = input.value.replace(/[^\d.]/g, '');
      const parts = value.split('.');
      const formatted = parts[0] + (parts[1] ? '.' + parts[1].slice(0, 2) : '');
      version.retail_price = Number(formatted);
    }
</script>
  
  <Card class="product-version-form">
    <Content>
      <form on:submit|preventDefault={handleSubmit}>
        <div class="form-field flex-row">
            <Select bind:value={selected} label="Version">
                {#each vl as v}
                    <Option value={v}>{v}</Option>
                {/each}
            </Select>
            {#if selected === 'other'}
            <Textfield
              style="margin-left: 10px"
              label="New version"
              bind:value={version.version}
              placeholder="Enter a new version"
              required
              invalid={!!errors.version}
            >
            </Textfield>
          {/if}
        </div>
  
        <div class="form-field">
          <Textfield
            label="Retail Price"
            required
            bind:value={version.retail_price}
            oninput={handlePriceInput}
            invalid={!!errors.retail_price}
          >
          </Textfield>
        </div>
  
        <Actions>
          <Button variant="raised" type="submit">
            <span class="mdc-button__label">Save</span>
          </Button>
        </Actions>
      </form>
    </Content>
  </Card>
  
  <style>
    .product-version-form {
      max-width: 500px;
      margin: 1rem auto;
    }
  
    .form-title {
      margin-bottom: 1.5rem;
      font-size: 1.25rem;
      font-weight: 500;
    }
  
    .form-field {
      margin-bottom: 1.5rem;
    }
  
    :global(.mdc-text-field) {
      width: 100%;
    }
  </style>