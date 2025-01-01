
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.material.material import Material
from backend.models.material.material_supplier import MaterialSupply
from backend.models.supplier.supplier import Supplier
from backend.serializers import MaterialSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @action(detail=True, methods=['post'])
    def update_suppliers(self, request, pk=None):
        """
        Custom action to update material suppliers.
        """
        try:
            # Fetch the material using the pk from the URL
            material = Material.objects.get(pk=pk)

            # Clear existing MaterialSupply records for this material
            MaterialSupply.objects.filter(material=material).delete()

            # Get suppliers data from the request
            data = request.data

            # Add new suppliers with details
            for supplier_data in data.get('suppliers', []):
                supplier_id = supplier_data.get('supplier_id')
                quantity_ordered = supplier_data.get('quantity_ordered')
                date_ordered = supplier_data.get('date_ordered')
                progress = supplier_data.get('progress', 'pending')

                # Check if the supplier exists
                try:
                    supplier = Supplier.objects.get(id=supplier_id)

                    # Create a new MaterialSupply record
                    MaterialSupply.objects.create(
                        material=material,
                        supplier=supplier,
                        quantity_ordered=quantity_ordered,
                        date_ordered=date_ordered,
                        progress=progress,
                    )
                except Supplier.DoesNotExist:
                    return Response({'error': f'Supplier with id {supplier_id} not found.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Suppliers updated successfully.'}, status=status.HTTP_200_OK)

        except Material.DoesNotExist:
            return Response({'error': 'Material not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)