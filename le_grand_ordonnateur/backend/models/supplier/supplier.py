from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    mail = models.TextField()
    tel = models.TextField()

    def __str__(self):
        return self.name