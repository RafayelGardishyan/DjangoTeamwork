from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Plan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Title")
    description = models.TextField(max_length=1000, verbose_name="Description")
    deadline = models.DateField(verbose_name="Deadline")
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def slugcreator(self):
        self.slug = slugify(self.name)

    def isdead(self):
        if timezone.now().date() >= self.deadline:
            return True

    def getdeletelink(self):
        return reverse('delete-plans', args={self.slug})

    def getlink(self):
        return reverse('description-plans', args={self.slug})
