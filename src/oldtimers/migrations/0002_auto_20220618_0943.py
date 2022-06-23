# Generated by Django 3.2.13 on 2022-06-18 09:43

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oldtimers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="color",
            field=colorfield.fields.ColorField(
                blank=True,
                default=None,
                image_field=None,
                max_length=18,
                null=True,
                samples=[("#FFFFFF", "white"), ("#000000", "black"), ("#808080", "gray"), ("#FF0000", "red")],
            ),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="mileage",
            field=models.PositiveBigIntegerField(
                blank=True, null=True, validators=[django.core.validators.MaxValueValidator(3000000)]
            ),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="seats",
            field=models.SmallIntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="transmission",
            field=models.PositiveSmallIntegerField(
                blank=True, choices=[(0, "Manual"), (1, "Automatic"), (2, "Other")], default=2, null=True
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="category",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "European Elite Classic"),
                    (1, "US Retro"),
                    (2, "European Legend"),
                    (3, "Fully Restored Oldtimer"),
                    (4, "US Muscle Car"),
                    (5, "Offroad Classic"),
                    (6, "Asian Legends"),
                    (7, "Rare Supercar"),
                    (8, "Deep Tuned Custom"),
                    (9, " Other"),
                ],
                default=9,
            ),
        ),
    ]