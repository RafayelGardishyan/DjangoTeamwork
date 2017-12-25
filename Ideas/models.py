from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Idea(models.Model):
    name = models.CharField(max_length=100, verbose_name="Title")
    description = models.TextField(max_length=1000, verbose_name="Description")
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def slugcreator(self):
        self.slug = slugify(self.name)

    def getdeletelink(self):
        return reverse('delete-ideas', args={self.slug})

    def getlink(self):
        return reverse('description-ideas', args={self.slug})
