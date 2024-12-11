from django.urls import path

from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/<int:space_pk>/', views.new_conversation, name='new'),
    path('conversation/mark_as_read/', views.mark_as_read, name='mark_as_read'),
    path('<int:conversation_id>/', views.conversation, name='detail'), 
    path('<int:conversation_id>/delete/', views.delete_conversation, name='delete'), 
]

