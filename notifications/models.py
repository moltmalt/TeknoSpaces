from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('approve', 'Approve'),
        ('decline', 'Decline'),
        ('message', 'Message'),
        ('booking_sent', 'Booking Sent'),
    ]

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.get_notification_type_display()} from {self.sender} to {self.receiver}'

    class Meta:
        ordering = ['-timestamp']