from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count, F, Avg
from django.utils import timezone
from datetime import datetime, date, timedelta
import calendar
import pandas as pd
from django.http import HttpResponse, FileResponse
from io import BytesIO
import os
from django.conf import settings

from .models import (Department, Employee, AttendanceRecord, LeaveRequest, Overtime, 
                     AttendanceStatistics, SalaryCalculation, ApprovalLog, CompensatoryLeave,
                     MonthlySummary, LeaveBalance, ArchiveRecord)
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, AttendanceRecordSerializer,
    LeaveRequestSerializer, OvertimeSerializer, AttendanceStatisticsSerializer,
    SalaryCalculationSerializer, ApprovalLogSerializer, CompensatoryLeaveSerializer,
    MonthlySummarySerializer, LeaveBalanceSerializer, ArchiveRecordSerializer
)
from .filters import (
    EmployeeFilter, AttendanceRecordFilter, LeaveRequestFilter, OvertimeFilter,
    AttendanceStatisticsFilter, SalaryCalculationFilter
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ['name', 'emp_id', 'phone', 'email']
    ordering_fields = ['emp_id', 'name', 'hire_date']
    ordering = ['emp_id']


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('employee', 'employee__department').all()
    serializer_class = AttendanceRecordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AttendanceRecordFilter
    search_fields = ['employee__name', 'employee__emp_id', 'attendance_no']
    ordering_fields = ['attendance_date', 'check_in', 'check_out']
    ordering = ['-attendance_date']

    @action(detail=False, methods=['POST'])
    def check_in(self, request):
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response({'error': '员工ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': '员工不存在'}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()
        record, created = AttendanceRecord.objects.get_or_create(
            employee=employee,
            attendance_date=today
        )

        if record.check_in:
            return Response({'error': '今日已签到'}, status=status.HTTP_400_BAD_REQUEST)

        record.check_in = timezone.now()
        record.save()
        
        serializer = self.get_serializer(record)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def check_out(self, request):
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response({'error': '员工ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': '员工不存在'}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()
        try:
            record = AttendanceRecord.objects.get(employee=employee, attendance_date=today)
        except AttendanceRecord.DoesNotExist:
            return Response({'error': '今日未签到'}, status=status.HTTP_400_BAD_REQUEST)

        if record.check_out:
            return Response({'error': '今日已签退'}, status=status.HTTP_400_BAD_REQUEST)

        record.check_out = timezone.now()
        
        if record.check_in:
            work_hours = (record.check_out - record.check_in).total_seconds() / 3600
            record.work_hours = round(work_hours, 2)
        
        record.save()
        
        serializer = self.get_serializer(record)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today_records(self, request):
        today = date.today()
        queryset = self.filter_queryset(self.queryset.filter(attendance_date=today))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exception_summary(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        department_id = request.query_params.get('department_id')

        queryset = self.queryset.filter(is_exception=True)
        if start_date:
            queryset = queryset.filter(attendance_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(attendance_date__lte=end_date)
        if department_id:
            queryset = queryset.filter(employee__department_id=department_id)

        summary = {
            'total_exceptions': queryset.count(),
            'by_type': dict(queryset.values('exception_type').annotate(count=Count('id')).values_list('exception_type', 'count')),
            'by_department': dict(queryset.values('employee__department__name').annotate(count=Count('id')).values_list('employee__department__name', 'count')),
        }
        return Response(summary)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related('employee', 'employee__department').all()
    serializer_class = LeaveRequestSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LeaveRequestFilter
    search_fields = ['employee__name', 'employee__emp_id', 'leave_no']
    ordering_fields = ['start_date', 'created_at', 'days']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        leave = LeaveRequest.objects.get(id=response.data['id'])
        employee = leave.employee
        leave_type = leave.leave_type
        
        balance, created = LeaveBalance.objects.get_or_create(
            employee=employee,
            year=date.today().year
        )
        
        if created:
            balance.annual_leave_total = 10
            balance.sick_leave_total = 12
            balance.personal_leave_total = 6
            balance.save()
        
        return response

    def _create_approval_log(self, obj, action_type, operator, remark=''):
        previous_status = obj.status
        new_status = 'approved' if action_type == 'approve' else 'rejected'
        
        ApprovalLog.objects.create(
            related_type='leave',
            related_id=obj.id,
            action_type=action_type,
            operator=operator,
            remark=remark,
            previous_status=previous_status,
            new_status=new_status
        )

    def _update_leave_balance(self, leave):
        if leave.status == 'approved':
            balance, _ = LeaveBalance.objects.get_or_create(
                employee=leave.employee,
                year=leave.start_date.year,
                defaults={'annual_leave_total': 10, 'sick_leave_total': 12, 'personal_leave_total': 6}
            )
            
            days = float(leave.days)
            if leave.leave_type == 'annual':
                balance.annual_leave_used = float(balance.annual_leave_used) + days
            elif leave.leave_type == 'sick':
                balance.sick_leave_used = float(balance.sick_leave_used) + days
            elif leave.leave_type == 'personal':
                balance.personal_leave_used = float(balance.personal_leave_used) + days
            balance.save()

    @action(detail=True, methods=['POST'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        approver = request.data.get('approver', '')
        remark = request.data.get('remark', '')

        previous_status = leave.status
        leave.status = 'approved'
        leave.approver = approver
        leave.approve_remark = remark
        leave.approve_time = timezone.now()
        leave.save()

        self._create_approval_log(leave, 'approve', approver, remark)
        self._update_leave_balance(leave)

        serializer = self.get_serializer(leave)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        approver = request.data.get('approver', '')
        remark = request.data.get('remark', '')

        leave.status = 'rejected'
        leave.approver = approver
        leave.approve_remark = remark
        leave.approve_time = timezone.now()
        leave.save()

        self._create_approval_log(leave, 'reject', approver, remark)

        serializer = self.get_serializer(leave)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def transfer(self, request, pk=None):
        leave = self.get_object()
        operator = request.data.get('operator', '')
        next_approver = request.data.get('next_approver', '')
        remark = request.data.get('remark', '')

        ApprovalLog.objects.create(
            related_type='leave',
            related_id=leave.id,
            action_type='transfer',
            operator=operator,
            remark=remark,
            previous_status=leave.status,
            new_status=leave.status,
            next_approver=next_approver
        )

        serializer = self.get_serializer(leave)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        queryset = self.filter_queryset(self.queryset.filter(status='pending'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def approval_history(self, request):
        employee_id = request.query_params.get('employee_id')
        queryset = ApprovalLog.objects.filter(related_type='leave')
        if employee_id:
            queryset = queryset.filter(related_id__in=LeaveRequest.objects.filter(employee_id=employee_id).values('id'))
        serializer = ApprovalLogSerializer(queryset, many=True)
        return Response(serializer.data)


class OvertimeViewSet(viewsets.ModelViewSet):
    queryset = Overtime.objects.select_related('employee', 'employee__department').all()
    serializer_class = OvertimeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OvertimeFilter
    search_fields = ['employee__name', 'employee__emp_id', 'overtime_no']
    ordering_fields = ['overtime_date', 'hours', 'created_at']
    ordering = ['-created_at']

    def _convert_to_compensatory_leave(self, overtime, approver):
        overtime_date = overtime.overtime_date
        valid_from = overtime_date + timedelta(days=1)
        valid_to = date(overtime_date.year, 12, 31)
        
        conversion_rate = 1.0
        if overtime.overtime_type == 'holiday':
            conversion_rate = 1.5
        elif overtime.overtime_type == 'weekend':
            conversion_rate = 1.2
        
        total_hours = float(overtime.hours) * conversion_rate
        
        CompensatoryLeave.objects.create(
            employee=overtime.employee,
            source_overtime=overtime,
            overtime_hours=float(overtime.hours),
            total_hours=total_hours,
            conversion_rate=conversion_rate,
            valid_from=valid_from,
            valid_to=valid_to,
            remark=f'由加班{overtime.overtime_no}自动折算，折算率：{conversion_rate}'
        )
        
        balance, created = LeaveBalance.objects.get_or_create(
            employee=overtime.employee,
            year=overtime_date.year,
            defaults={'annual_leave_total': 10, 'sick_leave_total': 12, 'personal_leave_total': 6}
        )
        balance.compensatory_leave_total = float(balance.compensatory_leave_total) + total_hours
        balance.save()

    @action(detail=True, methods=['POST'])
    def approve(self, request, pk=None):
        overtime = self.get_object()
        approver = request.data.get('approver', '')
        remark = request.data.get('remark', '')
        convert_to_cl = request.data.get('convert_to_cl', True)

        previous_status = overtime.status
        overtime.status = 'approved'
        overtime.approver = approver
        overtime.approve_remark = remark
        overtime.approve_time = timezone.now()
        overtime.save()

        ApprovalLog.objects.create(
            related_type='overtime',
            related_id=overtime.id,
            action_type='approve',
            operator=approver,
            remark=remark,
            previous_status=previous_status,
            new_status='approved'
        )

        if convert_to_cl:
            self._convert_to_compensatory_leave(overtime, approver)

        serializer = self.get_serializer(overtime)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def reject(self, request, pk=None):
        overtime = self.get_object()
        approver = request.data.get('approver', '')
        remark = request.data.get('remark', '')

        previous_status = overtime.status
        overtime.status = 'rejected'
        overtime.approver = approver
        overtime.approve_remark = remark
        overtime.approve_time = timezone.now()
        overtime.save()

        ApprovalLog.objects.create(
            related_type='overtime',
            related_id=overtime.id,
            action_type='reject',
            operator=approver,
            remark=remark,
            previous_status=previous_status,
            new_status='rejected'
        )

        serializer = self.get_serializer(overtime)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        queryset = self.filter_queryset(self.queryset.filter(status='pending'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def discrepancy_summary(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        queryset = self.queryset.filter(has_discrepancy=True)
        if year:
            queryset = queryset.filter(overtime_date__year=year)
        if month:
            queryset = queryset.filter(overtime_date__month=month)

        summary = {
            'total_with_discrepancy': queryset.count(),
            'by_type': dict(queryset.values('discrepancy_type').annotate(count=Count('id')).values_list('discrepancy_type', 'count')),
            'avg_discrepancy': queryset.aggregate(avg=Avg('hours_discrepancy'))['avg'] or 0,
        }
        return Response(summary)


class AttendanceStatisticsViewSet(viewsets.ModelViewSet):
    queryset = AttendanceStatistics.objects.select_related('employee', 'employee__department').all()
    serializer_class = AttendanceStatisticsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AttendanceStatisticsFilter
    search_fields = ['employee__name', 'employee__emp_id', 'statistic_no']
    ordering_fields = ['year', 'month', 'actual_days']
    ordering = ['-year', '-month']

    @action(detail=False, methods=['POST'])
    def generate_statistics(self, request):
        year = int(request.data.get('year'))
        month = int(request.data.get('month'))

        employees = Employee.objects.filter(is_active=True)
        results = []

        for employee in employees:
            statistic, created = AttendanceStatistics.objects.get_or_create(
                employee=employee,
                year=year,
                month=month
            )

            _, work_days = calendar.monthrange(year, month)
            statistic.work_days = work_days

            records = AttendanceRecord.objects.filter(
                employee=employee,
                attendance_date__year=year,
                attendance_date__month=month
            )

            statistic.actual_days = records.exclude(check_in__isnull=True).count()
            statistic.late_times = records.filter(status='late').count()
            statistic.early_leave_times = records.filter(status='early_leave').count()
            statistic.absent_days = records.filter(status='absent').count()

            total_work_hours = records.aggregate(total=Sum('work_hours'))['total'] or 0
            statistic.total_work_hours = total_work_hours

            approved_leaves = LeaveRequest.objects.filter(
                employee=employee,
                status='approved',
                start_date__year=year,
                start_date__month=month
            )
            total_leave_days = approved_leaves.aggregate(total=Sum('days'))['total'] or 0
            statistic.leave_days = total_leave_days

            approved_overtimes = Overtime.objects.filter(
                employee=employee,
                status='approved',
                overtime_date__year=year,
                overtime_date__month=month
            )
            total_overtime_hours = approved_overtimes.aggregate(total=Sum('hours'))['total'] or 0
            statistic.overtime_hours = total_overtime_hours

            statistic.save()
            results.append(statistic)

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        queryset = self.queryset
        if year and month:
            queryset = queryset.filter(year=int(year), month=int(month))
        
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SalaryCalculationViewSet(viewsets.ModelViewSet):
    queryset = SalaryCalculation.objects.select_related('employee', 'employee__department').all()
    serializer_class = SalaryCalculationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SalaryCalculationFilter
    search_fields = ['employee__name', 'employee__emp_id', 'salary_no']
    ordering_fields = ['year', 'month', 'net_salary']
    ordering = ['-year', '-month']

    @action(detail=False, methods=['POST'])
    def calculate_salary(self, request):
        year = int(request.data.get('year'))
        month = int(request.data.get('month'))

        employees = Employee.objects.filter(is_active=True)
        results = []

        for employee in employees:
            salary, created = SalaryCalculation.objects.get_or_create(
                employee=employee,
                year=year,
                month=month
            )

            salary.base_salary = employee.base_salary

            try:
                statistic = AttendanceStatistics.objects.get(
                    employee=employee,
                    year=year,
                    month=month
                )

                overtime_hours = statistic.overtime_hours
                hourly_rate = float(employee.base_salary) / 21.75 / 8
                salary.overtime_pay = round(float(overtime_hours) * hourly_rate * 1.5, 2)

                daily_rate = float(employee.base_salary) / 21.75
                salary.leave_deduction = round(float(statistic.leave_days) * daily_rate, 2)
                salary.late_deduction = round(statistic.late_times * 50, 2)
                salary.absent_deduction = round(statistic.absent_days * daily_rate * 2, 2)

            except AttendanceStatistics.DoesNotExist:
                pass

            salary.net_salary = (
                float(salary.base_salary)
                + float(salary.overtime_pay)
                + float(salary.bonus)
                - float(salary.leave_deduction)
                - float(salary.late_deduction)
                - float(salary.absent_deduction)
            )

            salary.save()
            results.append(salary)

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        queryset = self.queryset
        if year and month:
            queryset = queryset.filter(year=int(year), month=int(month))
        
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExportViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def attendance_records(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        department_id = request.query_params.get('department_id')
        employee_id = request.query_params.get('employee_id')
        is_exception = request.query_params.get('is_exception')

        queryset = AttendanceRecord.objects.select_related('employee', 'employee__department').all()
        if start_date:
            queryset = queryset.filter(attendance_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(attendance_date__lte=end_date)
        if department_id:
            queryset = queryset.filter(employee__department_id=department_id)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if is_exception and is_exception.lower() == 'true':
            queryset = queryset.filter(is_exception=True)

        data = []
        for record in queryset:
            data.append({
                '考勤编号': record.attendance_no,
                '员工编号': record.employee.emp_id,
                '员工姓名': record.employee.name,
                '部门': record.employee.department.name,
                '考勤日期': record.attendance_date.strftime('%Y-%m-%d'),
                '签到时间': record.check_in.strftime('%H:%M:%S') if record.check_in else '',
                '签退时间': record.check_out.strftime('%H:%M:%S') if record.check_out else '',
                '考勤状态': record.get_status_display(),
                '工作时长': float(record.work_hours),
                '迟到分钟': record.late_minutes,
                '早退分钟': record.early_leave_minutes,
                '是否异常': '是' if record.is_exception else '否',
                '异常类型': record.get_exception_type_display() if record.is_exception else '',
                '异常描述': record.exception_desc,
                '备注': record.remark
            })

        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='考勤记录')

        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=attendance_records_{date.today()}.xlsx'
        return response

    @action(detail=False, methods=['get'])
    def salary_report(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        department_id = request.query_params.get('department_id')

        queryset = SalaryCalculation.objects.select_related('employee', 'employee__department').all()
        if year:
            queryset = queryset.filter(year=int(year))
        if month:
            queryset = queryset.filter(month=int(month))
        if department_id:
            queryset = queryset.filter(employee__department_id=department_id)

        data = []
        for salary in queryset:
            total_deduction = float(salary.leave_deduction) + float(salary.late_deduction) + float(salary.absent_deduction)
            data.append({
                '薪资编号': salary.salary_no,
                '员工编号': salary.employee.emp_id,
                '员工姓名': salary.employee.name,
                '部门': salary.employee.department.name,
                '职位': salary.employee.position,
                '年份': salary.year,
                '月份': salary.month,
                '基本工资': float(salary.base_salary),
                '加班费': float(salary.overtime_pay),
                '请假扣款': float(salary.leave_deduction),
                '迟到扣款': float(salary.late_deduction),
                '旷工扣款': float(salary.absent_deduction),
                '总扣款': total_deduction,
                '奖金': float(salary.bonus),
                '实发工资': float(salary.net_salary),
                '备注': salary.remark
            })

        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='薪资报表')

        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=salary_report_{date.today()}.xlsx'
        return response

    @action(detail=False, methods=['get'])
    def attendance_statistics(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        department_id = request.query_params.get('department_id')

        queryset = AttendanceStatistics.objects.select_related('employee', 'employee__department').all()
        if year:
            queryset = queryset.filter(year=int(year))
        if month:
            queryset = queryset.filter(month=int(month))
        if department_id:
            queryset = queryset.filter(employee__department_id=department_id)

        data = []
        for stat in queryset:
            attendance_rate = (stat.actual_days / stat.work_days * 100) if stat.work_days > 0 else 0
            data.append({
                '统计编号': stat.statistic_no,
                '员工编号': stat.employee.emp_id,
                '员工姓名': stat.employee.name,
                '部门': stat.employee.department.name,
                '年份': stat.year,
                '月份': stat.month,
                '应出勤天数': stat.work_days,
                '实际出勤天数': stat.actual_days,
                '出勤率': f'{attendance_rate:.1f}%',
                '迟到次数': stat.late_times,
                '早退次数': stat.early_leave_times,
                '旷工天数': stat.absent_days,
                '请假天数': float(stat.leave_days),
                '加班总时长': float(stat.overtime_hours),
                '总工作时长': float(stat.total_work_hours)
            })

        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='考勤统计')

        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=attendance_statistics_{date.today()}.xlsx'
        return response

    def _save_archive_file(self, archive_type, year, month, department, output, record_count, archived_by, remark=''):
        year_str = str(year) if year else 'all'
        month_str = f'{month:02d}' if month else 'all'
        dept_str = department.name if department else 'all'
        
        file_name = f'{archive_type}_{year_str}_{month_str}_{dept_str}_{date.today().strftime("%Y%m%d%H%M%S")}.xlsx'
        relative_path = f'archives/{year_str}/{month_str}/{file_name}'
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(output.getvalue())
        
        file_size = os.path.getsize(full_path)
        
        archive = ArchiveRecord.objects.create(
            archive_type=archive_type,
            year=year or 0,
            month=month or 0,
            department=department,
            file_name=file_name,
            file_path=relative_path,
            file_size=file_size,
            record_count=record_count,
            archived_by=archived_by,
            remark=remark
        )
        return archive

    @action(detail=False, methods=['POST'])
    def archive_attendance(self, request):
        year = request.data.get('year')
        month = request.data.get('month')
        department_id = request.data.get('department_id')
        archived_by = request.data.get('archived_by', 'System')
        remark = request.data.get('remark', '')
        
        department = Department.objects.get(id=department_id) if department_id else None
        
        queryset = AttendanceRecord.objects.select_related('employee', 'employee__department').all()
        if year:
            queryset = queryset.filter(attendance_date__year=int(year))
        if month:
            queryset = queryset.filter(attendance_date__month=int(month))
        if department:
            queryset = queryset.filter(employee__department=department)
        
        data = []
        for record in queryset:
            data.append({
                '考勤编号': record.attendance_no,
                '员工编号': record.employee.emp_id,
                '员工姓名': record.employee.name,
                '部门': record.employee.department.name,
                '考勤日期': record.attendance_date.strftime('%Y-%m-%d'),
                '签到时间': record.check_in.strftime('%H:%M:%S') if record.check_in else '',
                '签退时间': record.check_out.strftime('%H:%M:%S') if record.check_out else '',
                '考勤状态': record.get_status_display(),
                '工作时长': float(record.work_hours),
                '迟到分钟': record.late_minutes,
                '早退分钟': record.early_leave_minutes,
                '是否异常': '是' if record.is_exception else '否',
                '异常类型': record.get_exception_type_display() if record.is_exception else '',
                '异常描述': record.exception_desc,
                '备注': record.remark
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='考勤记录')
        
        output.seek(0)
        archive = self._save_archive_file('attendance', int(year) if year else None, int(month) if month else None, 
                                         department, output, len(data), archived_by, remark)
        
        return Response(ArchiveRecordSerializer(archive).data)

    @action(detail=False, methods=['get'])
    def archives(self, request):
        archive_type = request.query_params.get('archive_type')
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        
        queryset = ArchiveRecord.objects.all()
        if archive_type:
            queryset = queryset.filter(archive_type=archive_type)
        if year:
            queryset = queryset.filter(year=int(year))
        if month:
            queryset = queryset.filter(month=int(month))
        
        serializer = ArchiveRecordSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download_archive(self, request, pk=None):
        archive = ArchiveRecord.objects.get(pk=pk)
        file_path = os.path.join(settings.MEDIA_ROOT, str(archive.file_path))
        
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{archive.file_name}"'
            return response
        return Response({'error': '文件不存在'}, status=404)


class MonthlySummaryViewSet(viewsets.ModelViewSet):
    queryset = MonthlySummary.objects.select_related('department').all()
    serializer_class = MonthlySummarySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['department__name', 'summary_no']
    ordering_fields = ['year', 'month', 'total_employees']
    ordering = ['-year', '-month']

    @action(detail=False, methods=['POST'])
    def generate_summaries(self, request):
        year = int(request.data.get('year'))
        month = int(request.data.get('month'))
        
        departments = Department.objects.all()
        results = []
        
        for dept in departments:
            summary, created = MonthlySummary.objects.get_or_create(
                department=dept,
                year=year,
                month=month
            )
            
            employees = Employee.objects.filter(department=dept, is_active=True)
            summary.total_employees = employees.count()
            
            stats = AttendanceStatistics.objects.filter(
                employee__in=employees,
                year=year,
                month=month
            )
            
            total_actual = stats.aggregate(Sum('actual_days'))['actual_days__sum'] or 0
            total_work = stats.aggregate(Sum('work_days'))['work_days__sum'] or 0
            summary.avg_attendance_rate = round((total_actual / total_work * 100) if total_work > 0 else 0, 2)
            
            summary.total_late_times = stats.aggregate(Sum('late_times'))['late_times__sum'] or 0
            summary.total_early_leave_times = stats.aggregate(Sum('early_leave_times'))['early_leave_times__sum'] or 0
            summary.total_absent_days = stats.aggregate(Sum('absent_days'))['absent_days__sum'] or 0
            summary.total_leave_days = stats.aggregate(Sum('leave_days'))['leave_days__sum'] or 0
            summary.total_overtime_hours = stats.aggregate(Sum('overtime_hours'))['overtime_hours__sum'] or 0
            summary.total_compensatory_hours = 0
            
            exception_records = AttendanceRecord.objects.filter(
                employee__in=employees,
                attendance_date__year=year,
                attendance_date__month=month,
                is_exception=True
            ).values('employee').distinct()
            summary.exception_count = exception_records.count()
            
            summary.save()
            results.append(summary)
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def confirm(self, request, pk=None):
        summary = self.get_object()
        confirmed_by = request.data.get('confirmed_by', '')
        
        summary.status = 'confirmed'
        summary.confirmed_by = confirmed_by
        summary.confirmed_at = timezone.now()
        summary.save()
        
        serializer = self.get_serializer(summary)
        return Response(serializer.data)


class CompensatoryLeaveViewSet(viewsets.ModelViewSet):
    queryset = CompensatoryLeave.objects.select_related('employee', 'employee__department', 'source_overtime').all()
    serializer_class = CompensatoryLeaveSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['employee__name', 'employee__emp_id', 'cl_no']
    ordering_fields = ['valid_from', 'total_hours', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=False, methods=['get'])
    def employee_summary(self, request):
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response({'error': '员工ID不能为空'}, status=400)
        
        queryset = self.queryset.filter(employee_id=employee_id)
        available = queryset.filter(status='available', remaining_hours__gt=0)
        
        summary = {
            'total_hours': float(queryset.aggregate(Sum('total_hours'))['total_hours__sum'] or 0),
            'used_hours': float(queryset.aggregate(Sum('used_hours'))['used_hours__sum'] or 0),
            'remaining_hours': float(available.aggregate(Sum('remaining_hours'))['remaining_hours__sum'] or 0),
            'expiring_soon': available.filter(valid_to__lte=date.today() + timedelta(days=30)).count(),
        }
        return Response(summary)


class LeaveBalanceViewSet(viewsets.ModelViewSet):
    queryset = LeaveBalance.objects.select_related('employee', 'employee__department').all()
    serializer_class = LeaveBalanceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['employee__name', 'employee__emp_id', 'lb_no']
    ordering_fields = ['year']
    ordering = ['-year']

    @action(detail=False, methods=['get'])
    def employee_balance(self, request):
        employee_id = request.query_params.get('employee_id')
        year = request.query_params.get('year', date.today().year)
        
        if not employee_id:
            return Response({'error': '员工ID不能为空'}, status=400)
        
        balance, created = self.queryset.get_or_create(
            employee_id=employee_id,
            year=int(year),
            defaults={'annual_leave_total': 10, 'sick_leave_total': 12, 'personal_leave_total': 6}
        )
        
        serializer = self.get_serializer(balance)
        return Response(serializer.data)


class ApprovalLogViewSet(viewsets.ModelViewSet):
    queryset = ApprovalLog.objects.all()
    serializer_class = ApprovalLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['related_type', 'operator', 'log_no']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        related_type = self.request.query_params.get('related_type')
        if related_type:
            queryset = queryset.filter(related_type=related_type)
        return queryset
