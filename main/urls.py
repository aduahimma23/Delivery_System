from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path("start/", start_view, name="start"),
    path("home/", home, name="home"),
    path("contact/", contact_view, name="contact"),
    path('orders/', order_list, name='order_list'),
    path('order-items/', order_items_list, name='order_items_list'),
    path("menu_list", menu_list, name="menu"),
    path('add-to-cart/<int:menu_item_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:cart_item_id>/<str:action>/', update_cart_item, name='update_cart_item'),

]