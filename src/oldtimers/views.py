from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.views.generic import ListView, TemplateView

from oldtimers.models import Retailer, Vehicle


class IndexView(TemplateView):
    template_name = "index.html"
    http_method_names = ["get"]


class CarListingView(ListView):
    template_name = "cars_listing.html"
    model = Vehicle
    # queryset = Vehicle.objects.all()
    context_object_name = "vehicles"
    # context_asian_legends = "asian_legend"
    # context_offroad = "offroad"


class CarListingByCategoryView(ListView):
    template_name = "cars_listing_by_category.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        self.category = self.kwargs["category"]
        return Vehicle.objects.filter(category=self.category)


class RetailerListView(ListView):
    template_name = "retailers_listing.html"
    model = Retailer


class ContactsView(TemplateView):
    template_name = "contacts.html"
