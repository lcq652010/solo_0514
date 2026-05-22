from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet, EmployeeViewSet, AttendanceRecordViewSet,
    LeaveRequestViewSet, OvertimeViewSet, AttendanceStatisticsViewSet,
    SalaryCalculationViewSet, ExportViewSet, MonthlySummaryViewSet,
    CompensatoryLeaveViewSet, LeaveBalanceViewSet, ApprovalLogViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance-records', AttendanceRecordViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'overtimes', OvertimeViewSet)
router.register(r'attendance-statistics', AttendanceStatisticsViewSet)
router.register(r'salary-calculations', SalaryCalculationViewSet)
router.register(r'monthly-summaries', MonthlySummaryViewSet)
router.register(r'compensatory-leaves', CompensatoryLeaveViewSet)
router.register(r'leave-balances', LeaveBalanceViewSet)
router.register(r'approval-logs', ApprovalLogViewSet)
router.register(r'exports', ExportViewSet, basename='export')

urlpatterns = [
    path('', include(router.urls)),
]
