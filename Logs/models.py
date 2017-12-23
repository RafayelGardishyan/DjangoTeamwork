from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify
from People.models import People

class Log(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    user = models.ForeignKey(People, on_delete=models.CASCADE, null=True, blank=True)
    added = models.DateField(auto_now=True)
    slug = models.CharField(unique=True, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    def slugcreator(self):
        self.slug = slugify(self.title)


    def getdeletelink(self):
        return reverse('delete-logs', args={self.slug})

    def getlink(self):
        return reverse('view-logs', args={self.slug})
