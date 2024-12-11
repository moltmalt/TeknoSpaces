# urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('my_notifications/', views.my_notifications, name='my_notifications'),
    path('delete/', views.delete_notification, name='delete_notification'),

]