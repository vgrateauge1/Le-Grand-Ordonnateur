from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.models.product.product import Product
from backend.models.product.product_stock import ProductStock

@receiver(post_save, sender=Product)
def create_stock_for_product(sender, instance, created, **kwargs):
    if created:  # Si un produit est créé
        ProductStock.objects.get_or_create(product=instance, defaults={'quantity': 0})
