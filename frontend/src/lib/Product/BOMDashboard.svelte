<script lang="ts">
	import Button, { Icon, Label } from "@smui/button";
	import IconButton from "@smui/icon-button";
	import Paper from "@smui/paper";
	import Textfield from "@smui/textfield";
	import type { BomLine } from "../../model/products";
	import Card from "@smui/card";
	import Select, {Option} from "@smui/select";
	import Dialog from "@smui/dialog";
	import MaterialForm from "$lib/Material/MaterialForm.svelte";
	import { upsertMaterial } from "../../api/material";
	import type { Material } from "../../model/material";
	import type { Supplier } from "../../model/supplier";
	import { upsertSupplier } from "../../api/supplier";
	import SupplierForm from "$lib/Supplier/SupplierForm.svelte";

    let {materials, suppliers, refresh, onSubmit, bomLines } = $props()
    let defaultBomLine: BomLine = { material: -1, supplier: -1, unit_price: 0, quantity: 0 }

    let tab = [...bomLines] 
    // dialogs
    let openMaterial: boolean = $state(false)
    let openSupplier: boolean = $state(false)
    let sM, sS = null

    let errors : { material: boolean; supplier: boolean; unit_price: boolean; quantity: boolean; }[] = $state([])
    
    const saveMaterial = (material: Material) =>{
        upsertMaterial(material)
            .then(()=>{
                refresh()
                openMaterial=false
            });
    }

    const saveSupplier = (supplier: Supplier) =>{
        upsertSupplier(supplier)
            .then(()=>{
                refresh()
                openSupplier=false
            }
        );
    }
    

    const addLine = () => {
        tab.push(defaultBomLine)
    };

    const removeLine = (index: number) => {
        tab.splice(index, 1);
    };

    const calculateLineTotal = (line : BomLine) => {
        try{
            const unitPrice = parseFloat(line.unit_price.toString());
            const quantity =  parseFloat(line.quantity.toString());
            return unitPrice * quantity;
        }catch(e){
            return 0;
        }
    };

    const calculateTotal = () => {
        let total = 0;
        for(let line of tab) {
            total += calculateLineTotal(line);
        };
        return total;
    };

    function tryParseFloat(value: string, defaultValue = 0) {
        const parsed = parseFloat(value);
        return isNaN(parsed) ? defaultValue : parsed;
    }

    function tryParseInt(value: string, defaultValue = 0) {
        const parsed = parseInt(value);
        return isNaN(parsed) ? defaultValue : parsed;
    }

    const validateBom = () => {
        errors = []
        let error = true
        for(let line of tab) {
            let check = {material:true, supplier: true, unit_price: true, quantity: true}
            line.unit_price=tryParseFloat(`${line.unit_price}`,-1)
            line.quantity=tryParseInt(`${line.quantity}`,-1)
            if (typeof line.material !== 'number' || line.material < 0) {
                check.material = false
                error = false
            }
            if (typeof line.supplier !== 'number' || line.supplier < 0) {
                check.supplier = false
                error = false
            }
            if (line.unit_price < 0) {

                check.unit_price = false
                error = false
            }
            if (line.quantity < 0) {
                check.quantity = false
                error = false
            }
            errors.push(check)
        };
        return error
    }   

    const handleSubmit = ()=>{
        if(validateBom()){
            errors=[]
            onSubmit(tab)
        }
    }
</script>

<Paper elevation={2} class="p-4">
    <div class="flex-row end m4">
        <Button onclick={()=>openMaterial=true} variant="raised" color="primary" class="m4">
            <Icon class="material-icons" >add</Icon>Material
        </Button>
        <Button onclick={()=>openSupplier=true} variant="raised" color="primary" class="m4">
            <Icon class="material-icons" >add</Icon>Supplier
        </Button>
    </div>
    <div class="spacer"></div>
    <div>
        {#each tab as line, index}
          <Card class="card flex-row ">
            <!-- Material Input -->
            <Select bind:value={line.material} label="Material" class="m4" invalid={!!errors[index]?.quantity}>
                <Option value={-1}></Option>
                {#each materials as m}
                    <Option value={m.id}>{m.name}</Option>
                {/each}
            </Select>

            <!-- Supplier Input -->
            <Select bind:value={line.supplier} label="Supplier" class="m4" invalid={!!errors[index]?.quantity}>
                <Option value={-1}></Option>
                {#each suppliers as s}
                    <Option value={s.id}>{s.name}</Option>
                {/each}
            </Select>
    
            <!-- Unit Price Input -->
            <Textfield label="Unit Price" outlined bind:value={line.unit_price} class="m4" invalid={!!errors[index]?.quantity}></Textfield>
    
            <!-- Quantity Input -->
            <Textfield label="Quantity" outlined type="number" bind:value={line.quantity} class="m4" invalid={!!errors[index]?.quantity}></Textfield>

            <Textfield label="Total" outlined disabled style = "width:180px;" class="m4"  value={calculateLineTotal(line)} />

            <!-- Remove Button -->
            <IconButton class="material-icons" onclick={()=>removeLine(index)}>close</IconButton>


          </Card>
        {/each}
    </div>
    <div class="flex-row space-between">
        <Button onclick={addLine} variant="raised" color="secondary" class="m4">
            <Icon class="material-icons" >add</Icon>Line
        </Button>
        <Textfield
            label="Grand Total"
            outlined
            disabled
            value={calculateTotal()}
            style = "width:180px;"

        />
    </div>
    <div class="spacer"></div>
    <div class="flex-row end m4">
        <Button variant="unelevated" type="submit" class="button-shaped-round" onclick={()=>handleSubmit()}>
            <Icon class="material-icons">save</Icon>
            <Label>Save</Label>
        </Button>
    </div>
</Paper>

<Dialog
  bind:open={openMaterial}
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
    <MaterialForm id={sM} onSubmit={saveMaterial}/>
</Dialog>

<Dialog
  bind:open={openSupplier}
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
    <SupplierForm id={sS} onSubmit={saveSupplier}/>
</Dialog>