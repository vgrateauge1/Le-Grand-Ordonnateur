from rest_framework import viewsets

from backend.models.supplier.supplier import Supplier
from backend.serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
