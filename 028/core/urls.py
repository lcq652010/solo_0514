from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PackageViewSet, CustomerViewSet, PhotographerViewSet,
    AppointmentViewSet, OrderViewSet, SettlementViewSet,
    PhotoSelectionViewSet, AuthView, CurrentUserView, dashboard_stats
)

router = DefaultRouter()
router.register(r'packages', PackageViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'photographers', PhotographerViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'settlements', SettlementViewSet)
router.register(r'photo-selections', PhotoSelectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', AuthView.as_view(), name='auth'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('dashboard/', dashboard_stats, name='dashboard-stats'),
]
