from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView, TemplateView

from oldtimers.models import Retailer, Vehicle


class IndexView(TemplateView):
    template_name = "index.html"
    http_method_names = ["get"]


class CarListingView(ListView):
    template_name = "cars_listing.html"
    model = Vehicle


class RetailerListView(ListView):
    template_name = "retailers_listing.html"
    model = Retailer


class ContactsView(TemplateView):
    template_name = "contacts.html"
