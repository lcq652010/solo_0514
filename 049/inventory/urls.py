from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, StockRecordViewSet, StockAlertViewSet

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'stock-records', StockRecordViewSet)
router.register(r'stock-alerts', StockAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
