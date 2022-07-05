import string
from decimal import Decimal
from random import choice, choices, randint

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from faker import Faker

from accounts.models import Customer
from config.celery import app
from oldtimers.models import Retailer, Vehicle

fake = Faker()


@app.task
def generate_fake_customers():
    num_of_instances = randint(10, 15)
    fake_customers = [
        Customer(
            email=fake.email(),
            username="FAKE{0}{1}".format(fake.user_name(), randint(0000, 9999)),
            password="1234fake",
            first_name=fake.name(),
            last_name=fake.last_name(),
        )
        for _ in range(num_of_instances)
    ]
    Customer.objects.bulk_create(fake_customers)


def available_fake_customers():
    """
    Check customers that have empty retailer field
    """
    all_fake_customers = Customer.objects.filter(username__icontains="FAKE")
    fake_customers_have_retailer = all_fake_customers.filter(retailer__isnull=False)

    available_customers = len(all_fake_customers) - len(fake_customers_have_retailer)

    if available_customers > 0:
        return True
    else:
        return False


@app.task
def generate_fake_retailers():
    num_of_instances = randint(5, 10)
    if not available_fake_customers():
        generate_fake_customers()
    all_customers_ids = Customer.objects.filter(username__icontains="FAKE", retailer__isnull=True).values_list(
        "id", flat=True
    )

    for _ in range(num_of_instances):
        try:
            Retailer.objects.create(
                user_id=all_customers_ids[randint(0, len(all_customers_ids) - 1)],
                id=fake.ean(length=13),
                email=fake.email(),
                zip_code=randint(10000, 99999),
                phone_number="+38067{0}".format(randint(1_000_000, 9_999_999)),
                country=fake.locale()[-2:],
                city=fake.city(),
                company_name=fake.company(),
                address=fake.address(),
                description=fake.paragraph(nb_sentences=2),
            )
        except (IntegrityError, ValidationError):
            continue


@app.task
def generate_fake_vehicles():
    num_of_instances = randint(5, 20)
    brands = [
        "BMW",
        "Porsche",
        "OPEL",
        "SUZUKI",
        "TOYOTA",
        "HONDA",
    ]
    models = ["GT", "RUF", "AMG 55", "SL 500", "SR-T", "XLM600"]
    fake_vehicles = [
        Vehicle(
            retailer_id=None,
            owner_id=None,
            vin=f"{''.join(choices(string.ascii_uppercase + string.digits, k=17))}",
            category=randint(1, 10),
            brand="FAKE_{0}_".format(choice(brands)),
            model=choice(models),
            production_year=randint(1900, 2000),
            condition=randint(0, 6),
            mileage=randint(0, 120000),
            seats=randint(2, 5),
            transmission=randint(0, 2),
            price=Decimal(randint(100000, 10000000)),
            description=fake.paragraph(nb_sentences=2),
        )
        for _ in range(num_of_instances)
    ]
    Vehicle.objects.bulk_create(fake_vehicles)


@app.task
def delete_all_fake_data():
    Customer.objects.filter(username__icontains="FAKE").delete()
    Vehicle.objects.filter(brand__icontains="FAKE").delete()
