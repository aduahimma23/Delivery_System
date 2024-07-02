import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from food_vendor.models import Restaurant, MenuItem


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="main_user_profile")
    first_name = models.CharField(max_length=100, unique=False, blank=False)
    last_name = models.CharField(max_length=100, unique=False, blank=False)
    phone_number = models.CharField(max_length=20, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to="customer/profile_picture", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"{self.user.username}'s profile"
    

class DeliveryAddress(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="delivery_addresses")
    address_line_1 = models.CharField(blank=False, unique=True, max_length=155)
    address_line_2 = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=100, blank=False, unique=False)
    city = models.CharField(max_length=100, blank=False, unique=False)
    post_code = models.CharField(max_length=50, blank=False, unique=True)
    is_default = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Address")
        verbose_name_plural = _("Delivery Addresses")

    def __str__(self):
        return f"{self.user_profile.first_name} {self.user_profile.last_name}, {self.address_line_1}, {self.post_code}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            DeliveryAddress.objects.filter(user_profile=self.user_profile, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Order(models.Model):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    DELIVERING = "DELIVERING"
    OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY'
    DELIVERED = 'DELIVERED'
    CANCELED = 'CANCELED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (DELIVERING, "Delivering"),
        (OUT_FOR_DELIVERY, 'Out for delivery'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order ID: {self.order_id} By: {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="order_items")
    payment_method = models.CharField(max_length=20, choices=[("CASH", "Cash on Delivery"), ("ONLINE", "Online")])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in cart {self.order.order_id}"
    
    def total_price(self):
        return self.quantity * self.menu_item.price

class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tracking")
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, default=Order.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tracking for Order {self.order.order_id}"

class CancelOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cancel_orders")
    cancellation_date = models.DateTimeField(default=timezone.now)
    reason = models.TextField()

    def save(self, *args, **kwargs):
        if self.order.status not in [Order.PENDING, Order.CONFIRMED]:
            raise ValueError("Only orders that are pending or confirmed can be canceled.")
        self.order.status = Order.CANCELED
        self.order.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cancellation for order {self.order.order_id}"
    
class OrderRewiew(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="reviews")
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self) -> str:
        return f"Review for order {self.order.order_id} by {self.user_profile.user.username}"
    