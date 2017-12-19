from django.db import models

# Create your models here.
class People(models.Model):
    name = models.CharField(max_length=100)
    birthDate = models.DateField()
    rang = models.CharField(max_length=50)

    def __str__(self):
        return self.name

