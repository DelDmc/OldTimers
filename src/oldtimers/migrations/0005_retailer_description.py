# Generated by Django 3.2.13 on 2022-06-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oldtimers", "0004_alter_vehicle_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="retailer",
            name="description",
            field=models.TextField(blank=True, max_length=500, verbose_name="description"),
        ),
    ]