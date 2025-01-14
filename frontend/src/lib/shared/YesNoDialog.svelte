<script lang="ts">
  import Dialog, { Title, Content, Actions } from '@smui/dialog';
  import Button from '@smui/button';

  export let open = false;
  export let title = 'Confirm Action';
  export let message = 'Are you sure you want to proceed?';
  export let onConfirm: () => void;
  export let onCancel: () => void = () => { open = false; };
  export let confirmText = 'Yes';
  export let cancelText = 'No';
</script>

<Dialog
  bind:open
  aria-labelledby="confirm-dialog-title"
  aria-describedby="confirm-dialog-content"
  scrimClickAction=""
  escapeKeyAction=""
>
  <Title id="confirm-dialog-title">{title}</Title>
  <Content id="confirm-dialog-content">{message}</Content>
  <Actions>
    <Button onclick={onCancel} variant="outlined">
      <span class="mdc-button__label">{cancelText}</span>
    </Button>
    <Button onclick={onConfirm} variant="raised">
      <span class="mdc-button__label">{confirmText}</span>
    </Button>
  </Actions>
</Dialog>