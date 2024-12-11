from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
    path('edit_profile/', views.edit_admin_profile, name='edit_admin_profile'),
    path('admin_spaces/', views.admin_spaces, name='admin_spaces'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('get_space/<int:space_id>/', views.get_space, name='get_space'),
    path('edit_space/', views.edit_space, name='edit_space'),
    path('admin_reservations/', views.admin_reservations, name='admin_reservations'),
    path('approve_reservation/<int:reservation_id>/', views.approve_reservation, name='approve_reservation'),
    path('decline_reservation/<int:reservation_id>/', views.decline_reservation, name='decline_reservation'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'), #new
    path('delete_space/<int:space_id>/', views.delete_space, name='delete_space'),#new
    path('edit_user_details/<int:user_id>/', views.edit_user_details, name='edit_user_details'), #ambot
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'), #new
    path('admin_edit_user_from_admin_dashboard/', views.edit_user_from_admin_dashboard, name='edit_user_from_admin_dashboard'), #ambot
    #users
    
    path('user-profile/', views.user_profile, name='user_profile'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('user_spaces/', views.user_spaces, name='user_spaces'),
    path('user_home/', views.user_home, name='user_home'),
    path('reserve_space/', views.reserve_space, name='reserve_space'),
    path('user_reservation/', views.user_reservation, name='user_reservation'),

]
