<script lang="ts">
    import Button, { Icon, Label } from "@smui/button";
    import IconButton from "@smui/icon-button";
    import Paper from "@smui/paper";
    import Textfield from "@smui/textfield";
    import Card from "@smui/card";
    import type { StepFormData, ManufacturingFormData } from '../../model/manufacturing';

    let { onSubmit, manufacturing, refresh } = $props();

    let manufacturingName = $state('');
    let defaultStep: StepFormData = {
        name: '',
        order: 0,
        estimated_time: 0
    };

    let tab = $state<StepFormData[]>([]);
    let errors = $state<{ name: boolean, estimated_time: boolean }[]>([]);

    const addStep = () => {
        tab = [...tab, { ...defaultStep, order: tab.length + 1 }];
    };

    const removeLine = (index: number) => {
        tab.splice(index, 1);
        tab = tab.map((step, idx) => ({
            ...step,
            order: idx + 1
        }));
    };

    const validateForm = () => {
        errors = [];
        let isValid = true;

        if (!manufacturingName.trim()) {
            isValid = false;
        }

        for (const step of tab) {
            const stepErrors = {
                name: !step.name.trim(),
                estimated_time: step.estimated_time <= 0
            };

            if (stepErrors.name || stepErrors.estimated_time) {
                isValid = false;
            }

            errors.push(stepErrors);
        }

        return isValid;
    };

    const handleSubmit = () => {
        if (validateForm()) {
            const formData: ManufacturingFormData = {
                name: manufacturingName,
                steps: tab.map(step => ({
                    name: step.name,
                    order: step.order,
                    estimated_time: step.estimated_time
                }))
            };
            onSubmit(formData)
                .then(() => {
                  refresh();
                });
        }
    };
</script>

<Paper elevation={2} class="p-4">
    <div class="mb-4">
            <Textfield
                label="Manufacturing Name"
                outlined
                bind:value={manufacturingName}
                class="w-full max-w-md"
            />
        </div>

        <div class="space-y-4">
            {#each tab as step, index}
                <Card class="card flex-row p-4">
                    <Textfield
                        label="Step Name"
                        outlined
                        bind:value={step.name}
                        class="m4 flex-grow"
                        invalid={errors[index]?.name}
                    />

                    <Textfield
                        label="Estimated Time (minutes)"
                        outlined
                        type="number"
                        bind:value={step.estimated_time}
                        class="m4 w-48"
                        invalid={errors[index]?.estimated_time}
                    />

                    <div class="flex items-center mx-4">
                        <span class="text-sm text-gray-500">#{step.order}</span>
                    </div>

                    <IconButton
                        class="material-icons"
                        onclick={() => removeLine(index)}
                    >
                        close
                    </IconButton>
                </Card>
            {/each}
        </div>

        <div class="flex justify-between items-center mt-4">
            <Button
                onclick={addStep}
                variant="raised"
                color="secondary"
                class="m4"
            >
                <Icon class="material-icons">add</Icon>
                <Label>Add Step</Label>
            </Button>
        </div>

        <div class="spacer"></div>

        <div class="flex-row end m4">
            <Button
                variant="unelevated"
                class="button-shaped-round"
                onclick={handleSubmit}
            >
                <Icon class="material-icons">save</Icon>
                <Label>Save Manufacturing Process</Label>
            </Button>
        </div>
</Paper>

<style>
    .card {
        margin-bottom: 1rem;
    }

    .flex-row {
        display: flex;
        align-items: center;
    }

    .end {
        justify-content: flex-end;
    }

    .spacer {
        height: 1rem;
    }

    .m4 {
        margin: 1rem;
    }
</style>