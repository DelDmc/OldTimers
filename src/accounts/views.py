from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
# Create your views here.
from django.urls import reverse, reverse_lazy


class UserLoginView(LoginView):
    template_name = "registration/login.html"

    def get_form(self, form_class=None):
        print(self.get_form_kwargs())
        return super().get_form(form_class=None)

    def get_default_redirect_url(self):
        return reverse("index")


class UserLogOutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
