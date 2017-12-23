from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploaded_files')
    added_on = models.DateField(auto_now=True)

    def getname(self):
        self.name = self.file.name

    def getdownloadurl(self):
        return self.file.path
