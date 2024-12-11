# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='prof_pic', blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, unique=True) 
    email = models.EmailField(blank=True)
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    year_level = models.IntegerField(null=True, blank=True, default=1)
    usertype = models.CharField(max_length=10, choices=[('student', 'Student'), ('faculty', 'Faculty'), ('admin', 'Admin')])
    program = models.CharField(max_length=100, null=True, default='Unrecorded')
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

# This should be already done in settings.py
# AUTH_USER_MODEL = 'accounts.CustomUser'