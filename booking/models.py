from django.db import models
from django.conf import settings
from space.models import Space

class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, default='2003-08-04')
    start_time = models.TimeField()
    end_time = models.TimeField()
    request_letter = models.FileField(upload_to='request_letters/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Booking for {self.user} on {self.date} for {self.space}'