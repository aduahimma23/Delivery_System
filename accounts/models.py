from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class CustomeUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password=None, **extra_fields)
    

class CustomUser(AbstractUser):
    ADMIN = 1
    FOOD_VENDOR = 2
    CUSTOMER = 3
    DELIVERY_STAFF = 4
    INTERN_STAFF = 5

    USER_TYPE_CHOICES = [
        (ADMIN, "Admin"),
        (DELIVERY_STAFF, "Food Deliverer"),
        (CUSTOMER, "Customer"),
        (FOOD_VENDOR, "Food Vendor"),
        (INTERN_STAFF, "Intern Staff"),
    ]

    user_type = models.IntegerField(default=CUSTOMER, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    terms_and_conditions = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomeUserManager()

    def clean(self):
        if not self.terms_and_conditions:
            raise ValidationError("You must agree to the terms and conditions to register.")

    def save(self, *args, **kwargs):
        self.clean()
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
    

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer_profile")
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

class DeliveryStaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='delivery_staff_profile')
    phone_number = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20)

class InternStaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='intern_staff_profile')
    department = models.CharField(max_length=50)

class FoodVendorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='delivery_manager_profile')
    shop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == CustomUser.DELIVERY_STAFF:
            DeliveryStaffProfile.objects.create(user=instance)
        elif instance.user_type == CustomUser.CUSTOMER:
            CustomerProfile.objects.create(user=instance)
        elif instance.user_type == CustomUser.DELIVERY_STAFF:
            DeliveryStaffProfile.objects.create(user=instance)
        elif instance.user_type == CustomUser.INTERN_STAFF:
            InternStaffProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == CustomUser.DELIVERY_STAFF and hasattr(instance, 'delivery_manager_profile'):
        instance.delivery_manager_profile.save()
    elif instance.user_type == CustomUser.CUSTOMER and hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
    elif instance.user_type == CustomUser.DELIVERY_STAFF and hasattr(instance, 'delivery_staff_profile'):
        instance.delivery_staff_profile.save()
    elif instance.user_type == CustomUser.INTERN_STAFF and hasattr(instance, 'intern_staff_profile'):
        instance.intern_staff_profile.save()