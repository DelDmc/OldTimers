# Generated by Django 3.2.13 on 2022-05-15 10:50

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oldtimers", "0013_alter_retailer_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="retailer",
            name="country",
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name="retailer",
            name="service_fee",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=1.0,
                max_digits=19,
                validators=[django.core.validators.MinValueValidator(1.0)],
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="brand",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="condition",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "Excellent"),
                    (1, "Very Good"),
                    (2, "Good"),
                    (3, "Satisfactory"),
                    (4, "Poor"),
                    (5, "Out of order"),
                    (6, "Other"),
                ],
                default=6,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="description",
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="image",
            field=models.ImageField(blank=True, default="default.png", null=True, upload_to="media/vehicle"),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=19,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("1"))],
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="production_year",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(2000),
                    django.core.validators.MinValueValidator(1900),
                ],
                verbose_name="year",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="retailer",
            field=models.ForeignKey(
                blank=True,
                default=1,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="vehicles",
                to="oldtimers.retailer",
            ),
        ),
    ]
