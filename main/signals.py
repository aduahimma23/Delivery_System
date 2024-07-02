from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from .models import UserProfile, DeliveryAddress

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        DeliveryAddress.objects.create(
            user_profile=user_profile,
            address_line_1="Default Address Line 1",
            city="Default City",
            state="Default State",
            postal_code="000000",
            country="Default Country",
            is_default=True
        )
    else:
        instance.profile.save()   