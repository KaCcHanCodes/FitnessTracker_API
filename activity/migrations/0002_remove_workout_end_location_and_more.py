# Generated by Django 5.1.1 on 2024-10-02 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='end_location',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='start_location',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='workout',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]