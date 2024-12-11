from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib import messages



@login_required
def my_notifications(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by('-timestamp')
    
    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()

        # Redirection based on notification type
        if notification.notification_type == 'message':
            return redirect('conversation:inbox')  # Redirect to the conversation inbox
        elif notification.notification_type in ['approve', 'decline', 'booking_sent']:
            return redirect('dashboard:my_notifications')  # Redirect to My Spaces for booking-related notifications

    return render(request, 'notifications/my_notifications.html', {'notifications': notifications})

def delete_notification(request):
    if request.method == "POST":
        notification_id = request.POST.get("notification_id")
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            messages.success(request, "Notification deleted successfully.")
        except Notification.DoesNotExist:
            messages.error(request, "Notification not found.")
    return redirect('notifications:my_notifications')  # Redirect back to the notifications page