from django.urls import path
from . import views

urlpatterns = [
    path('admins/', views.admin_signup, name='admin_signup'),
    path('admins/success/', views.signup_success, name='signup_success'),
    path('login/', views.admin_login, name='admin_login'),
    path('home/', views.admin_home, name='admin_home'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
