from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from twilio.rest import Client
from .models import TwilioSettings

def get_twilio_settings():
    try:
        return TwilioSettings.objects.first()
    except ObjectDoesNotExist:
        return None

def send_sms(to, message):
    twilio_settings = get_twilio_settings()
    if not twilio_settings:
        raise ValueError("Twilio settings are not configured.")

    client = Client(twilio_settings.account_sid, twilio_settings.auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_settings.phone_number,
        to=to
    )
    return message
