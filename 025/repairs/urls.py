from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepairWorkerViewSet, RepairViewSet, RepairLogViewSet

router = DefaultRouter()
router.register(r'workers', RepairWorkerViewSet)
router.register(r'repairs', RepairViewSet)
router.register(r'logs', RepairLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
