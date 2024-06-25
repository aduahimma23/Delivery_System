from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm

def is_food_vendor(user):
    return user.user_type == CustomUser.FOOD_VENDOR

def is_delivery_staff(user):
    return user.user_type == CustomUser.DELIVERY_STAFF

def is_customer(user):
    return user.user_type == CustomUser.CUSTOMER

def is_admin(user):
    return user.user_type == CustomUser.ADMIN

def is_intern_staff(user):
    return user.user_type == CustomUser.INTERN_STAFF

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})

@login_required(login_url='account:login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('main:home')

@login_required(login_url='account:login')
def dashboard(request):
    user = request.user
    context = {'user': user}

    if user.user_type == CustomUser.FOOD_VENDOR:
        return render(request, 'account/vendor_dashboard.html', context)
    elif user.user_type == CustomUser.DELIVERY_STAFF:
        return render(request, 'account/delivery_dashboard.html', context)
    elif user.user_type == CustomUser.CUSTOMER:
        return render(request, 'account/customer_dashboard.html', context)
    elif user.user_type == CustomUser.ADMIN:
        return render(request, 'account/admin_dashboard.html', context)
    elif user.user_type == CustomUser.INTERN_STAFF:
        return render(request, 'account/intern_dashboard.html', context)
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('account:login')
