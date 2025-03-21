# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('app.urls')),  # Root URL points to app.urls
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('mentee/', include('mentee.urls')),
    path('case_manager/', include('case_manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)