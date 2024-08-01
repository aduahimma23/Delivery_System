from django import forms
from .models import (DeliveryItem, SenderDetails, ReceiverDetails, CancelDeliveryItem, 
                     TrackDeliveryItem, DeliveryItemReview)


class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['item_description', "weight", 'special_instructions']
        
        widgets = {
            "item_description": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item Description"}),
            "weight": forms.TextInput(attrs={"class": "form-control", "placeholder": "150kg"}),
            "special_instructions": forms.TextInput(attrs={"class": "form-control", "placeholder": "Special Isntruction"})
        }

class SenderDetailsForm(forms.ModelForm):
    class Meta:
        model = SenderDetails
        fields = ['address', 'city', 'region', 'postal_code']

        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sender Address"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Accra"}),
            "region": forms.TextInput(attrs={"class": "form-control", "placeholder": "Greater Accra"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "CK-0001-8859"})
        }

class ReceiverDetailsForm(forms.ModelForm):
    class Meta:
        model = ReceiverDetails
        fields = ['name', 'address', 'city', 'landmark', 'postal_code', 'phone_number']

        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sender Address"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Accra"}),
            "region": forms.TextInput(attrs={"class": "form-control", "placeholder": "Greater Accra"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "CK-0001-8859"}),
            "landmark": forms.TextInput(attrs={"class": "form-control", "placeholder": "Near Cycle Bus Stop"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "0029758587"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Akwasi Aboagye"}),
        }

class TrackDeliveryItemForm(forms.ModelForm):
    class Meta:
        model = TrackDeliveryItem
        fields = ['current_status']

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