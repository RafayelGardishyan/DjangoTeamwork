from django.db import models
from People.models import People

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Task", null=True, blank=True)
    user = models.ForeignKey(People, on_delete=models.CASCADE, null=True, blank=True)
    date = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

