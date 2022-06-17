from django.urls import path

from oldtimers.views import CarListingView, RetailerListView

app_name = "oldtimers"

urlpatterns = [
    path("car-listing", CarListingView.as_view(), name="get_cars"),
    path("retailers", RetailerListView.as_view(), name="get_retailers"),
]
