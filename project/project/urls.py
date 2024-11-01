from django.contrib import admin
from django.urls import path, include  # include allows including app URLs

urlpatterns = [
    path('admin/', admin.site.urls),   # Admin panel URL
    path('accounts/', include('authentication.urls')),  # Include URLs from accounts app
    path('', include('app.urls')),
]
