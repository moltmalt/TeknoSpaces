from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from . import views
from . views import CustomLoginView


app_name = 'core'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name='about_us'),
    path('log_in/', CustomLoginView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
]
