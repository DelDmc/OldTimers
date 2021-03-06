# Generated by Django 3.2.13 on 2022-07-07 13:20

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('email', models.EmailField(blank=True, max_length=128)),
                ('address', models.CharField(blank=True, max_length=128, verbose_name='address')),
                ('city', models.CharField(blank=True, max_length=64, verbose_name='city')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('zip_code', models.CharField(max_length=5, verbose_name='zip code')),
                ('international_delivery', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('invoice_date', models.DateTimeField()),
                ('billing_address', models.CharField(default='N/A', max_length=128, verbose_name='address')),
                ('billing_city', models.CharField(blank=True, max_length=64, verbose_name='city')),
                ('billing_country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('billing_zip_code', models.CharField(max_length=5, verbose_name='zip code')),
                ('total', models.DecimalField(decimal_places=2, max_digits=19)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('email', models.EmailField(max_length=128)),
                ('address', models.CharField(blank=True, max_length=128, verbose_name='address')),
                ('city', models.CharField(blank=True, max_length=64, verbose_name='city')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=5, verbose_name='zip code')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='description')),
                ('photo', models.ImageField(blank=True, default='users_photo/default.jpg', null=True, upload_to='users_photo/')),
                ('service_fee', models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=19, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='retailer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('create_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('vin', models.CharField(db_index=True, max_length=17, primary_key=True, serialize=False, unique=True)),
                ('category', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'European Elite Classic'), (1, 'US Retro'), (2, 'European Legend'), (3, 'Fully Restored Oldtimer'), (4, 'US Muscle Car'), (5, 'Offroad Classic'), (6, 'Asian Legends'), (7, 'Rare Supercar'), (8, 'Deep Tuned Custom'), (9, 'European Racing Classics'), (10, ' Other')], default=10)),
                ('brand', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('production_year', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2000), django.core.validators.MinValueValidator(1900)], verbose_name='year')),
                ('condition', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Excellent'), (1, 'Very Good'), (2, 'Good'), (3, 'Satisfactory'), (4, 'Poor'), (5, 'Out of order'), (6, 'Other')], default=6, null=True)),
                ('mileage', models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(3000000)])),
                ('seats', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(1)])),
                ('color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=None)),
                ('transmission', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Manual'), (1, 'Automatic'), (2, 'Other')], default=2, null=True)),
                ('image', models.ImageField(blank=True, default='default.png', null=True, upload_to='media/vehicle')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('description', models.TextField(blank=True, max_length=500)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to=settings.AUTH_USER_MODEL)),
                ('retailer', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='vehicle', to='oldtimers.retailer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('create_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('invoice_line_id', models.IntegerField(db_index=True, default='N/A', primary_key=True, serialize=False)),
                ('delivery_fee', models.DecimalField(decimal_places=2, max_digits=19)),
                ('insurance_fee', models.DecimalField(decimal_places=2, max_digits=19)),
                ('delivery_service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items', to='oldtimers.deliveryservice')),
                ('invoices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items', to='oldtimers.invoices')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items_price', to='oldtimers.vehicle')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items_vehicle', to='oldtimers.vehicle')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('create_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=128)),
                ('last_name', models.CharField(blank=True, max_length=128)),
                ('rank', models.PositiveSmallIntegerField(choices=[(0, 'Chief Executive Officer'), (1, 'General Manager / Administrator'), (2, 'Sales Manager')], default=2)),
                ('email', models.EmailField(blank=True, max_length=128)),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='oldtimers.retailer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
