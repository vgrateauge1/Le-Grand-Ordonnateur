from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Column, Task
from .serializers import ColumnSerializer, TaskSerializer

def accueil(request):
    return render(request, 'accueil.html')


class ColumnViewSet(ModelViewSet):
    queryset = Column.objects.all().order_by('position')
    serializer_class = ColumnSerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by('position')
    serializer_class = TaskSerializer
