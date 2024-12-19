from django.db import models

class Column(models.Model):
    name = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="tasks")
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
