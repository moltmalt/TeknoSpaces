from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from space.models import Space
from booking.models import Booking
from account.models import CustomUser
from account.forms import CustomUserForm
from django.http import JsonResponse
from .forms import BookingForm
from datetime import time
from django.urls import reverse
from django.contrib.auth import get_user_model
from notifications.models import Notification
from .forms import DeclineBookingForm


@login_required
def index(request):
    admin_spaces = Space.objects.filter(managed_by=request.user)  # Spaces managed by the user
    user_bookings = Booking.objects.filter(user=request.user)  # Get bookings by the user
    
    pending_bookings = user_bookings.filter(status='pending')
    approved_bookings = user_bookings.filter(status='approved')
    rejected_bookings = user_bookings.filter(status='rejected')
    archived_bookings = user_bookings.filter(status='archived')

    return render(request, 'dashboard/index.html', {
        'admin_spaces': admin_spaces,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'archived_bookings': archived_bookings,
    })

def user_update(request):
    user = request.user
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'dashboard/edit_profile.html', {'form': form})

def dashboard(request):
    return render(request, 'dashboard/index.html')

@login_required
def load_section(request):
    section = request.GET.get('section', 'my_spaces')
    template_name = f'dashboard/{section}.html'
    
    admin_spaces = Space.objects.filter(managed_by=request.user)  # Spaces managed by the user
    user_bookings = Booking.objects.filter(user=request.user)  # Get bookings by the user

    admin_bookings = admin_bookings = Booking.objects.filter(space__in=admin_spaces)
    admin_pending_bookings = admin_bookings.filter(status='pending')
    admin_approved_bookings = admin_bookings.filter(status='approved')
    admin_rejected_bookings = admin_bookings.filter(status='rejected')
    
    pending_bookings = user_bookings.filter(status='pending')
    approved_bookings = user_bookings.filter(status='approved')
    rejected_bookings = user_bookings.filter(status='rejected')
    archived_bookings = user_bookings.filter(status='archived')

    context = {
        'admin_spaces': admin_spaces,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'archived_bookings': archived_bookings,
        'admin_pending_bookings': admin_pending_bookings,
        'admin_approved_bookings': admin_approved_bookings,
        'admin_rejected_bookings': admin_rejected_bookings,
    }
    
    return render(request, template_name, context)

from django.db.models import Q
from datetime import datetime

@login_required
def approve_booking(request, booking_id):
    # Retrieve the booking instance
    booking = get_object_or_404(Booking, id=booking_id)
    booking_start = booking.start_time
    booking_end = booking.end_time
    booking_date = booking.date  # Get the date for the booking
    
    # Check for conflicting bookings for the same space and date
    conflicting_bookings = Booking.objects.filter(
        space=booking.space,  # Same space
        status='approved',  # Only consider approved bookings
        date=booking_date,   # Same date
    ).exclude(id=booking.id)  # Exclude the current booking from the conflict check

    # Check for overlapping times with existing approved bookings
    for existing_booking in conflicting_bookings:
        existing_start = existing_booking.start_time
        existing_end = existing_booking.end_time
        
        # Check if the times overlap
        if (booking_start < existing_end and booking_end > existing_start):
            messages.error(request, 'Conflicting booking found for the same slot on the same day.')
            return redirect('dashboard:index')  # Redirect back to my_bookings page

    # No conflict, approve the booking
    booking.status = 'approved'
    booking.save()

    admin_user = request.user
    target_user = booking.user

    if booking.space.price > 0:
        notification = Notification.objects.create(
            notification_type='approve',
            sender= admin_user,
            receiver=target_user,
            message='Your booking has been approved. Kindly settle the payment within today and tomorroe and submit the receipt to propertycustodian@cit.edu.',
            link = f'/spaces/{booking.space.id}/',
        )
    else:
        notification = Notification.objects.create(
            notification_type='approve',
            sender= admin_user,
            receiver=target_user,
            message='Your booking has been approved. Kindly email propertycustodian@cit.edu for asssistance.',
            link = f'/spaces/{booking.space.id}/',
        )
    
    messages.success(request, 'Booking approved successfully.')
    return redirect('dashboard:my_bookings')  # Redirect back to my_bookings page

@login_required
def decline_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = DeclineBookingForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            # Update the booking status and save the reason
            booking.status = 'rejected'
            booking.save()

            admin_user = request.user
            target_user = booking.user
            
            # Create a notification with the reason included
            notification = Notification.objects.create(
                notification_type='decline',
                sender=admin_user,
                receiver=target_user,
                message=f'Your booking has been declined. Reason: {reason}',
                link=f'/spaces/{booking.space.id}/'
            )

            messages.success(request, 'Booking declined successfully.')
            return redirect('dashboard:my_bookings')
    else:
        form = DeclineBookingForm()

    return render(request, 'dashboard/decline_booking.html', {'form': form, 'booking': booking})

@login_required
def my_bookings(request):
    
    admin_spaces = Space.objects.filter(managed_by=request.user)  # Spaces managed by the user

    admin_bookings = admin_bookings = Booking.objects.filter(space__in=admin_spaces)
    admin_pending_bookings = admin_bookings.filter(status='pending')
    admin_approved_bookings = admin_bookings.filter(status='approved')
    admin_rejected_bookings = admin_bookings.filter(status='rejected')
  

    context = {
        'admin_spaces': admin_spaces,
        'admin_pending_bookings': admin_pending_bookings,
        'admin_approved_bookings': admin_approved_bookings,
        'admin_rejected_bookings': admin_rejected_bookings,
    }
    
    return render(request, 'dashboard/my_bookings.html', context)

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            # Check for conflicts
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            space = form.cleaned_data['space']
            
            # Check if the time falls within the allowed range
            if start_time < time(8, 0) or end_time > time(17, 0):
                messages.error(request, "Booking must be between 8:00 AM and 5:00 PM.")
                return render(request, 'dashboard/edit_booking.html', {'form': form, 'booking': booking})
            else:
                conflict = Booking.objects.filter(
                    space=space,
                    date=date,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exclude(id=booking_id)

                if conflict.exists():
                    messages.error(request, "The selected time slot conflicts with another booking.")
                    print(form.errors)  # Check what's causing the form to be invalid
                    return render(request, 'dashboard/edit_booking.html', {'form': form, 'booking': booking})
                else:
                    form.save()
                    messages.success(request, "Booking updated successfully.")
                    print(form.errors)

                    notification = Notification.objects.create(
                        notification_type='messsage',
                        sender=request.user,
                        receiver=booking.user,
                        message='Your booking has been edited. Kindly check the changes.',
                        link = f'/spaces/{booking.space.id}/'
                    )
                        
                    return redirect('dashboard:my_bookings')
        else:
            # If form is invalid, re-render the form with errors
            messages.error(request, "There were some errors in the form.")
            print(form.errors)
            return render(request, 'dashboard/edit_booking.html', {'form': form, 'booking': booking})
    else:
        form = BookingForm(instance=booking)

    return render(request, 'dashboard/edit_booking.html', {'form': form, 'booking': booking})

User = get_user_model()

def my_users(request):
    # Fetch all users. You can filter by status if needed, e.g. active users only
    users = User.objects.all()
    return render(request, 'dashboard/my_users.html', {'users': users})

def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'inactive'
    user.save()

    # Reject all bookings for this user
    Booking.objects.filter(user=user).update(status='rejected')

    messages.success(request, f'User {user.username} has been deactivated and all their bookings have been rejected.')
    return redirect(reverse('dashboard:my_users'))

def reactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.status = 'active'
    user.save()
    messages.success(request, f'User {user.username} has been reactivated.')
    return redirect(reverse('dashboard:my_users'))

@login_required
def archive_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status == 'approved':  # Ensure only approved bookings can be archived
        booking.status = 'archived'
        booking.save()
    return redirect('dashboard:index')  # Adjust the redirect as needed