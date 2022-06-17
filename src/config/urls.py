"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from config.settings import base
from oldtimers.views import IndexView, ContactsView

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('oldtimers/', include('oldtimers.urls')),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
] + static(base.MEDIA_URL, document_root=base.MEDIA_ROOT) + static(base.STATIC_URL, document_root=base.STATIC_ROOT)
