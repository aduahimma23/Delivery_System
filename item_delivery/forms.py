from django import forms
from .models import (DeliveryItem, SenderDetails, ReceiverDetails, CancelDeliveryItem, DeliveryItemReview)


class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['item_description', 'item_weight', 'delivery_date', 'special_instructions']


class SenderAddressForm(forms.ModelForm):
    class Meta:
        model = SenderDetails
        fields = ['sender_name', 'sender_address', 'sender_city', 'sender_state', 'sender_postal_code', 'sender_phone_number']

class ReceiverAddressForm(forms.ModelForm):
    class Meta:
        model = ReceiverDetails
        fields = ['recipient_name', 'recipient_address', 'recipient_city', 'recipient_state', 'recipient_postal_code', 'recipient_phone_number']

class CancelDeliveryItemForm(forms.ModelForm):
    class Meta:
        model = CancelDeliveryItem
        fields = ['reason']

class DeliveyItemReviewForm(forms.ModelForm):
    class Meta:
        model = DeliveryItemReview
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.item:
            raise forms.ValidationError("Delivery an item(s) is required.")
        if not self.item.status:
            raise forms.ValidationError("You can only review delivered items.")
        return cleaned_data