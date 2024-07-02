from django import forms
from .models import MenuItemPriceDiscount

class MenuItemPriceDiscountForm(forms.ModelForm):
    model = MenuItemPriceDiscount
    fields = ['menu_item_price', 'discount_percent', 'start_date', 'end_date']
    widgets = {
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }


