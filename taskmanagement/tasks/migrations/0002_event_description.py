# Generated by Django 4.2.11 on 2024-04-16 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]