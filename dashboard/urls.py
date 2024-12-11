from django.urls import path

from . import views
from notifications.views import my_notifications

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='edit'),
    path('approve_booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('decline_booking/<int:booking_id>/', views.decline_booking, name='decline_booking'),
    path('my_spaces/', views.load_section, name='my_spaces'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('my_users/', views.my_users, name='my_users'),  # URL to manage users
    path('my_notifications/', my_notifications, name='my_notifications'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('users/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('users/reactivate/<int:user_id>/', views.reactivate_user, name='reactivate_user'),
    path('archive/<int:booking_id>/', views.archive_booking, name='archive'),
]