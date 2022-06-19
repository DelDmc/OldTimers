from django.urls import path

from accounts.views import UserLoginView, UserLogOutView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogOutView.as_view(), name="logout"),
]
