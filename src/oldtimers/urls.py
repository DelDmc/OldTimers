from django.urls import path

from oldtimers.views import (CarListingByCategoryView, RetailerListView,
                             delete_fake_data, fake_customers, fake_retailers,
                             fake_vehicles)

app_name = "oldtimers"

urlpatterns = [
    path("car-listing/<category>/", CarListingByCategoryView.as_view(), name="get_cars_by_cat"),
    path("retailers", RetailerListView.as_view(), name="get_retailers"),
    path("fake-customers/", fake_customers, name="fake_customers"),
    path("fake-retailers/", fake_retailers, name="fake_retailers"),
    path("fake-vehicles/", fake_vehicles, name="fake_vehicles"),
    path("fake-delete/", delete_fake_data, name="fake_delete"),
]
