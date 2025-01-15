from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch

from backend.models.product.product import Product
from backend.models.product.product_version import ProductVersion
from backend.serializers import ProductSerializer


# Custom Pagination Class (Define it here)
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # Allow 'size' as a query parameter
    max_page_size = 100  # Optional: Set a maximum number of products per page


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination  # Use the custom pagination class

    @action(detail=False, methods=['get'])
    def active(self, request):

        # Filter active products
        products_with_active_versions = Product.objects.filter(is_active=True)

        # Search feature with the name of the product
        search_query = request.query_params.get('search', None)
        if search_query:
            products_with_active_versions = products_with_active_versions.filter(name__icontains=search_query)

        # Apply pagination
        page = self.paginate_queryset(products_with_active_versions)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'include_versions': True})
            return self.get_paginated_response(serializer.data)

        # If pagination is not applied, return all products (fallback)
        serializer = self.get_serializer(products_with_active_versions, many=True, context={'include_versions': True})
        return Response(serializer.data, status=status.HTTP_200_OK)

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
