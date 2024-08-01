from django.contrib import admin
from django.urls import path, include
from main.views import start_view

urlpatterns = [
    path("", start_view),
    path("admin/", admin.site.urls),
    path('main/', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path("item_delivery/", include("item_delivery.urls")),
]
