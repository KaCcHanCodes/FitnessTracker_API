# Generated by Django 5.1.1 on 2024-10-01 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]