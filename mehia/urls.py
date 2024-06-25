from django.contrib import admin
from django.urls import path, include
from main.views import home

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path('main/', include('main.urls')),
    path('accounts/', include('accounts.urls')),
]
