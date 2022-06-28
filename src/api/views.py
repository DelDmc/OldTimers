from django.contrib.auth import get_user
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.models import Customer
from api.serializers import CustomerSerializer, VehicleSerializer
from oldtimers.models import Vehicle

# Create your views here.


class CustomerViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """

    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class VehicleViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class CreateVehicleView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VehicleSerializer


class RetrieveVehicleView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VehicleSerializer
    lookup_field = "vin"

    def get_queryset(self):
        vin = self.kwargs["vin"]
        return Vehicle.objects.filter(vin=vin)


class DeleteVehicleView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["delete"]
    lookup_field = "vin"

    def get_queryset(self):
        vin = self.kwargs["vin"]
        return Vehicle.objects.filter(vin=vin)


class UpdateVehicleView(UpdateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["patch", "put", "post"]
    lookup_field = "vin"

    def get_queryset(self):
        vin = self.kwargs["vin"]
        return Vehicle.objects.filter(vin=vin)


class RetrieveMyVehiclesView(ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        customer = self.request.user
        if customer.is_owner():
            queryset = Vehicle.objects.filter(owner_id=customer.id)
            if customer.is_retailer():
                second_queryset = Vehicle.objects.filter(retailer__user_id=customer.id)
                matches = queryset | second_queryset
                return matches
            else:
                return queryset
        else:
            queryset = Vehicle.objects.filter(owner_id=customer.id)
            return queryset
