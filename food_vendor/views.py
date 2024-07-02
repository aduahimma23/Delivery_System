from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *

@login_required
def create_discount(request):
    if request.POST == "POST":
        form = MenuItemPriceDiscountForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            messages.success(request, "Discount creeated")
            return redirect("vendor_dashboard")
    else:
        form = MenuItemPriceDiscount()
    
    return render(request, "", {"form": form})

