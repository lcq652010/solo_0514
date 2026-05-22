"""
URL configuration for campus_supermarket project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('supermarket.urls')),
]
