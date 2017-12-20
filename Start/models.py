from django.db import models

# Create your models here.
class Admin(models.Model):
    password = models.CharField(max_length=20)
