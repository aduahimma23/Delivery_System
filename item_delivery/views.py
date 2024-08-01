from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from .forms import *
from .utils import send_sms


current_time = timezone.now()

def home_view(request):
    recent_deliveries = DeliveryItem.objects.filter(status = "Delivered").order_by("-delivery_date")[:3]
    pending_deliveries = DeliveryItem.objects.filter(status = "In Transit").order_by("-created_at")[:3]
    # cancelled_deliveries = CancelDeliveryItem.objects.filter(delivery_item.status = "Cancelled").order_by("-cancelled_date")[:2]
    if request.method == "POST":
        form = DeliveryItemForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect("success")
    else:
        form = DeliveryItemForm()

    context = {
        "form": form,
        "recent_delivered": recent_deliveries,
        "pending_deliveries": pending_deliveries

    }
    return render(request, "item_delivery/index.html", context)

def item_delivery_view(request):
    if request.method == "POST":
        form = DeliveryItemForm(request.POST)
        if form.is_valid():
            delivery_item = form.save(commit=False)
            delivery_item.save()
            
            receiver = ReceiverDetails.objects.get(delivery_item=delivery_item)
            # Send an SMS to the receiver
            send_sms(
                receiver.phone_number,
                f"Your item has been submitted successfully. Tracking number: {delivery_item.tracking_number}"
            )
            return redirect('item_delivery_details')
    else:
        form = DeliveryItemForm()
    
    # if request.method == 'POST':
    #     item_description = request.POST['item_description']
    #     item_weight = request.POST['item_weight']
    #     delivery_date = request.POST['delivery_date']
    #     special_instructions = request.POST.get('special_instructions', '')

    #     delivery_item = DeliveryItem.objects.create(
    #         item_description=item_description,
    #         item_weight=item_weight,
    #         delivery_date=delivery_date,
    #         special_instructions=special_instructions
    #     )

    #     return redirect('track', tracking_number=delivery_item.tracking_number)
    
    return render(request, "item_delivery/details.html", {"form": form})


# @login_required
def sender_details_view(request):
    # try:
    #     previous_data = SenderDetails.objects.filter(sender=request.user).latest('sent_at')
    #     initial_data = {
    #         'address': previous_data.address,
    #         'city': previous_data.city,
    #         'region': previous_data.region,
    #         'postal_code': previous_data.postal_code,
    #     }
    # except SenderDetails.DoesNotExist:
    #     initial_data = {}

    if request.method == 'POST':
        # Get the delivery_item_id from the POST data
        delivery_item_id = request.POST.get('delivery_item_id')

        # Define form here to ensure it exists in case of an error
        form = SenderDetailsForm(request.POST)
        try:
            delivery_item = DeliveryItem.objects.get(id=delivery_item_id)
        except DeliveryItem.DoesNotExist:
            # Handle the case where the DeliveryItem does not exist
            return render(request, "item_delivery/send.html", {'form': form, 'error': 'Invalid delivery item ID'})

        if form.is_valid():
            sender_details = form.save(commit=False)
            sender_details.sender = request.user
            sender_details.delivery_item = delivery_item
            sender_details.save()
            return redirect('success_url')
    else:
        # initial=initial_data
        form = SenderDetailsForm()
    
    return render(request, "item_delivery/send.html", {'form': form})

# @login_required
def receiver_details_view(request,):
    try:
        delivery_item = DeliveryItem.objects.get()
    except DeliveryItem.DoesNotExist:
        return render(request, "item_delivery/receiver_details.html", {'error': 'Invalid delivery item ID'})

    try:
        sender_details = delivery_item.senders.latest('sent_at')  # Adjust this if necessary
    except SenderDetails.DoesNotExist:
        return render(request, "item_delivery/receiver_details.html", {'error': 'Sender details not found for this delivery item'})

    if request.method == 'POST':
        form = ReceiverDetailsForm(request.POST)
        if form.is_valid():
            receiver_details = form.save(commit=False)
            receiver_details.delivery_item = delivery_item
            receiver_details.sender = sender_details
            receiver_details.save()
            return redirect('success_url')
    else:
        form = ReceiverDetailsForm()

    return render(request, "item_delivery/receiver_details.html", {'form': form, 'delivery_item': delivery_item})

def tracking_view(request, tracking_number):
    track_item = get_object_or_404(
        TrackDeliveryItem, delivery_item_tracking_number = tracking_number
    )
    context = {
        "track_item": track_item,
        "location_updates": track_item.location_updates
    }
    return render(request, "item_delivery/track_item.html", context)

def cancel_delivery_view(request, item_id):
    delivery_item = DeliveryItem.objects.get(pk=item_id)
    if request.method == "POST":
        form = CancelDeliveryItemForm(request.POST)
        try:
            if form.is_valid():
                cancel_delivery_item = form.save(commit=False)
                cancel_delivery_item.delivery_item = delivery_item
                cancel_delivery_item.save()
                return redirect("home")
        except Exception as e:
            raise ValueError(request, f"You can't submit without a reason{e}")
    else:
        form = CancelDeliveryItemForm()
    
    return render(request, "item_delivery/cancel_item.html", {'form': form, 'delivery_item': delivery_item})