from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    PAYMENT_METHODS = (
        ("CASH", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
        ("BOTH", "Both")
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="food_vendor_profile")
    restaurant_name = models.CharField(max_length=150, unique=True, blank=False)
    logo = models.ImageField(upload_to='vendor/logos/', blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="Both")
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    vendor = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True, related_name='menu_items')
    name = models.CharField(max_length=255, blank=False, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    description = models.TextField(blank=True, unique=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='vendor/menu/items/', blank=True, null=True)

    def __str__(self):
        return self.name


class PriceOption(models.Model):
    menu_item = models.ManyToManyField(MenuItem, related_name="menu_prices")
    name = models.CharField(max_length=155, blank=True, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Extraitem(models.Model):
    menu_item = models.ManyToManyField(MenuItem, blank=True, related_name="extra_items")
    name = models.CharField(max_length=155, blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=3)
    image = models.ImageField(upload_to="vendor/menu/extra_items", unique=True, blank=False)

    def __str__(self):
        return self.name
    
    
class Promotion(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="promotions")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(decimal_places=2, max_digits=6)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.restaurant.restaurant_name}"
    

