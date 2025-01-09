from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.product.product import Product
from backend.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['post'])
    def upsert(self, request):
        product_id = request.data.get('id')  # Assuming `id` is provided in the request
        data = request.data

        if product_id:
            # Attempt to retrieve and update the product
            try:
                product = Product.objects.get(id=product_id)
                # Use the serializer to validate and save the updated data
                serializer = ProductSerializer(product, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)  # Successfully updated
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data
            except Product.DoesNotExist:
                # Product with the given id does not exist
                return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # No `id` provided, create a new product
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Successfully created
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data


