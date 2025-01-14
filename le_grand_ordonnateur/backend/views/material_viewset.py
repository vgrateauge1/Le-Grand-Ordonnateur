
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.material.material import Material
from backend.serializers import MaterialSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @action(detail=False, methods=['post'], url_path='upsert')
    def upsert(self, request):
        """
        Custom action to upsert a material (create or update).
        """
        material_id = request.data.get('id')  # Assuming `id` is provided in the request
        data = request.data

        if material_id:
            try:
                material = Material.objects.get(id=material_id)
                serializer = self.get_serializer(material, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)  # Successfully updated
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data
            except Material.DoesNotExist:
                return Response({'error': 'Material not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Create a new material
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Successfully created
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid data