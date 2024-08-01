from django.urls import path
from .views import *

app_name = "item"

urlpatterns = [
    path("home/", home_view, name="home"),
    path("send/", sender_details_view, name="send"),
    path("item_delivery/", item_delivery_view, name="details"),
    path("receiver_details/", receiver_details_view, name="receiver_details"),
    path("'item_delivery/track/<str:tracking_number>/", tracking_view, name="track"),
]