import uuid as uuid

from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Customer


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_datetime = models.DateTimeField(null=True, auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now=True)


class Retailer(BaseModel):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="retailer", null=False)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)
    company_name = models.CharField(max_length=50, blank=True, null=False)
    phone_number = PhoneNumberField(blank=True, null=False)
    email = models.EmailField(max_length=128)
    address = models.CharField(_("address"), max_length=128, null=False, blank=True)
    city = models.CharField(_("city"), max_length=64, blank=True, null=False)
    country = CountryField(blank=True, null=False)
    zip_code = models.CharField(_("zip code"), max_length=5, blank=True, null=False)
    description = models.TextField(
        _("description"),
        max_length=500,
        null=False,
        blank=True,
    )
    photo = models.ImageField(upload_to="users_photo/", null=True, blank=True)
    service_fee = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=True,
        default=1.00,
        validators=[MinValueValidator(1.00)],
    )

    def __str__(self):
        return f"{self.company_name} - {self.city} ({self.get_country_display()})"

    def vehicles_count(self):
        return self.vehicle.count()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Vehicle(BaseModel):
    YEAR_OF_PRODUCTION_MIN = 1900
    YEAR_OF_PRODUCTION_MAX = 2000

    class VEHICLE_CATEGORY_CHOICES(models.IntegerChoices):
        EU_ELITE = 0, "European Elite Classic"
        US_RETRO = 1, "US Retro"
        EU_LEGEND = 2, "European Legend"
        RESTORED_OLDTIMER = 3, "Fully Restored Oldtimer"
        US_MUSCLE = 4, "US Muscle Car"
        OFFROAD = 5, "Offroad Classic"
        ASIAN_LEGEND = 6, "Asian Legends"
        RARE_SUPERCAR = 7, "Rare Supercar"
        CUSTOM = 8, "Deep Tuned Custom"
        EU_RACING = 9, "European Racing Classics"
        OTHER = 10, " Other"

    class VEHICLE_CONDITION_CHOICES(models.IntegerChoices):
        EXCELLENT = 0, "Excellent"
        VERY_GOOD = 1, "Very Good"
        GOOD = 2, "Good"
        SATISFACTORY = 3, "Satisfactory"
        POOR = 4, "Poor"
        OUT_OF_ORDER = 5, "Out of order"
        OTHER = 6, "Other"

    class VEHICLE_TRANSMISSION_CHOICES(models.IntegerChoices):
        M = 0, "Manual"
        A = 1, "Automatic"
        OTHER = 2, "Other"

    owner = models.ForeignKey(
        Customer,
        related_name="vehicle",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    retailer = models.ForeignKey(
        Retailer,
        related_name="vehicle",
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        default=1,
    )
    vin = models.CharField(null=False, blank=False, unique=True, max_length=17, primary_key=True, db_index=True)
    category = models.PositiveSmallIntegerField(
        choices=VEHICLE_CATEGORY_CHOICES.choices,
        default=VEHICLE_CATEGORY_CHOICES.OTHER,
        null=False,
        blank=True,
    )
    brand = models.CharField(
        max_length=50,
        null=False,
        blank=True,
    )
    model = models.CharField(
        max_length=50,
        null=False,
        blank=True,
    )
    production_year = models.PositiveSmallIntegerField(
        _("year"),
        null=True,
        blank=True,
        validators=[MaxValueValidator(YEAR_OF_PRODUCTION_MAX), MinValueValidator(YEAR_OF_PRODUCTION_MIN)],
    )
    condition = models.PositiveSmallIntegerField(
        choices=VEHICLE_CONDITION_CHOICES.choices,
        default=VEHICLE_CONDITION_CHOICES.OTHER,
        null=True,
        blank=True,
    )
    mileage = models.PositiveBigIntegerField(null=True, blank=True, validators=[MaxValueValidator(3000000)])
    seats = models.SmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(7), MinValueValidator(1)])
    color = ColorField(blank=True, null=True)
    transmission = models.PositiveSmallIntegerField(
        choices=VEHICLE_TRANSMISSION_CHOICES.choices,
        default=VEHICLE_TRANSMISSION_CHOICES.OTHER,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        default="default.png",
        upload_to="media/vehicle",
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(1.00)]
    )
    description = models.TextField(
        max_length=500,
        null=False,
        blank=True,
    )

    def __str__(self):
        return f"{self.brand} {self.model} Price: {self.price} $ "

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Employee(BaseModel):
    class EMPLOYEE_RANK_CHOICES(models.IntegerChoices):
        CEO = 0, "Chief Executive Officer"
        GENERAL_MANAGER = 1, "General Manager / Administrator"
        SALES_MANAGER = 2, "Sales Manager"

    user = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="employee")
    retailer = models.ForeignKey(to="Retailer", related_name="employees", on_delete=models.CASCADE)
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    first_name = models.CharField(
        max_length=128,
        null=False,
        blank=True,
    )
    last_name = models.CharField(
        max_length=128,
        null=False,
        blank=True,
    )
    rank = models.PositiveSmallIntegerField(
        choices=EMPLOYEE_RANK_CHOICES.choices, default=EMPLOYEE_RANK_CHOICES.SALES_MANAGER
    )
    email = models.EmailField(
        max_length=128,
        null=False,
        blank=True,
    )


class DeliveryService(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)
    company_name = models.CharField(max_length=50, null=False, blank=True)
    phone_number = PhoneNumberField(null=False, blank=True)
    email = models.EmailField(
        max_length=128,
        null=False,
        blank=True,
    )
    address = models.CharField(
        _("address"),
        max_length=128,
        null=False,
        blank=True,
    )
    city = models.CharField(
        _("city"),
        max_length=64,
        null=False,
        blank=True,
    )
    country = CountryField(
        null=False,
        blank=True,
    )
    zip_code = models.CharField(
        _("zip code"),
        max_length=5,
        null=False,
        blank=False,
    )
    international_delivery = models.BooleanField(default=False)


class Invoices(BaseModel):
    invoice_date = models.DateTimeField(
        null=False,
        blank=False,
    )
    billing_address = models.CharField(_("address"), max_length=128, default="N/A")
    billing_city = models.CharField(
        _("city"),
        max_length=64,
        blank=True,
        null=False,
    )
    billing_country = CountryField(
        null=False,
        blank=True,
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


class InvoiceItems(BaseModel):
    vehicle = models.ForeignKey(to="Vehicle", related_name="invoice_items_vehicle", on_delete=models.CASCADE)
    delivery_service_id = models.ForeignKey(
        to="DeliveryService",
        related_name="invoice_items",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    invoices = models.ForeignKey(
        to="Invoices",
        related_name="invoice_items",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    invoice_line_id = models.IntegerField(primary_key=True, blank=False, db_index=True, default="N/A")
    price = models.ForeignKey(
        to="Vehicle",
        related_name="invoice_items_price",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    delivery_fee = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )
    insurance_fee = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )
