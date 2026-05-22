from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, CoachViewSet, VehicleViewSet, ScheduleViewSet,
    TrainingReservationViewSet, ExamRegistrationViewSet, PaymentViewSet, 
    StudentArchiveViewSet, UserProfileViewSet, TrainingHoursViewSet, 
    TrainingArchiveViewSet, current_user_info
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'coaches', CoachViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'reservations', TrainingReservationViewSet)
router.register(r'exams', ExamRegistrationViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'archives', StudentArchiveViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'training-hours', TrainingHoursViewSet)
router.register(r'training-archives', TrainingArchiveViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('current-user/', current_user_info, name='current-user'),
]
