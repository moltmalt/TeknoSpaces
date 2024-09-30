# signup/urls.py
from django.urls import path
from . import views  # Make sure views is imported

urlpatterns = [
    path('signup/', views.admin_signup, name='admin_signup'),  
    path('signup/success/', views.signup_success, name='signup_success'),  # For sign-up success page
    path('login/', views.admin_login, name='admin_login'),  # Optional: Admin login page if needed
    path('home/', views.admin_home, name='admin_home'),  
    path('logout/', views.admin_logout, name='admin_logout')
]
    