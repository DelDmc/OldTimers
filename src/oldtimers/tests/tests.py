import random
import string
from decimal import getcontext

from django.core.exceptions import ValidationError
from django.test import TestCase

from oldtimers.models import Offer, Retailer, Vehicle


def sample_retailer(id, company_name, **params):
    defaults = {
        "email": "email@test.com",
        "zip_code": "35068",
        "mobile": "+35965524123",
        "country": "GB",
        "city": "LONDON",
    }
    defaults.update(params)
    test_retailer = Retailer.objects.create(id=2, company_name=company_name, **defaults)
    return test_retailer


def sample_vehicle(retailer_id, **params):
    defaults = {
        "vin": f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=17))}",
        "category": "2",
        "brand": "Porsche",
        "model": "911",
        "production_year": "1988",
        "condition": "3",
        "price": "20000.00",
        "description": "good",
    }

    defaults.update(params)
    test_vehicle = Vehicle.objects.create(retailer_id=retailer_id, **defaults)
    return test_vehicle


def sample_offer(retailer_id, vehicle_id):
    test_offer = Offer.objects.create(retailer_id=retailer_id, vehicle_id=vehicle_id)
    return test_offer


class TestRetailerModel(TestCase):
    def setUp(self) -> None:
        defaults = {
            "id": 1,
            "email": "default@deafult.com",
            "zip_code": "00000",
            "mobile": "+35623152258",
            "country": "GB",
            "service_fee": "1.30",
        }
        self.default_retailer = Retailer.objects.create(company_name="test_company", **defaults)
        self.vehicles_count = 10
        self.test_retailer = sample_retailer(id=2, company_name="BravoMotors")
        for i in range(self.vehicles_count):
            sample_vehicle(retailer_id=self.test_retailer.id)

    def tearDown(self) -> None:
        self.test_retailer.delete()

    def test_vehicles_count_normal_case(self):
        self.assertEqual(self.vehicles_count, self.test_retailer.vehicles_count())

    # def test_negative_service_fee(self):
    #     self.test_retailer.service_fee = -1.0
    #     with self.assertRaises(ValidationError):
    #         Retailer.objects.create(id=5, company_name="test", service_fee=-1.0)


class TestVehicleModel(TestRetailerModel):
    def test_year_of_manufacture_limit(self):
        with self.assertRaises(ValidationError):
            sample_vehicle(retailer_id=2, production_year=1899)

    def test_vehicle_negative_price(self):
        with self.assertRaises(ValidationError):
            sample_vehicle(retailer_id=2, production_year=1995, price="-12000.00")

    def test_vehicle_zero_price(self):
        with self.assertRaises(ValidationError):
            sample_vehicle(retailer_id=2, production_year=1995, price="0.00")


class TestOfferModel(TestCase):
    def setUp(self) -> None:
        defaults = {
            "email": "default@deafult.com",
            "zip_code": "00000",
            "mobile": "+33600000000",
            "service_fee": "1.3",
        }
        vin = "JT100000000000000"
        self.default_retailer = Retailer.objects.create(id=1, **defaults)
        self.test_retailer = Retailer.objects.create(
            company_name="BravoMotors", id=2, email="test@test.com", service_fee="1.30"
        )
        self.default_vehicle = sample_vehicle(retailer_id=2, vin=vin)
        self.test_offer = sample_offer(
            retailer_id=self.test_retailer.id,
            vehicle_id=vin,
        )

    def tearDown(self) -> None:
        self.default_retailer.delete()

    def test_offer_price(self):
        c = getcontext()

        c.prec = 3
        print(c)
        print(self.test_offer.vehicle.price, self.test_retailer)
        self.assertEqual(str(self.test_offer.offer_price()), "26000.00")
