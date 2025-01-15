from datetime import timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from backend.models.manufacturing.manufacturing import Manufacturing
from backend.models.manufacturing.step import Step
from backend.models.product.product import Product
from backend.models.product.product_stock import ProductStock
from backend.serializers import ManufacturingSerializer, ProductStockSerializer


class ManufacturingViewSet(viewsets.ModelViewSet):
    queryset = Manufacturing.objects.all()
    serializer_class = ManufacturingSerializer
    product_stock_serializer_class = ProductStockSerializer

    @action(detail=False, methods=['get'], url_path='(?P<product_id>[^/.]+)')
    def get_manufacturing(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        version = product.versions.get(is_active=True)

        try:
            manufacturing = Manufacturing.objects.get(
                product=product,
                version=version
            )
            return Response(
                self.serializer_class(manufacturing).data,
                status=status.HTTP_200_OK
            )
        except Manufacturing.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='(?P<product_id>[^/.]+)/upsert')
    @transaction.atomic
    def upsert(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)

        # Get the latest product version
        version = product.versions.get(is_active=True)

        # Try to get existing manufacturing for this product version
        try:
            manufacturing = Manufacturing.objects.get(
                product=product,
                version=version
            )
        except Manufacturing.DoesNotExist:
            manufacturing = Manufacturing(
                product=product,
                version=version
            )

        # Update manufacturing data
        manufacturing.name = request.data.get('name')
        manufacturing.save()

        # Delete existing steps to replace with new ones
        manufacturing.steps.all().delete()

        # Create new steps
        for index, step_data in enumerate(request.data.get('steps', [])):
            Step.objects.create(
                manufacturing=manufacturing,
                name=step_data['name'],
                order=index,
                estimated_time=timedelta(minutes=step_data.get('estimated_time', 0))
            )

        # Return serialized data
        return Response(
            self.serializer_class(manufacturing).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['put'], url_path='(?P<product_id>[^/.]+)/increment')
    def increment_stock(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)

        try:
            with transaction.atomic():
                # Get or create the product stock
                product_stock, created = ProductStock.objects.get_or_create(
                    product=product,
                    defaults={'quantity': 0}
                )

                product_stock.quantity += 1
                product_stock.save()

            return Response(
                self.product_stock_serializer_class(product_stock).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
