from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.FloatField()


    def __str__(self):
        return f"{self.name} ({self.unit_price})"