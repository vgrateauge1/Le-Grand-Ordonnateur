from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import Column, Task
from .serializers import ColumnSerializer, TaskSerializer

def accueil(request):
    return render(request, 'accueil.html')


class ColumnViewSet(ModelViewSet):
    queryset = Column.objects.all().order_by('position')
    serializer_class = ColumnSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def perform_update(self, serializer):
        print("Données reçues pour la mise à jour de la tâche :", serializer.validated_data)  # Affiche les données reçues
        serializer.save()
