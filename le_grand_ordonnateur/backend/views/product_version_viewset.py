from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.product.product import Product
from backend.models.product.product_version import ProductVersion
from backend.serializers import ProductVersionSerializer


class ProductVersionViewSet(viewsets.ModelViewSet):
    queryset = ProductVersion.objects.all()
    serializer_class = ProductVersionSerializer
    @action(detail=False, methods=['get'], url_path='(?P<product_id>\d+)')
    def get_by_product_id(self, request, product_id=None):
        """
        Custom action to get all versions by product_id.
        """
        versions = ProductVersion.objects.filter(product_id=product_id)
        if versions.exists():
            serializer = self.get_serializer(versions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='upsert')
    def upsert(self, request):
        """
        Custom action to upsert a product version (create or update).
        Expects 'product_id', 'version', and other necessary data in the request body.
        """
        version_id = request.data.get('version')  # Assuming `id` is provided in the request
        product_id = request.data.get('product')  # Product ID must be provided
        data = request.data

        # Ensure the product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': f'Product with ID {product_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        ProductVersion.objects.filter(product_id=product_id).update(is_active=False)

        try:
            version = ProductVersion.objects.get(version = version_id, product_id=product_id)
            serializer = ProductVersionSerializer(version, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(product=product, is_active=True)
                return Response(serializer.data, status=status.HTTP_200_OK)  # Successfully updated
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data
        except ProductVersion.DoesNotExist:
            serializer = ProductVersionSerializer(data=data)
            if serializer.is_valid():
                serializer.save(product=product, is_active=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Successfully created
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data
