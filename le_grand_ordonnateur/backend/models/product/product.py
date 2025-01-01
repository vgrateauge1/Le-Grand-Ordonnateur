from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    retail_price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    version = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"

