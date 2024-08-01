from django.db import models
from django.conf import settings
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from main.models import UserProfile

class UserLoction(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longtitude = models.DecimalField(max_digits=9, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)

    def __Str__(self):
        return f"{self.user.username}"
    
class TwilioSettings(models.Model):
    account_sid = models.CharField(max_length=150, blank=False)
    auth_token = models.CharField(max_length=150, blank=False)
    phone_number = models.CharField(max_length=20, unique=True, null=False)

    def __str__(self):
        return f"Twilio Settings (Phone: {self.phone_number})"

class DeliveryItem(models.Model):
    PENDING = 'PENDING'
    CONFIRMED = "CONFIRMED"
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, "Confirmed"),
        (IN_TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    item_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    item_description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_date = models.DateField()
    special_instructions = models.TextField(blank=True, null=True)
    tracking_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)

    def generate_tracking_number(self):
        return str(uuid.uuid4().replace("-", "").upper()[:12])

    def get_history(self):
        return self.deliveryitemhistory_set.all().order_by("-timestamp")

    def __str__(self):
        return f"Delivery {self.item_id} Date: {self.delivery_date}"
    
class DeliveryItemHistory(models.Model):
    delivery_item = models.ForeignKey('DeliveryItem', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"History for {self.delivery_item.tracking_number} at {self.timestamp}"
    
@receiver(pre_save, sender=DeliveryItem)
def save_delivery_item_history(sender, instance, **kwargs):
    if instance.pk:
        previous = DeliveryItem.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            DeliveryItemHistory.objects.create(
                delivery_item = instance,
                status = previous.status,
                additional_info = f"Status changed from {previous.status} to {instance.status}"
            )

class SenderDetails(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_deliveries')
    delivery_item = models.ForeignKey(DeliveryItem, on_delete=models.CASCADE, related_name="senders")
    address = models.TextField()
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Username: "


class ReceiverDetails(models.Model):
    delivery_item = models.ForeignKey(DeliveryItem, on_delete=models.CASCADE, related_name="receivers")
    sender = models.ForeignKey(SenderDetails, on_delete=models.CASCADE, related_name="receivers")
    name = models.CharField(max_length=255)
    email_address = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery to {self.name} Delivered at {self.received_at}"


class TrackDeliveryItem(models.Model):
    delivery_item = models.ForeignKey(DeliveryItem, on_delete=models.CASCADE, related_name="trackings")
    current_status = models.CharField(max_length=155, choices=DeliveryItem.STATUS_CHOICES, default=DeliveryItem.PENDING)
    location_updates = models.JSONField(default=list)
    timespand = models.DateTimeField(auto_now_add=True)

    def add_state(self, status, location):
        self.location_updates.append({
            "status": status,
            "location": location,
            "timespand": self.timespand
            })
        self.current_status = status
        self.save()
    

class CancelDeliveryItem(models.Model):
    delivery_item = models.ForeignKey(DeliveryItem, on_delete=models.CASCADE, related_name="cancel_deliveries")
    cancellation_date = models.DateTimeField(default=timezone.now)
    reason = models.TextField(max_length=500)

    def save(self, *args, **kwargs):
        if self.delivery_item.status not in [DeliveryItem.PENDING, DeliveryItem.CONFIRMED]:
            raise ValueError("Only orders that are pending or confirmed can be canceled.")
        self.delivery_item = DeliveryItem.CANCELLED
        self.delivery_item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cancellation for order {self.delivery_item.item_id}"
    

class DeliveryItemReview(models.Model):
    item = models.OneToOneField(DeliveryItem, on_delete=models.CASCADE, related_name="delivery_reviews")
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="delivery_reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Delivery Item Review")
        verbose_name_plural = _("Delivery Item Reviews")

    def __str__(self):
        return f"Review for order {self.item.item_id} by {self.user_profile.user.username}"
