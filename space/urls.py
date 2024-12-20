from django.urls import path

from . import views

app_name = 'space'

urlpatterns = [
    path('', views.space_list, name='spaces'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('add/', views.add_space, name='add'),
]