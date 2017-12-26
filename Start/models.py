from django.core.mail import send_mail
from django.db import models

# Create your models here.
class Admin(models.Model):
    password = models.CharField(max_length=20)
    email = models.EmailField()
    license = models.CharField(max_length=20)

    def sendemail(self, subject, message):
        send_mail(subject, message, 'codeniacs@gmail.com', [self.email,], fail_silently=False)
