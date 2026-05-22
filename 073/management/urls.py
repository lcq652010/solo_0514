from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, CoachViewSet, VehicleViewSet,
    CoachScheduleViewSet, TrainingAppointmentViewSet,
    TrainingRecordViewSet, FeeSettlementViewSet,
    SubjectHourConfigViewSet, StudentSubjectStatsViewSet
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'coaches', CoachViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'subject-hour-configs', SubjectHourConfigViewSet)
router.register(r'student-subject-stats', StudentSubjectStatsViewSet)
router.register(r'coach-schedules', CoachScheduleViewSet)
router.register(r'training-appointments', TrainingAppointmentViewSet)
router.register(r'training-records', TrainingRecordViewSet)
router.register(r'fee-settlements', FeeSettlementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
