from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet,
    CustomerViewSet,
    ServiceViewSet,
    AuntViewSet,
    OrderViewSet,
    ReviewViewSet,
    OrderArchiveViewSet,
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'customers', CustomerViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'aunts', AuntViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'archives', OrderArchiveViewSet, basename='archive')

urlpatterns = [
    path('', include(router.urls)),
]
