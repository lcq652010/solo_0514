from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rental.views import (
    DeviceViewSet,
    InstitutionViewSet,
    RentalViewSet,
    CalibrationViewSet,
    DamageRecordViewSet,
    MaintenanceRecordViewSet,
    ReturnAcceptanceViewSet,
    SettlementViewSet,
    DashboardViewSet,
)

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'rentals', RentalViewSet)
router.register(r'calibrations', CalibrationViewSet)
router.register(r'damage-records', DamageRecordViewSet)
router.register(r'maintenance-records', MaintenanceRecordViewSet)
router.register(r'return-acceptances', ReturnAcceptanceViewSet)
router.register(r'settlements', SettlementViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
