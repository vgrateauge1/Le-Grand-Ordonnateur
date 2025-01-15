from django.db import models
from backend.models.product.product import Product

class ProductStock(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='stock',
        primary_key=True
    )
    quantity = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Stock"
        verbose_name_plural = "Product Stocks"

    def __str__(self):
        return f"Stock for {self.product.name}: {self.quantity}"

    def increase_stock(self, amount):
        if amount < 0:
            raise ValueError("Increase amount must be positive.")
        self.quantity += amount
        self.save()

    def decrease_stock(self, amount):
        if amount < 0:
            raise ValueError("Decrease amount must be positive.")
        if amount > self.quantity:
            raise ValueError("Insufficient stock to decrease.")
        self.quantity -= amount
        self.save()
