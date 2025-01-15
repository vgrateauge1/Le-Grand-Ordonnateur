from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.models.product.product_stock import ProductStock
from backend.models.product.product import Product
from backend.serializers import ProductStockSerializer

from rest_framework.decorators import action

class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = ProductStock.objects.all()
    serializer_class = ProductStockSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 0)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        stock, created = ProductStock.objects.get_or_create(product=product)
        stock.quantity = quantity
        stock.save()
        return Response(ProductStockSerializer(stock).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests to fetch stock information for a specific product.
        """
        try:
            stock = self.queryset.get(product_id=pk)
            serializer = self.serializer_class(stock)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductStock.DoesNotExist:
            return Response({"detail": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
