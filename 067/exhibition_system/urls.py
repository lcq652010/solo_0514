from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exhibition.views import (
    BoothViewSet,
    CompanyViewSet,
    BookingViewSet,
    ConstructionDemandViewSet,
    ProgressTrackerViewSet,
    PaymentViewSet,
    ExhibitionViewSet,
    BuilderViewSet,
    ConstructionConfirmViewSet,
    ProgressStepTemplateViewSet,
    ProgressStepViewSet,
    SalesDashboardViewSet,
)

router = DefaultRouter()
router.register(r'booths', BoothViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'construction-demands', ConstructionDemandViewSet)
router.register(r'progress', ProgressTrackerViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'exhibitions', ExhibitionViewSet)
router.register(r'builders', BuilderViewSet)
router.register(r'construction-confirms', ConstructionConfirmViewSet)
router.register(r'progress-step-templates', ProgressStepTemplateViewSet)
router.register(r'progress-steps', ProgressStepViewSet)
router.register(r'sales-dashboard', SalesDashboardViewSet, basename='sales-dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
