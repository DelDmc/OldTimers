from decimal import Decimal
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
    paginate_by = 6

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
    search_form_context = "sorted_retailer"

    vehicle_args = {
        "retailer": fields.Str(required=False),
        "brand": fields.Str(required=False),
        "production_year": fields.Int(required=False,),
        "price__range": fields.Str(required=False)
    }

    def get_context_data(self, **kwargs):
        context = {}
        for retailer in self.queryset:
            vehicles = Vehicle.objects.filter(retailer__company_name__contains=retailer.company_name)
            context[retailer] = [vehicle for vehicle in vehicles]

        kwargs["retailers_vehicles"] = context
        print("kwargs", kwargs)
        return kwargs

    @use_args(vehicle_args, location="query")
    def get(self, request, parameters, *args, **kwargs):
        print("parameters", parameters)

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        vehicles = [vehicle for vehicle in self.get_vehicles(request, parameters)]
        context["sorted_retailer"] = vehicles
        print("context", context)
        return self.render_to_response(context)

    def get_vehicles(self, request, parameters):
        price_range = parameters.get('price__range').split(";")
        parameters['price__range'] = tuple(float(item) for item in price_range)
        retailer_sorted_vehicles = [
            Vehicle.objects.filter(**{param_name: param_value}) for param_name, param_value in parameters.items()
        ]
        print("retailer_sorted_vehicles", retailer_sorted_vehicles)
        print("parameters", parameters)
        return retailer_sorted_vehicles


class ContactsView(TemplateView):
    template_name = "contacts.html"
