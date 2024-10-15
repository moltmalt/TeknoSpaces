from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.admin_signup, name='admin_signup'),
    path('login/', views.admin_login, name='admin_login'),
    path('home/', views.admin_home, name='admin_home'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
    path('edit_profile/', views.edit_admin_profile, name='edit_admin_profile'),
    path('admin_spaces/', views.admin_spaces, name='admin_spaces'),
]
