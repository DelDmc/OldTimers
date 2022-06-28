from rest_framework.serializers import ModelSerializer

from accounts.models import Customer
from oldtimers.models import Vehicle


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "birthdate", "username", "phone_number"]


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "vin",
            "brand",
            "model",
            "price",
            "mileage",
            "image",
            "owner",
            "retailer",
            "production_year",
            "description",
            "category",
        ]
