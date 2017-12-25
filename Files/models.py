import os
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploaded_files')
    added_on = models.DateField(auto_now=True)
    slug = models.CharField(max_length=100)

    def getname(self):
        self.name = self.file.name

    def saveslug(self):
        self.slug = slugify(self.name)

    def getdownloadurl(self):
        return self.file.url

    def deletefile(self):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)

    def getdeletelink(self):
        return reverse('delete-files', args=[self.slug])
