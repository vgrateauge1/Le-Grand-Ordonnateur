from django.db import models

from backend.models.manufacturing.manufacturing import Manufacturing


class Step(models.Model):
    name = models.CharField(max_length=255)
    manufacturing = models.ForeignKey(Manufacturing, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()  # To track the sequence of steps
    estimated_time = models.DurationField(help_text="Estimated time to complete this step")

    class Meta:
        ordering = ['order']
