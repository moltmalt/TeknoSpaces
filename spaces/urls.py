from django.urls import path
from . import views

urlpatterns = [
    path('', views.spaces_list, name = 'spaces')
]