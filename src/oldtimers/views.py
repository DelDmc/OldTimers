from decimal import Decimal
from random import shuffle

from django.views.generic import ListView, TemplateView
from django.views.generic.base import TemplateResponseMixin
from webargs import fields
from webargs.djangoparser import use_args

from oldtimers.models import Retailer, Vehicle

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = "vehicles"
    extra_context_counter = "counter"
    queryset = Vehicle.objects.all()
    random_vehicles_qty = 6

    def get_context_data(self, **kwargs):
        queryset = list(self.queryset)
        shuffle(queryset)
        if queryset:
            extra_context = [queryset[i] for i in range(self.random_vehicles_qty)]
            extra_context_counter = len(queryset)
            kwargs["vehicles"] = extra_context
            kwargs["counter"] = extra_context_counter
            return kwargs
        else:
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
    search_form_context = "sorted_vehicles"
    max_vehicle_price = Decimal(50 * 10**6)
    min_vehicle_price = 0

    vehicle_args = {
        "retailer": fields.Str(required=False),
        "brand": fields.Str(required=False),
        "production_year": fields.Int(
            required=False,
        ),
        "price_from": fields.Str(required=False),
        "price_to": fields.Str(required=False),
    }

    def get_context_data(self, **kwargs):
        context = {}
        for retailer in self.queryset:
            vehicles = Vehicle.objects.filter(retailer__company_name__contains=retailer.company_name)
            context[retailer] = [vehicle for vehicle in vehicles]
        kwargs["retailers_vehicles"] = context
        return kwargs

    @use_args(vehicle_args, location="query")
    def get(self, request, parameters, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        vehicles = self.get_vehicles(parameters)
        context["sorted_vehicles"] = vehicles
        return self.render_to_response(context)

    def get_price_range(self, parameters):
        price_from = parameters.get("price_from")
        price_to = parameters.get("price_to")

        if price_from:
            price_from = Decimal(int(price_from))
            if price_to:
                price_to = Decimal(int(price_to))
            else:
                price_to = self.max_vehicle_price
        else:
            if price_to:
                price_from = self.min_vehicle_price
                price_to = Decimal(int(price_to))
            else:
                price_from = None
                price_to = None

        if price_from and price_to:
            price_range = (price_from, price_to)
            return price_range
        else:
            return None

    def get_vehicles(self, parameters):
        """Returns list of sorted vehicles as per data received from parameters"""
        if parameters:
            price_range = self.get_price_range(parameters)
            parameters.pop("price_from")
            parameters.pop("price_to")

            if price_range:
                parameters["price__range"] = price_range

        for param_name, param_value in parameters.items():
            search_form_context = Vehicle.objects.filter(**{param_name: param_value})
            return search_form_context


class ContactsView(TemplateView):
    template_name = "contacts.html"
