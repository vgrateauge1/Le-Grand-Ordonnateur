from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock_quantity = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.stock_quantity})"