# Generated by Django 4.2.1 on 2023-05-29 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customDBLogger", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="statuslog",
            name="custom_category",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="statuslog",
            name="user",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
