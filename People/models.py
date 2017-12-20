from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class People(models.Model):
    name = models.CharField(max_length=100)
    birthDate = models.DateField()
    rang = models.CharField(max_length=50)
    secretKey = models.CharField(max_length=5, verbose_name="Secret Key")
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def saveslug(self, slug):
        self.slug = slugify(slug)

    def getdeletelink(self):
        return reverse('people', args=[self.slug])

