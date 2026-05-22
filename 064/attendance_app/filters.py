import django_filters
from django.db.models import Q
from .models import AttendanceRecord, LeaveRequest, Overtime, AttendanceStatistics, SalaryCalculation, Employee


class EmployeeFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name='department_id')
    is_active = django_filters.BooleanFilter()
    keyword = django_filters.CharFilter(method='filter_keyword')

    class Meta:
        model = Employee
        fields = ['department', 'is_active', 'gender']

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(emp_id__icontains=value) | Q(phone__icontains=value)
        )


class AttendanceRecordFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name='employee__department_id')
    employee = django_filters.NumberFilter(field_name='employee_id')
    start_date = django_filters.DateFilter(field_name='attendance_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='attendance_date', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status')
    is_exception = django_filters.BooleanFilter(method='filter_exception')
    keyword = django_filters.CharFilter(method='filter_keyword')

    class Meta:
        model = AttendanceRecord
        fields = ['department', 'employee', 'start_date', 'end_date', 'status', 'is_exception']

    def filter_exception(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(status__in=['late', 'early_leave', 'absent']) |
                Q(check_in__isnull=True) | Q(check_out__isnull=True)
            )
        return queryset

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(employee__name__icontains=value) | Q(employee__emp_id__icontains=value)
        )


class LeaveRequestFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name='employee__department_id')
    employee = django_filters.NumberFilter(field_name='employee_id')
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    leave_type = django_filters.CharFilter(field_name='leave_type')
    status = django_filters.CharFilter(field_name='status')
    keyword = django_filters.CharFilter(method='filter_keyword')

    class Meta:
        model = LeaveRequest
        fields = ['department', 'employee', 'start_date', 'end_date', 'leave_type', 'status']

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(employee__name__icontains=value) | Q(employee__emp_id__icontains=value)
        )


class OvertimeFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name='employee__department_id')
    employee = django_filters.NumberFilter(field_name='employee_id')
    start_date = django_filters.DateFilter(field_name='overtime_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='overtime_date', lookup_expr='lte')
    overtime_type = django_filters.CharFilter(field_name='overtime_type')
    status = django_filters.CharFilter(field_name='status')
    has_discrepancy = django_filters.BooleanFilter(method='filter_discrepancy')
    keyword = django_filters.CharFilter(method='filter_keyword')

    class Meta:
        model = Overtime
        fields = ['department', 'employee', 'start_date', 'end_date', 'overtime_type', 'status', 'has_discrepancy']

    def filter_discrepancy(self, queryset, name, value):
        if value:
            return queryset.filter(actual_hours__isnull=False)
        return queryset

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(employee__name__icontains=value) | Q(employee__emp_id__icontains=value)
        )


class AttendanceStatisticsFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name='employee__department_id')
    employee = django_filters.NumberFilter(field_name='employee_id')
    year = django_filters.NumberFilter(field_name='year')
    month = django_filters.NumberFilter(field_name='month')
    keyword = django_filters.CharFilter(method='filter_keyword')

    class Meta:
        model = AttendanceStatistics
        fields = ['department', 'employee', 'year', 'month']

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(employee__name__icontains=value) | Q(employee__emp_id__icontains=value)
        )


class SalaryCalculationFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name='employee__department_id')
    employee = django_filters.NumberFilter(field_name='employee_id')
    year = django_filters.NumberFilter(field_name='year')
    month = django_filters.NumberFilter(field_name='month')
    keyword = django_filters.CharFilter(method='filter_keyword')

    class Meta:
        model = SalaryCalculation
        fields = ['department', 'employee', 'year', 'month']

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(employee__name__icontains=value) | Q(employee__emp_id__icontains=value)
        )
