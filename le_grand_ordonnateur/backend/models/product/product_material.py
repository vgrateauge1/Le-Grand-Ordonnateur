from django.db import models

from backend.models.material.material import Material
from backend.models.product.product import Product
from backend.models.product.product_version import ProductVersion
from backend.models.supplier.supplier import Supplier


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, related_name='product_materials')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'material', 'version'], name='unique_product_material')
        ]