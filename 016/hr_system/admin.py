from django.contrib import admin
from .models import Department, Position, Employee, Attendance, Leave, Overtime, Salary, Payslip


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'base_salary', 'created_at')
    list_filter = ('department',)
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'gender', 'department', 'position', 
                    'hire_date', 'status', 'base_salary')
    list_filter = ('department', 'position', 'status', 'gender')
    search_fields = ('name', 'employee_id', 'phone', 'id_card')
    readonly_fields = ('employee_id',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status', 'work_hours')
    list_filter = ('status', 'date')
    search_fields = ('employee__name', 'employee__employee_id')
    date_hierarchy = 'date'


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 
                    'days', 'status', 'approver')
    list_filter = ('leave_type', 'status')
    search_fields = ('employee__name',)
    readonly_fields = ('days',)


@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'overtime_type', 'date', 'start_time', 
                    'end_time', 'hours', 'status', 'approver')
    list_filter = ('overtime_type', 'status', 'date')
    search_fields = ('employee__name',)
    readonly_fields = ('hours',)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'month', 'base_salary', 'overtime_pay',
                    'bonus', 'deduction', 'net_salary')
    list_filter = ('year', 'month')
    search_fields = ('employee__name', 'employee__employee_id')
    readonly_fields = ('overtime_pay', 'late_deduction', 'early_leave_deduction',
                       'absent_deduction', 'leave_deduction', 'deduction',
                       'work_days', 'late_count', 'early_leave_count',
                       'absent_count', 'overtime_hours', 'net_salary')


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('payslip_no', 'salary', 'issued', 'issued_at', 'created_at')
    list_filter = ('issued', 'created_at')
    search_fields = ('payslip_no', 'salary__employee__name')
    readonly_fields = ('payslip_no',)