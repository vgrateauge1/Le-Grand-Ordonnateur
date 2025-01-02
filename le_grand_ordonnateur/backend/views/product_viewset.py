from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.material.material import Material
from backend.models.product.product import Product
from backend.models.product.product_material import ProductMaterial
from backend.models.product.product_version import ProductVersion
from backend.serializers import ProductSerializer, ProductMaterialSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['post'])
    def upsert(self, request):
        """
        Custom action to create or update a product (upsert).
        """
        product_id = request.data.get('id')  # Assuming `id` is provided in the request
        data = request.data

        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                serializer = ProductSerializer(product, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_product_material(self, request, pk=None):
        """
        Custom action to add ProductMaterial for a specific version of the product.
        """
        try:
            # Fetch the product using the pk from the URL
            product = Product.objects.get(pk=pk)

            # Ensure the version matches the requested version
            requested_version = request.data.get('version')
            if product.version != requested_version:
                return Response(
                    {'error': 'Product version mismatch.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Retrieve the material and quantity from the request data
            material_id = request.data.get('material_id')
            quantity = request.data.get('quantity')

            # Ensure the material exists
            try:
                material = Material.objects.get(id=material_id)
            except Material.DoesNotExist:
                return Response(
                    {'error': 'Material not found.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the ProductMaterial linking the Product and Material
            product_material = ProductMaterial.objects.create(
                product=product,
                material=material,
                quantity=quantity
            )

            return Response(
                {'message': 'ProductMaterial added successfully.'},
                status=status.HTTP_201_CREATED
            )

        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def set_active_version(self, request, pk=None):
        """
        Custom action to set the active version of a product.
        Requires version to set the active version of the product by ID.
        """
        product_id = pk  # The product ID is now passed as part of the URL
        version = request.data.get('version')

        if not version:
            return Response(
                {'error': 'Version is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the product by its ID
            product = Product.objects.get(id=product_id)

            # Check if the requested version exists for this product
            product_version = ProductVersion.objects.filter(product=product, version=version).first()
            if not product_version:
                return Response(
                    {'error': 'Product version not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Set is_active to True for the requested version, and False for others
            ProductVersion.objects.filter(product=product).update(is_active=False)
            product_version.is_active = True
            product_version.save()

            # Optionally, set the is_active flag for the product itself
            product.is_active = True
            product.save()

            return Response(
                {'message': 'Active product version set successfully.'},
                status=status.HTTP_200_OK
            )

        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )