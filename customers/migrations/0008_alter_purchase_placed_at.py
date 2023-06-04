# Generated by Django 4.2.1 on 2023-06-04 01:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0007_alter_customer_id_alter_purchase_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase",
            name="placed_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="placed"
            ),
        ),
    ]
