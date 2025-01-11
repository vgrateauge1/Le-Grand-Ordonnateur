from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.product.product import Product
from backend.models.product.product_material import ProductMaterial
from backend.models.product.product_version import ProductVersion
from backend.serializers import ProductMaterialSerializer, BomLineSerializer


class ProductMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer

    @action(detail=False, methods=['get'], url_path='bom/(?P<product_id>[^/.]+)')
    def get_bom(self, request, product_id=None):
        """
        Custom action to retrieve the Bill of Materials (BOM) for a specific product and version.
        """
        try:
            active_version = ProductVersion.objects.get(product_id=product_id, is_active=True)
            # Filter ProductMaterial objects by product ID and version ID
            product_materials = ProductMaterial.objects.filter(product_id=product_id, version_id= active_version.id)

            if not product_materials.exists():
                return Response(
                    [],
                    status=status.HTTP_200_OK
                )

            serializer = self.get_serializer(product_materials, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  # Successfully retrieved BOM
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='bom/(?P<product_id>[^/.]+)/upsert')
    def upsert_bom(self, request, product_id=None):
        """
        Upserts a list of BOM lines for the active version of a product.
        """
        # Get the active version of the product
        product = get_object_or_404(Product, pk=product_id)
        try:
            active_version = ProductVersion.objects.get(product=product, is_active=True)
            serializer = BomLineSerializer(data=request.data, many=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Upsert BOM lines
            bom_lines = serializer.validated_data
            for line in bom_lines:
                ProductMaterial.objects.update_or_create(
                    product=product,
                    version=active_version,
                    material_id=line['material'].id,
                    supplier_id=line['supplier'].id,
                    defaults={
                        'unit_price': line['unit_price'],
                        'quantity': line['quantity'],
                    },
                )

            return Response({"message": "BOM updated successfully."}, status=status.HTTP_200_OK)
        except ProductVersion.DoesNotExist:
            return Response(
                {"error": "No active version found for this product."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Deserialize and validate the BOM lines
