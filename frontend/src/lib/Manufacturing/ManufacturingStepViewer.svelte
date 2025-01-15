<script lang="ts">
    import type { Manufacturing, Step } from '../../model/manufacturing';
    import Paper, { Title, Content } from '@smui/paper';
    import Button, { Label } from '@smui/button';
    import Checkbox from '@smui/checkbox';
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';
    import FormField from '@smui/form-field';
    import { onDestroy } from 'svelte';

    let { manufacturing }: { manufacturing: Manufacturing } = $props();

    interface StepState {
        order: number;
        timeRemaining: number;
        isRunning: boolean;
        isCompleted: boolean;
    }

    let stepStates: StepState[] = $state([]);
    let intervals = $state<{ [key: number]: number }>({});
    let allStepsCompleted = $derived(stepStates.length > 0 && stepStates.every(state => state.isCompleted));

    function handleSubmit() {
        console.log('here');
    }

    function parseTimeToSeconds(timeStr: string): number {
        const [hours, minutes, seconds] = timeStr.split(':').map(Number);
        return (hours * 3600) + (minutes * 60) + seconds;
    }

    function formatTime(totalSeconds: number): string {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        return [hours, minutes, seconds]
            .map(val => val.toString().padStart(2, '0'))
            .join(':');
    }

    // Initialize step states
    $effect(() => {
        stepStates = manufacturing.steps.map(step => ({
            order: step.order,
            timeRemaining: parseTimeToSeconds(step.estimated_time),
            isRunning: false,
            isCompleted: false
        }));
    });

    function updateStepState(stepState: StepState) {
        stepStates = stepStates.map(state =>
            state.order === stepState.order ? stepState : state
        );
    }

    function getStepState(order: number): StepState | undefined {
        return stepStates.find(state => state.order === order);
    }

    function toggleTimer(step: Step) {
        const state = getStepState(step.order);
        if (!state) return;

        if (state.isRunning) {
            // Stop timer
            if (intervals[step.order]) {
                clearInterval(intervals[step.order]);
                delete intervals[step.order];
            }

            updateStepState({
                ...state,
                isRunning: false
            });
        } else {
            // Start timer
            const intervalId = window.setInterval(() => {
                const currentState = getStepState(step.order);
                if (!currentState) return;

                if (currentState.timeRemaining <= 0) {
                    clearInterval(intervalId);
                    delete intervals[step.order];
                    updateStepState({
                        ...currentState,
                        isRunning: false
                    });
                    return;
                }

                updateStepState({
                    ...currentState,
                    timeRemaining: currentState.timeRemaining - 1
                });
            }, 1000);

            intervals[step.order] = intervalId;
            updateStepState({
                ...state,
                isRunning: true
            });
        }
    }

    function completeStep(step: Step) {
        const state = getStepState(step.order);
        if (!state) return;

        if (intervals[step.order]) {
            clearInterval(intervals[step.order]);
            delete intervals[step.order];
        }

        updateStepState({
            ...state,
            isCompleted: true,
            isRunning: false
        });
    }

    // Cleanup intervals on component unmount
    onDestroy(() => {
        Object.values(intervals).forEach(clearInterval);
    });
</script>

<Paper elevation={1}>
    <Title>{manufacturing.name}</Title>
    <Content>
        <DataTable style="width: 100%;">
            <Head>
                <Row>
                    <Cell>Step Name</Cell>
                    <Cell>Timer</Cell>
                    <Cell>Controls</Cell>
                    <Cell>Status</Cell>
                </Row>
            </Head>
            <Body>
                {#each manufacturing.steps as step}
                    {@const state = getStepState(step.order)}
                    {#if state}
                        <Row>
                            <Cell>{step.name}</Cell>
                            <Cell>
                                <span class="mdc-typography--body2">
                                    {formatTime(state.timeRemaining)}
                                </span>
                            </Cell>
                            <Cell>
                                <Button
                                    variant="raised"
                                    onclick={() => toggleTimer(step)}
                                    disabled={state.isCompleted}
                                >
                                    <Label>{state.isRunning ? 'Pause' : 'Start'}</Label>
                                </Button>
                            </Cell>
                            <Cell>
                                <FormField>
                                    <Checkbox
                                        bind:checked={state.isCompleted}
                                        onclick={() => completeStep(step)}
                                        disabled={state.isCompleted}
                                    />
                                </FormField>
                            </Cell>
                        </Row>
                    {/if}
                {/each}
            </Body>
        </DataTable>
        <div class="submit-container">
            <Button
                variant="raised"
                color="primary"
                onclick={handleSubmit}
                disabled={!allStepsCompleted}
            >
                <Label>Submit</Label>
            </Button>
        </div>
    </Content>
</Paper>

<style>
    :global(.mdc-data-table) {
        width: 100%;
    }

    :global(.mdc-data-table__row) {
        height: 72px !important;
    }

    :global(.mdc-data-table__cell) {
        padding: 0 24px !important;
    }

    .submit-container {
        display: flex;
        justify-content: flex-end;
        padding: 24px;
    }
</style>