from django.contrib import admin
from .models import *

@admin.register(TwilioSettings)
class TwilioSettingsAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "account_sid")
    