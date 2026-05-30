from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from properties.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls')),
    path('favorites/', include('favorites.urls')),
    path('inquiries/', include('inquiries.urls')),
    path('transactions/', include('transactions.urls')),
    path('dashboard/', include('dashboard.urls')),
]

# Serve static and media files (works even with DEBUG = False)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)