from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeStandardViewSet, BillViewSet, MeterReadingViewSet

router = DefaultRouter()
router.register(r'fee-standards', FeeStandardViewSet)
router.register(r'bills', BillViewSet)
router.register(r'meter-readings', MeterReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
