from random import randint, random, shuffle

from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.views.generic import ListView, TemplateView

from oldtimers.models import Retailer, Vehicle


class IndexView(TemplateView):
    template_name = "index.html"
    http_method_names = ["get"]
    extra_context = "vehicles"
    extra_context_counter = "counter"

    def get_context_data(self, **kwargs):
        queryset = list(Vehicle.objects.all())
        shuffle(queryset)
        print(queryset)
        self.extra_context = []
        self.extra_context_counter = len(queryset)
        for i in range(6):
            self.extra_context.append(queryset[i])
        kwargs["vehicles"] = self.extra_context
        kwargs["counter"] = self.extra_context_counter
        print(kwargs)
        return kwargs


class CarListingByCategoryView(ListView):
    template_name = "cars_listing_by_category.html"
    context_object_name = "vehicles"
    paginate_by = 2

    def get_queryset(self):
        self.category = self.kwargs["category"]
        if int(self.category) == 99:
            return Vehicle.objects.all()
        else:
            return Vehicle.objects.filter(category=self.category)


class RetailerListView(ListView):
    template_name = "retailers_listing.html"
    model = Retailer


class ContactsView(TemplateView):
    template_name = "contacts.html"
