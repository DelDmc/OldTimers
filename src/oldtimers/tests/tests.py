import random
import string

from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Customer as User
from oldtimers.models import DeliveryService, Retailer, Vehicle


def sample_retailer(id, user_id, company_name, **params):
    defaults = {
        "email": "email@test.com",
        "zip_code": "35068",
        "phone_number": "+35965524123",
        "country": "GB",
        "city": "LONDON",
    }
    defaults.update(params)
    test_retailer = Retailer.objects.create(id=id, company_name=company_name, user_id=user_id, **defaults)
    return test_retailer


def sample_vehicle(retailer_id, **params):
    defaults = {
        "vin": f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=17))}",
        "price": "20000.00",
    }
    defaults.update(params)
    test_vehicle = Vehicle.objects.create(retailer_id=retailer_id, **defaults)
    return test_vehicle


def sample_delivery_service(company_name):
    defaults = {"zip_code": "00001"}
    return DeliveryService.objects.create(company_name=company_name, **defaults)


class TestRetailerModel(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(id=1, email="test@test.com", username="test1", password="12345")
        self.user = User.objects.create_user(id=2, email="test2@test.com", username="test2", password="12345")

        defaults = {
            "user_id": 1,
            "id": 1,
            "email": "default@deafult.com",
            "service_fee": "1.30",
        }
        self.default_retailer = Retailer.objects.create(company_name="test_company", **defaults)
        self.vehicles_count = 10
        self.test_retailer = sample_retailer(id=2, user_id=2, company_name="BravoMotors")
        for i in range(self.vehicles_count):
            sample_vehicle(retailer_id=self.test_retailer.id)

    def tearDown(self) -> None:
        self.test_retailer.delete()

    def test_vehicles_count_normal_case(self):
        self.assertEqual(self.vehicles_count, self.test_retailer.vehicles_count())

    def test_negative_service_fee(self):
        self.test_retailer.service_fee = -1.0
        with self.assertRaises(ValidationError):
            Retailer.objects.create(id=5, user_id=1, company_name="test", service_fee=-1.0)


class TestVehicleModel(TestCase):
    def setUp(self) -> None:

        self.user = User.objects.create_user(id=2, email="test@test.com", password="123456")

        self.test_retailer = sample_retailer(id=2, user_id=2, company_name="BravoMotors")

    def tearDown(self) -> None:
        self.test_retailer.delete()

    def test_year_of_manufacture_limit(self):
        with self.assertRaises(ValidationError):
            sample_vehicle(retailer_id=2, production_year=1899)

    def test_vehicle_negative_price(self):
        with self.assertRaises(ValidationError):
            sample_vehicle(retailer_id=2, production_year=1995, price="-12000.00")

    def test_vehicle_zero_price(self):
        with self.assertRaises(ValidationError):
            sample_vehicle(retailer_id=2, production_year=1995, price="0.00")


class TestDeliveryServiceModel(TestCase):
    def setUp(self) -> None:
        self.test_delivery_service = sample_delivery_service("TestDelivery")

    def tearDown(self) -> None:
        self.test_delivery_service.delete()

    def test_if_international_delivery(self):
        self.assertFalse(self.test_delivery_service.international_delivery)
