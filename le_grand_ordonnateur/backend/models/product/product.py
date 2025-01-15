from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    quantity = models.FloatField(default=0)  # Nouveau champ pour le stock
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


