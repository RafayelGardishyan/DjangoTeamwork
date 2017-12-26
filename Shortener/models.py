from django.db import models

# Create your models here.
class Short(models.Model):
    slug = models.SlugField(max_length=100)
    link = models.URLField()