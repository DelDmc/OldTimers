from random import randint, random, shuffle

from django.db.models import Q
from django.http import Http404, HttpResponse
# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.base import TemplateResponseMixin
from webargs import fields
from webargs.djangoparser import use_args, use_kwargs

from oldtimers.models import Retailer, Vehicle


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = "vehicles"
    extra_context_counter = "counter"
    queryset = Vehicle.objects.all()

    def get_context_data(self, **kwargs):
        queryset = list(self.queryset)
        shuffle(queryset)
        print(queryset)
        extra_context = [queryset[i] for i in range(6)]
        extra_context_counter = len(queryset)
        kwargs["vehicles"] = extra_context
        kwargs["counter"] = extra_context_counter
        print(kwargs)
        return kwargs


class CarListingByCategoryView(ListView):
    template_name = "cars_listing_by_category.html"
    context_object_name = "vehicles"
    paginate_by = 3

    def get_queryset(self):
        self.category = self.kwargs["category"]
        if int(self.category) == 99:
            return Vehicle.objects.all()
        else:
            return Vehicle.objects.filter(category=self.category)


class RetailerListView(ListView, TemplateResponseMixin):
    template_name = "retailers_listing.html"
    model = Retailer
    context_object_name = "retailers"
    queryset = Retailer.objects.all()
    additional_context = "retailers_vehicles"

    def get_context_data(self, **kwargs):
        context = {}
        for retailer in self.queryset:
            vehicles = Vehicle.objects.filter(retailer__company_name__contains=retailer.company_name)
            context[retailer] = [vehicle for vehicle in vehicles]

        kwargs["retailers_vehicles"] = context
        print("kwargs", kwargs)
        return kwargs

    # specific_retailer_vehicle_template = "retailer_vehicle.html"
    # context_object_name = "retailers"
    # extra_context = "vehicles"
    # queryset = Retailer.objects.all()
    # only_retailers_vehicles = Vehicle.objects.filter(retailer_id=True)
    #
    # vehicle_args = {
    #     "retailer": fields.Str(required=False),
    #     "brand": fields.Str(required=False),
    #     "production_year": fields.Int(required=False),
    #     "price": fields.Int(required=False)
    # }
    #
    # # def get_template_names(self):
    # #     return [self.template_name, self.specific_retailer_vehicle_template]
    #
    # @use_args(vehicle_args, location="query")
    # def get(self, request, parameters, *args, **kwargs):
    #     super(RetailerListView, self).get(request, *args, **kwargs)
    #     specific_retailer_vehicles = self.get_vehicles(request, parameters)
    #     context = self.get_context_data(specific_retailer_vehicles=specific_retailer_vehicles)
    #     return self.render_to_response(context)
    #
    # def get_context_data(self,  **kwargs):
    #     kwargs["vehicles"] = self.only_retailers_vehicles
    #     kwargs["retailers"] = self.queryset
    #     print("kwargs", kwargs)
    #     return kwargs
    #
    # def get_vehicles(self, request, parameters):
    #     retailer_vehicles = self.only_retailers_vehicles
    #     for param_name, param_value in parameters.items():
    #         if param_value:
    #             retailer_vehicles = retailer_vehicles.filter(**{param_name: param_value})
    #     print("vehicles", retailer_vehicles)
    #     return retailer_vehicles


class ContactsView(TemplateView):
    template_name = "contacts.html"
