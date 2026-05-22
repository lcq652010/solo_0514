from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hospital.views import *

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'pets', PetViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'charges', ChargeViewSet)
router.register(r'inventory-logs', InventoryLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/user-info/', get_user_info, name='user-info'),
]
