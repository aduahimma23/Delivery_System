from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class Restaurant(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("CASH", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
        ("BOTH", "Both")
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="food_vendor_profile")
    restaurant_name = models.CharField(max_length=150, unique=True, blank=False)
    logo = models.ImageField(upload_to='vendor/logos/', blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="Both")
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name

class Category(models.Model):
    LOCAL_FOOD = "Local Dishes"
    CONTINENTAL_FOOD = "Continental Dishes"
    OTHERS = "Others"

    FOOD_CATEGORY_CHOICE = (
        ("LOCAL FOOD", "Local Dishes"),
        ("CONTINENTAL FOOD", "Continental Dishes"),
        ("OTHERS", "Others")
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="categories")
    cateory_name = models.CharField(max_length=255, blank=False, choices=FOOD_CATEGORY_CHOICE, default=LOCAL_FOOD)


class MenuCategory(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu")
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    vendor = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True, related_name='menu_items')
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField(blank=True, unique=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='vendor/menu/items/', blank=True, null=True)

    def __str__(self):
        return self.name


class MenuItemPrice(models.Model):
    NORMAL = "Normal"
    REGULAR = "Regular"
    MEDIUM = "Medium"
    LARGE = "Large"
    EXTRA_LARGE = "Extra Large"

    SIZE_CHOICES = [
        ("NORMAL", "Normal"),
        ('REGULAR', 'Regular'), 
        ('MEDIUM', 'Medium'),
        ('LARGE', 'Large'),
        ('EXTRA_LARGE', 'Extra Large'),
    ]
    
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="prices")
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default=NORMAL)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('menu_item', 'size')

    def __str__(self):
        return f"{self.size} - {self.menu_item.name}"


class Extraitem(models.Model):
    menu_item = models.ManyToManyField(MenuItem, blank=True, related_name="extra_items")
    name = models.CharField(max_length=155, blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=3)
    image = models.ImageField(upload_to="vendor/menu/extra_items", unique=True, blank=False)

    def __str__(self):
        return self.name


class MenuItemPriceDiscount(models.Model):
    menu_item_price = models.ForeignKey(MenuItemPrice, on_delete=models.CASCADE, related_name="discounts")
    discount_percent = models.DecimalField(decimal_places=2, max_digits=5)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end end date.")
        if self.discount_percent <= 0 or self.discount_percent > 100:
            raise ValidationError("Discount percent must be between 1 and 100. ")
    
    def __str__(self):
        return f"{self.discount_percent}% off {self.menu_item_price.menu_item.name} ({self.menu_item_price.size})"
    
    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date
    
class Promotion(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="promotions")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="promotions")
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(decimal_places=2, max_digits=6)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date")
        if self.discount_percent <= 0 or self.discount_percent > 100:
            raise ValidationError("Discount percent must be between 1 and 100")
        
    def __str__(self):
        return f"{self.discount_percent}% off on {self.menu_item.name}"
    
    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date