from django.db import models

from backend.models.Kanban.Column import Column


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="tasks")
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title