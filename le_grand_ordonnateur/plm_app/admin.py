from django.contrib import admin
from .models import Column, Task

# Enregistrement des modèles
admin.site.register(Column)
admin.site.register(Task)