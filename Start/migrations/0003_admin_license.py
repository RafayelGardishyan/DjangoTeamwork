# Generated by Django 2.0 on 2017-12-26 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Start', '0002_admin_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='license',
            field=models.CharField(default='rgardishyan@gmail.com', max_length=20),
            preserve_default=False,
        ),
    ]
