from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/owners/', include('owners.urls')),
    path('api/bills/', include('bills.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/repairs/', include('repairs.urls')),
]
