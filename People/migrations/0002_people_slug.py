# Generated by Django 2.0 on 2017-12-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='slug',
            field=models.CharField(default='s', max_length=100),
            preserve_default=False,
        ),
    ]