import uuid as uuid

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

    owner = models.ForeignKey(
        get_user_model(),
        related_name="vehicle",
        on_delete=models.CASCADE
    )
    retailer = models.ForeignKey(
        to="oldtimers.Retailer",
        related_name="vehicle",
        on_delete=models.CASCADE
    )
    vin = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=17,
        primary_key=True
    )
    category = models.PositiveSmallIntegerField(
        choices=VEHICLE_CATEGORY_CHOICES.choices,
        default=VEHICLE_CATEGORY_CHOICES.OTHER,
        null=False,
        blank=False,
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
        validators=[
            MaxValueValidator(YEAR_OF_PRODUCTION_MAX_YEAR),
            MinValueValidator(YEAR_OF_PRODUCTION_MIN_YEAR)
        ],
    )
    condition = models.PositiveSmallIntegerField(
        choices=VEHICLE_CONDITION_CHOICES.choices,
        default=VEHICLE_CONDITION_CHOICES.OTHER
    )
    image = models.ImageField(
        default="default.png",
        upload_to="media/vehicle"
    )
    price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=500,
        null=False,
        blank=False,
    )


class Retailer(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        db_index=True,
        unique=True
    )
    company_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True
    )
    mobile = PhoneNumberField(
        blank=False,
        null=False,
        unique=True
    )
    email = models.EmailField(
        max_length=128
    )
    address = models.CharField(
        _("address"),
        max_length=128
    )
    city = models.CharField(
        _("city"),
        max_length=64,
    )
    country = CountryField(
        blank=False,
        null=False
    )
    zip_code = models.CharField(
        _("zip code"),
        max_length=5
    )


class Offer(models.Model):
    retailer = models.ForeignKey(
        to="oldtimers.Retailer",
        related_name="offers",
        on_delete=models.CASCADE
    )
    vehicle_id = models.OneToOneField(
        to="oldtimers.Vehicle",
        related_name="offers",
        on_delete=models.CASCADE,
    )
    offer_price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )


class Employee(models.Model):
    class EMPLOYEE_RANK_CHOICES(models.IntegerChoices):
        CEO = 0, "Chief Executive Officer"
        GENERAL_MANAGER = 1, "General Manager / Administrator"
        SALES_MANAGER = 2, "Sales Manager"

    retailer = models.ForeignKey(
        to="oldtimers.Retailer",
        related_name="employees",
        on_delete=models.CASCADE
    )
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    first_name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
    )
    rank = models.PositiveSmallIntegerField(
        choices=EMPLOYEE_RANK_CHOICES.choices,
        default=EMPLOYEE_RANK_CHOICES.SALES_MANAGER
    )
    email = models.EmailField(
        max_length=128,
        null=False,
        blank=False,
    )


class DeliveryService(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        db_index=True,
        unique=True
    )
    company_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )
    mobile = PhoneNumberField(
        null=False,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        max_length=128,
        null=False,
        blank=False,
    )
    address = models.CharField(
        _("address"),
        max_length=128,
        null=False,
        blank=False,
    )
    city = models.CharField(
        _("city"),
        max_length=64,
        null=False,
        blank=False,
    )
    country = CountryField(
        null=False,
        blank=False,
    )
    zip_code = models.CharField(
        _("zip code"),
        max_length=5,
        null=False,
        blank=False,
    )
    international_delivery = models.BooleanField(
        default=False
    )


class Invoices(models.Model):
    invoice_date = models.DateTimeField(
        null=False,
        blank=False,
    )
    billing_address = models.CharField(
        _("address"),
        max_length=128,
        default="N/A"
    )
    billing_city = models.CharField(
        _("city"),
        max_length=64,
    )
    billing_country = CountryField(
        null=False,
        blank=False,
    )
    billing_zip_code = models.CharField(
        _("zip code"),
        max_length=5,
        null=False,
        blank=False,
    )
    total = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )


class InvoiceItems(models.Model):
    vehicle = models.ForeignKey(
        to="oldtimers.Vehicle",
        related_name="invoice_items_vehicle",
        on_delete=models.CASCADE
    )
    delivery_service_id = models.ForeignKey(
        to="oldtimers.DeliveryService",
        related_name="invoice_items",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    invoices = models.ForeignKey(
        to="oldtimers.Invoices",
        related_name="invoice_items",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    invoice_line_id = models.IntegerField(
        primary_key=True,
        blank=False,
        db_index=True,
        default="N/A"
    )
    price = models.ForeignKey(
        to="oldtimers.Vehicle",
        related_name="invoice_items_price",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    delivery_charge = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )
    insurance_charge = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )



