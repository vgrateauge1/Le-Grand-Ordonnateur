from django.db import models

from backend.models.material.material import Material
from backend.models.supplier.supplier import Supplier


class MaterialSupply(models.Model):
    # Foreign keys to link material and supplier
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    # Additional fields
    quantity_ordered = models.FloatField()
    date_ordered = models.DateField()

    # Progress of the order
    ORDER_PROGRESS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    progress = models.CharField(
        max_length=10, choices=ORDER_PROGRESS_CHOICES, default='pending'
    )

    def __str__(self):
        return f"{self.material.name} from {self.supplier.name} - {self.progress}"

    class Meta:
        # Add constraints to ensure that each combination of material and supplier is unique
        unique_together = ('material', 'supplier', 'date_ordered')