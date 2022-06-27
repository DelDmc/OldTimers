from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (CreateVehicleAPIView, CustomerViewSet,
                       DeleteVehicleAPIView, RetrieveCustomerVehiclesAPIView,
                       RetrieveVehicleAPIView, UpdateVehicleAPIView,
                       VehicleViewSet)

app_name = "api"

router = DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"vehicles", VehicleViewSet)

schema_view = get_schema_view(openapi.Info(title="API", default_version="v1", description="Test description"))


urlpatterns = [
    path("", include(router.urls)),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    # path("auth/", include("djoser.urls")),
    # path("auth/", include("djoser.urls.jwt")),
    # path("auth/", include("djoser.urls.authtoken")),
    path("create-vehicle/", CreateVehicleAPIView.as_view(), name="create_vehicle"),
    path("retrieve-vehicle/<str:vin>/", RetrieveVehicleAPIView.as_view(), name="retrieve_vehicle"),
    path("delete-vehicle/<str:vin>/", DeleteVehicleAPIView.as_view(), name="delete_vehicle"),
    path("update-vehicle/<str:vin>/", UpdateVehicleAPIView.as_view(), name="update_vehicle"),
    path(
        "retrieve-vehicles/my/",
        RetrieveCustomerVehiclesAPIView.as_view({"get": "list"}),
    ),
]
