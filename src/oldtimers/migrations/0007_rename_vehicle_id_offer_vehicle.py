# Generated by Django 3.2.13 on 2022-05-14 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("oldtimers", "0006_alter_vehicle_vin"),
    ]

    operations = [
        migrations.RenameField(
            model_name="offer",
            old_name="vehicle_id",
            new_name="vehicle",
        ),
    ]