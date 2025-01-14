from django.contrib import admin

from backend.models.Kanban.Column import Column
from backend.models.Kanban.Task import Task

# Register your models here.

admin.site.register(Column)
admin.site.register(Task)