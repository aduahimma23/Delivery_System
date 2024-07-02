from django import forms
from .models import (DeliveryAddress, OrderRewiew, CancelOrder, )
                    

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = "__all__"

class ReviewForm(forms.ModelForm):
    class Meta:
        model = OrderRewiew
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.order:
            raise forms.ValidationError("Order is required.")
        if not self.order.status:
            raise forms.ValidationError("You can only review delivered orders.")
        return cleaned_data
    

class CancelOrderForm(forms.ModelForm):
    class Meta:
        model = CancelOrder
        fields = ['reason']

