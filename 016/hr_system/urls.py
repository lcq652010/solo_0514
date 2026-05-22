from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'positions', views.PositionViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'attendances', views.AttendanceViewSet)
router.register(r'leaves', views.LeaveViewSet)
router.register(r'overtimes', views.OvertimeViewSet)
router.register(r'salaries', views.SalaryViewSet)
router.register(r'payslips', views.PayslipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('statistics/attendance/', views.attendance_statistics, name='attendance-statistics'),
    path('statistics/salary/', views.salary_statistics, name='salary-statistics'),
]