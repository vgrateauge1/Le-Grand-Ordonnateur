from django.db import models

from backend.models.product.product import Product


class ProductVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="versions")
    version = models.CharField(max_length=50)
    retail_price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)  # Whether this version is the active one

    class Meta:
        # Using a composite key by enforcing unique constraint on product and version fields
        constraints = [
            models.UniqueConstraint(fields=['product', 'version'], name='unique_product_version')
        ]

    def __str__(self):
        return f"{self.product.name} (v{self.version})"
