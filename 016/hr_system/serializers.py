from rest_framework import serializers
from .models import Department, Position, Employee, Attendance, Leave, Overtime, Salary, Payslip


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Position
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')
    position_name = serializers.ReadOnlyField(source='position.name')

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['employee_id']


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    status_display = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Attendance
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    leave_type_display = serializers.ReadOnlyField(source='get_leave_type_display')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    approver_name = serializers.ReadOnlyField(source='approver.name')

    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = ['days']


class OvertimeSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    overtime_type_display = serializers.ReadOnlyField(source='get_overtime_type_display')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    approver_name = serializers.ReadOnlyField(source='approver.name')

    class Meta:
        model = Overtime
        fields = '__all__'
        read_only_fields = ['hours']


class SalarySerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    department_name = serializers.ReadOnlyField(source='employee.department.name')

    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ['overtime_pay', 'late_deduction', 'early_leave_deduction', 
                            'absent_deduction', 'leave_deduction', 'deduction', 
                            'work_days', 'late_count', 'early_leave_count', 
                            'absent_count', 'overtime_hours', 'net_salary']


class PayslipSerializer(serializers.ModelSerializer):
    salary_detail = SalarySerializer(source='salary', read_only=True)

    class Meta:
        model = Payslip
        fields = '__all__'
        read_only_fields = ['payslip_no']