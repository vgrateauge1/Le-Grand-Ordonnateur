from django.db import models

from backend.models.product.product import Product
from backend.models.product.product_version import ProductVersion


class Manufacturing(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='manufacturings')
    version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, related_name='manufacturings')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'version'], name='unique_manufacturing')
        ]