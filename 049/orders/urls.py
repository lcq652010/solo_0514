from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, WholesaleOrderViewSet, SettlementViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'wholesale-orders', WholesaleOrderViewSet)
router.register(r'settlements', SettlementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
