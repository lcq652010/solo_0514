from rest_framework import serializers
from .models import (Department, Employee, AttendanceRecord, LeaveRequest, Overtime, 
                     AttendanceStatistics, SalaryCalculation, ApprovalLog, CompensatoryLeave,
                     MonthlySummary, LeaveBalance, ArchiveRecord)
from datetime import datetime, date


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.IntegerField(source='department.id', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    emp_id = serializers.CharField(source='employee.emp_id', read_only=True)
    department_id = serializers.IntegerField(source='employee.department.id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    exception_type_display = serializers.CharField(source='get_exception_type_display', read_only=True)
    check_in_formatted = serializers.SerializerMethodField()
    check_out_formatted = serializers.SerializerMethodField()
    attendance_date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = '__all__'
        read_only_fields = ['attendance_no', 'late_minutes', 'early_leave_minutes', 
                           'is_exception', 'exception_type', 'exception_desc']

    def get_check_in_formatted(self, obj):
        if obj.check_in:
            return obj.check_in.strftime('%Y-%m-%d %H:%M:%S')
        return ''

    def get_check_out_formatted(self, obj):
        if obj.check_out:
            return obj.check_out.strftime('%Y-%m-%d %H:%M:%S')
        return ''

    def get_attendance_date_formatted(self, obj):
        if obj.attendance_date:
            return obj.attendance_date.strftime('%Y-%m-%d')
        return ''


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    emp_id = serializers.CharField(source='employee.emp_id', read_only=True)
    department_id = serializers.IntegerField(source='employee.department.id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    start_date_formatted = serializers.SerializerMethodField()
    end_date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ['leave_no']

    def get_start_date_formatted(self, obj):
        if obj.start_date:
            return obj.start_date.strftime('%Y-%m-%d')
        return ''

    def get_end_date_formatted(self, obj):
        if obj.end_date:
            return obj.end_date.strftime('%Y-%m-%d')
        return ''


class OvertimeSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    emp_id = serializers.CharField(source='employee.emp_id', read_only=True)
    department_id = serializers.IntegerField(source='employee.department.id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    overtime_type_display = serializers.CharField(source='get_overtime_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    discrepancy_type_display = serializers.CharField(source='get_discrepancy_type_display', read_only=True)
    overtime_date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Overtime
        fields = '__all__'
        read_only_fields = ['overtime_no', 'actual_hours', 'hours_discrepancy', 
                           'discrepancy_type', 'has_discrepancy']

    def get_overtime_date_formatted(self, obj):
        if obj.overtime_date:
            return obj.overtime_date.strftime('%Y-%m-%d')
        return ''


class AttendanceStatisticsSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    emp_id = serializers.CharField(source='employee.emp_id', read_only=True)
    department_id = serializers.IntegerField(source='employee.department.id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    attendance_rate = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceStatistics
        fields = '__all__'
        read_only_fields = ['statistic_no']

    def get_attendance_rate(self, obj):
        if obj.work_days > 0:
            rate = (obj.actual_days / obj.work_days) * 100
            return round(rate, 2)
        return 0


class SalaryCalculationSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    emp_id = serializers.CharField(source='employee.emp_id', read_only=True)
    department_id = serializers.IntegerField(source='employee.department.id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    total_deduction = serializers.SerializerMethodField()

    class Meta:
        model = SalaryCalculation
        fields = '__all__'
        read_only_fields = ['salary_no']

    def get_total_deduction(self, obj):
        return float(obj.leave_deduction) + float(obj.late_deduction) + float(obj.absent_deduction)


class ApprovalLogSerializer(serializers.ModelSerializer):
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    related_type_display = serializers.CharField(source='get_related_type_display', read_only=True)

    class Meta:
        model = ApprovalLog
        fields = '__all__'
        read_only_fields = ['log_no']


class CompensatoryLeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    emp_id = serializers.CharField(source='employee.emp_id', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    overtime_no = serializers.CharField(source='source_overtime.overtime_no', read_only=True)

    class Meta:
        model = CompensatoryLeave
        fields = '__all__'
        read_only_fields = ['cl_no', 'remaining_hours', 'status']


class MonthlySummarySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = MonthlySummary
        fields = '__all__'
        read_only_fields = ['summary_no']


class LeaveBalanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    emp_id = serializers.CharField(source='employee.emp_id', read_only=True)

    class Meta:
        model = LeaveBalance
        fields = '__all__'
        read_only_fields = ['lb_no', 'annual_leave_remaining', 'sick_leave_remaining',
                           'personal_leave_remaining', 'compensatory_leave_remaining']


class ArchiveRecordSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    archive_type_display = serializers.CharField(source='get_archive_type_display', read_only=True)
    file_size_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ArchiveRecord
        fields = '__all__'
        read_only_fields = ['archive_no']

    def get_file_size_formatted(self, obj):
        if obj.file_size < 1024:
            return f'{obj.file_size} B'
        elif obj.file_size < 1024 * 1024:
            return f'{obj.file_size / 1024:.2f} KB'
        else:
            return f'{obj.file_size / (1024 * 1024):.2f} MB'
