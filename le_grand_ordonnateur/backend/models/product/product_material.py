from django.db import models

from backend.models.material.material import Material
from backend.models.product.product import Product
from backend.models.product.product_version import ProductVersion


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='materials')
    version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='products')
    quantity = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'material', 'version'], name='unique_product_material')
        ]