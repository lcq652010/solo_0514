from django.contrib import admin
from .models import Department, Employee, AttendanceRecord, LeaveRequest, Overtime, AttendanceStatistics, SalaryCalculation


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'name', 'gender', 'department', 'position', 'base_salary', 'hire_date', 'is_active']
    list_filter = ['department', 'gender', 'is_active']
    search_fields = ['name', 'emp_id', 'phone', 'email']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['attendance_no', 'employee', 'attendance_date', 'check_in', 'check_out', 
                   'status', 'work_hours', 'late_minutes', 'early_leave_minutes', 'is_exception']
    list_filter = ['status', 'attendance_date', 'is_exception', 'exception_type']
    search_fields = ['attendance_no', 'employee__name', 'employee__emp_id']
    date_hierarchy = 'attendance_date'
    readonly_fields = ['attendance_no', 'late_minutes', 'early_leave_minutes', 
                      'is_exception', 'exception_type', 'exception_desc']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['leave_no', 'employee', 'leave_type', 'start_date', 'end_date', 
                   'days', 'status', 'approver', 'created_at']
    list_filter = ['leave_type', 'status', 'created_at']
    search_fields = ['leave_no', 'employee__name', 'employee__emp_id']
    readonly_fields = ['leave_no']


@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):
    list_display = ['overtime_no', 'employee', 'overtime_type', 'overtime_date', 
                   'start_time', 'end_time', 'hours', 'actual_hours', 
                   'has_discrepancy', 'status', 'approver']
    list_filter = ['overtime_type', 'status', 'discrepancy_type', 'overtime_date']
    search_fields = ['overtime_no', 'employee__name', 'employee__emp_id']
    readonly_fields = ['overtime_no', 'actual_hours', 'hours_discrepancy', 
                       'discrepancy_type', 'has_discrepancy']


@admin.register(AttendanceStatistics)
class AttendanceStatisticsAdmin(admin.ModelAdmin):
    list_display = ['statistic_no', 'employee', 'year', 'month', 'work_days', 
                   'actual_days', 'late_times', 'early_leave_times', 
                   'absent_days', 'leave_days', 'overtime_hours']
    list_filter = ['year', 'month']
    search_fields = ['statistic_no', 'employee__name', 'employee__emp_id']
    readonly_fields = ['statistic_no']


@admin.register(SalaryCalculation)
class SalaryCalculationAdmin(admin.ModelAdmin):
    list_display = ['salary_no', 'employee', 'year', 'month', 'base_salary', 
                   'overtime_pay', 'leave_deduction', 'late_deduction', 
                   'absent_deduction', 'bonus', 'net_salary']
    list_filter = ['year', 'month']
    search_fields = ['salary_no', 'employee__name', 'employee__emp_id']
    readonly_fields = ['salary_no']
