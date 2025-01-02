<script>
    import Button from '@smui/button';
    import TopAppBar, {Row, Section} from '@smui/top-app-bar'
</script>

<TopAppBar variant="static">
    <Row class="flex items-center">
        <Section >
          <Button href="/" class="text-white">LGO</Button>
        </Section>
        <div style="width: 10%"></div>
        <Section align="end" toolbar class="flex space-x-4">
          <Button href="/products" class="text-white">Products</Button>
          <Button href="/" class="text-white">Materials</Button>
          <Button href="/" class="text-white">Suppliers</Button>
        </Section>
    </Row>
</TopAppBar>
