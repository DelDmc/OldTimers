import uuid as uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Vehicle(models.Model):
    YEAR_OF_PRODUCTION_MIN_YEAR = 1900
    YEAR_OF_PRODUCTION_MAX_YEAR = 2000

    class VEHICLE_CATEGORY_CHOICES(models.IntegerChoices):
        LUXURY = 0, "Lux Class"
        SPORT = 1, "Sport Class"
        SUV = 2, " SUV Class"
        MOTORCYCLE = 3, "Moto"
        RACE = 4, "Race Class"
        OTHER = 5, " Other"

    class VEHICLE_CONDITION_CHOICES(models.IntegerChoices):
        EXCELLENT = 0, "Excellent"
        VERY_GOOD = 1, "Very Good"
        GOOD = 2, "Good"
        SATISFACTORY = 3, "Satisfactory"
        POOR = 4, "Poor"
        OUT_OF_ORDER = 5, "Out of order"
        OTHER = 6, "Other"

    owner = models.ForeignKey(get_user_model(), related_name="vehicle", on_delete=models.CASCADE)
    retailer = models.ForeignKey(to="oldtimers.Retailer", related_name="vehicle", on_delete=models.CASCADE)
    vin = models.CharField(null=False, blank=False, unique=True, max_length=17, primary_key=True)
    category = models.PositiveSmallIntegerField(
        choices=VEHICLE_CATEGORY_CHOICES.choices, default=VEHICLE_CATEGORY_CHOICES.OTHER, null=False, blank=False
    )
    brand = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
    model = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
    production_year = models.IntegerField(
        _("year"),
        validators=[MaxValueValidator(YEAR_OF_PRODUCTION_MAX_YEAR), MinValueValidator(YEAR_OF_PRODUCTION_MIN_YEAR)],
    )
    condition = models.PositiveSmallIntegerField(
        choices=VEHICLE_CONDITION_CHOICES.choices, default=VEHICLE_CONDITION_CHOICES.OTHER
    )
    image = models.ImageField(default="default.png", upload_to="media/vehicle")
    price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)


class Retailer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    company_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    mobile = PhoneNumberField(blank=False, null=False, unique=True)
    email = models.EmailField(max_length=128)
    address = models.CharField(_("address"), max_length=128)
    city = models.CharField(
        _("city"),
        max_length=64,
    )
    country = CountryField(blank=False, null=False)
    zip_code = models.CharField(_("zip code"), max_length=5)


class Offer(models.Model):
    pass


class Employee(models.Model):
    retailer = models.ForeignKey(to="oldtimers.Retailer", related_name="employees", on_delete=models.CASCADE)


class DeliveryService(models.Model):
    pass


class Invoices(models.Model):
    pass


class InvoiceItems(models.Model):
    vehicle = models.ForeignKey(to="oldtimers.Retailer", related_name="invoice_items", on_delete=models.CASCADE)
    delivery_service = models.ForeignKey(
        to="oldtimers.DeliveryService", related_name="delivery_services", on_delete=models.CASCADE
    )
