from rest_framework import viewsets

from backend.models.Kanban.Task import Task
from backend.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_update(self, serializer):
        print("Données reçues pour la mise à jour de la tâche :",
              serializer.validated_data)  # Affiche les données reçues
        serializer.save()