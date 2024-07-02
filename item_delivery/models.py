from django.db import models
from django.conf import settings
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from main.models import UserProfile


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
    item_weight = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_date = models.DateField()
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery {self.item_id}"


class SenderDetails(models.Model):
    delivery_item = models.ForeignKey(DeliveryItem, on_delete=models.CASCADE, related_name="senders")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_deliveries')
    sender_name = models.CharField(max_length=255)
    sender_address = models.TextField()
    sender_city = models.CharField(max_length=100)
    sender_state = models.CharField(max_length=100)
    sender_postal_code = models.CharField(max_length=20)
    sender_phone_number = models.CharField(max_length=20)


class ReceiverDetails(models.Model):
    sender = models.ForeignKey(SenderDetails, on_delete=models.CASCADE, related_name="receivers")
    recipient_name = models.CharField(max_length=255)
    recipient_address = models.TextField()
    recipient_city = models.CharField(max_length=100)
    recipient_state = models.CharField(max_length=100)
    recipient_postal_code = models.CharField(max_length=20)
    recipient_phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Delivery to {self.recipient_name}"


class TrackDeliveryItem(models.Model):
    delivert_item = models.ForeignKey(DeliveryItem, on_delete=models.CASCADE, related_name="trackings")
    status = models.CharField(max_length=155, choices=DeliveryItem.STATUS_CHOICES, default=DeliveryItem.PENDING)
    timespand = models.DateTimeField(auto_now_add=True)


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

    def __str__(self) -> str:
        return f"Review for order {self.item.item_id} by {self.user_profile.user.username}"
