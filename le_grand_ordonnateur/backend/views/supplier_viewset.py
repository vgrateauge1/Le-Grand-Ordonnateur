from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.supplier.supplier import Supplier
from backend.serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    @action(detail=False, methods=['post'], url_path='upsert')
    def upsert(self, request):
        """
        Custom action to upsert a supplier (create or update).
        """
        supplier_id = request.data.get('id')  # Assuming `id` is provided in the request
        data = request.data

        if supplier_id:
            try:
                # Update existing supplier
                supplier = Supplier.objects.get(id=supplier_id)
                serializer = self.get_serializer(supplier, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)  # Successfully updated
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data
            except Supplier.DoesNotExist:
                return Response({'error': 'Supplier not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Create a new supplier
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Successfully created
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data