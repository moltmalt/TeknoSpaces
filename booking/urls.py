from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('space/<int:space_id>/calendar/', views.calendar_view, name='calendar')
]