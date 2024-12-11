from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('spaces/', include('space.urls')),
    path('inbox/', include('conversation.urls')), 
    path('dashboard/', include('dashboard.urls')), 
    path('booking/', include('booking.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
