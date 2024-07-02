from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Order, OrderRewiew, CancelOrder, OrderTracking, OrderItem
from food_vendor.models import MenuItem, MenuItemPrice, Promotion, MenuCategory
from .forms import ReviewForm, CancelOrderForm

app_name = "main"

def home(request):
    return render(request, "main/index.html")

def menu_list(request):
    menu_items = MenuItem.objects.filter()
    return render(request, "main/menu.html", {"menu_items": menu_items})

# Add a cart item to carts
@login_required
def add_to_cart(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    cart, created = Order.objects.get_or_create(user=request.user, defaults={'created_at': timezone.now()})
    cart_item, created = OrderItem.objects.get_or_create(cart=cart, menu_item=menu_item, defaults={'quantity': 1})

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('order') 

# Removing the cart item from carts
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(OrderItem, id=cart_item_id)
    cart_item.delete()

    return JsonResponse({"status": "Success"})

# Updating the cart items
@login_required
def update_cart_item(request, cart_item_id, action):
    cart_item = get_object_or_404(OrderItem, id=cart_item_id)
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return JsonResponse({'status': 'success', 'quantity': cart_item.quantity})


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'main/orders/order_list.html', {'orders': orders})

# Order items views
def order_items_list(request):
    order_items = OrderItem.objects.all()
    return render(request, 'main/orders/shopping_cart.html', {'order_items': order_items})

@login_required
def create_review(request, order_id):
    order = get_object_or_404(OrderRewiew, id=order_id, user_profile=request.user.profile)
    if order.review:
        messages.error(request, "This order has already been reviewed.")
        return redirect('order_detail', order_id=order_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, order=order)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.user_profile = request.user.profile
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('order_detail', order_id=order.id)
    else:
        form = ReviewForm()

    return render(request, 'account/create_review.html', {'form': form, 'order': order})

@login_required
def track_order(request, order_id):
    order = get_object_or_404(OrderTracking, id=order_id, user_profile=request.user.profile)
    if order.status == Order.PENDING:
        messages.error(request, "You can only track orders that have been placed successfully.")
        return redirect("order_detail", order_id=order_id)
    
    tracking_events = order.tracking.all()

    return render(request, "main/orders/track_order.html", {"order": order, "tracking_events": tracking_events})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(CancelOrder, id=order_id, user=request.user)

    if request.method == 'POST':
        form = CancelOrderForm(request.POST)
        if form.is_valid():
            cancel_order = form.save(commit=False)
            cancel_order.order = order
            try:
                cancel_order.save()
                messages.success(request, 'Order canceled successfully.')
                return redirect('order_list')  # Assuming you have an order list view
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = CancelOrderForm()

    return render(request, 'main/orders/cancel_order.html', {'form': form, 'order': order})

# Applying promotions to the food item if the vendor is running a promotion.
def apply_promotions(menu_items):
    today = timezone.now().date()
    for item in menu_items:
        active_promotions = item.promotions.filter(start_date_lte=today, end_date_lte=today)
        if active_promotions.exists():
            promotion = active_promotions.first()
            item.discounted_price = item.price * (1 - promotion.discount / 100)
        else:
            item.discounted_price = item.price
    
    return menu_items

def menu_category(request, category_id):
    category = get_object_or_404(MenuCategory, id=category_id)
    menu_items = MenuItem.objects.filter(category=category)
    menu_items = apply_promotions(menu_items)

    return render(request, "", {'category': category, 'menu_items': menu_items})