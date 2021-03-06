# Generated by Django 2.0 on 2017-12-23 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0002_people_slug'),
        ('Logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='People.People'),
        ),
        migrations.AlterField(
            model_name='log',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
