from rest_framework.viewsets import ModelViewSet

from backend.models.Kanban.Column import Column
from backend.serializers import ColumnSerializer


class ColumnViewSet(ModelViewSet):
    queryset = Column.objects.all().order_by('position')
    serializer_class = ColumnSerializer
