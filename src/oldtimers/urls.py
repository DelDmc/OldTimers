from django.urls import path

from oldtimers.views import (CarListingByCategoryView, CarListingView,
                             RetailerListView)

app_name = "oldtimers"

urlpatterns = [
    path("car-listing", CarListingView.as_view(), name="get_cars"),
    path("car-listing/<category>/", CarListingByCategoryView.as_view(), name="get_cars_by_cat"),
    path("retailers", RetailerListView.as_view(), name="get_retailers"),
]
