from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Department, Position, Employee, Attendance, Leave, Overtime, Salary, Payslip
from .serializers import (
    DepartmentSerializer, PositionSerializer, EmployeeSerializer,
    AttendanceSerializer, LeaveSerializer, OvertimeSerializer,
    SalarySerializer, PayslipSerializer
)
from .pagination import CustomPagination


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('-created_at')
    serializer_class = DepartmentSerializer
    pagination_class = CustomPagination


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.select_related('department').all().order_by('-created_at')
    serializer_class = PositionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department_id=department)
        return queryset


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department', 'position').all().order_by('-created_at')
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department')
        position = self.request.query_params.get('position')
        status = self.request.query_params.get('status')
        keyword = self.request.query_params.get('keyword')
        gender = self.request.query_params.get('gender')

        if department:
            queryset = queryset.filter(department_id=department)
        if position:
            queryset = queryset.filter(position_id=position)
        if status:
            queryset = queryset.filter(status=status)
        if gender:
            queryset = queryset.filter(gender=gender)
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | 
                Q(employee_id__icontains=keyword) |
                Q(phone__icontains=keyword) |
                Q(email__icontains=keyword)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        required_fields = ['name', 'gender', 'phone', 'email', 'id_card', 'department', 'position', 'hire_date', 'base_salary']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'code': 400, 'message': f'{field} 不能为空', 'data': None},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if len(data.get('phone', '')) != 11:
            return Response(
                {'code': 400, 'message': '手机号格式不正确', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(data.get('id_card', '')) != 18:
            return Response(
                {'code': 400, 'message': '身份证号格式不正确', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if Employee.objects.filter(phone=data.get('phone')).exists():
            return Response(
                {'code': 400, 'message': '手机号已存在', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if Employee.objects.filter(id_card=data.get('id_card')).exists():
            return Response(
                {'code': 400, 'message': '身份证号已存在', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {'code': 200, 'message': '创建成功', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee', 'employee__department').all().order_by('-date', '-created_at')
    serializer_class = AttendanceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_name = self.request.query_params.get('employee_name')
        department = self.request.query_params.get('department')
        attendance_status = self.request.query_params.get('status')
        date = self.request.query_params.get('date')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        employee_id = self.request.query_params.get('employee_id')

        if employee_id:
            queryset = queryset.filter(employee__employee_id=employee_id)
        if employee_name:
            queryset = queryset.filter(employee__name__icontains=employee_name)
        if department:
            queryset = queryset.filter(employee__department_id=department)
        if attendance_status:
            queryset = queryset.filter(status=attendance_status)
        if date:
            queryset = queryset.filter(date=date)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        required_fields = ['employee', 'date']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'code': 400, 'message': f'{field} 不能为空', 'data': None},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if data.get('check_in') and data.get('check_out'):
            check_in = datetime.fromisoformat(data.get('check_in').replace('Z', '+00:00'))
            check_out = datetime.fromisoformat(data.get('check_out').replace('Z', '+00:00'))
            if check_out <= check_in:
                return Response(
                    {'code': 400, 'message': '签退时间必须晚于签到时间', 'data': None},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if Attendance.objects.filter(employee_id=data.get('employee'), date=data.get('date')).exists():
            return Response(
                {'code': 400, 'message': '该员工当日考勤记录已存在', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {'code': 200, 'message': '创建成功', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        
        if data.get('check_in') and data.get('check_out'):
            check_in = datetime.fromisoformat(str(data.get('check_in')).replace('Z', '+00:00'))
            check_out = datetime.fromisoformat(str(data.get('check_out')).replace('Z', '+00:00'))
            if check_out <= check_in:
                return Response(
                    {'code': 400, 'message': '签退时间必须晚于签到时间', 'data': None},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {'code': 200, 'message': '更新成功', 'data': serializer.data}
        )

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response(
                {'code': 400, 'message': '员工ID不能为空', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {'code': 404, 'message': '员工不存在', 'data': None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if employee.status != 'active':
            return Response(
                {'code': 400, 'message': '该员工已离职，无法打卡', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        now = datetime.now()
        today = now.date()
        
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today
        )
        
        if attendance.check_in:
            time_diff = now - attendance.check_in.replace(tzinfo=None)
            if time_diff.total_seconds() < 60:
                return Response(
                    {'code': 429, 'message': '操作过于频繁，请稍后再试', 'data': None},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            return Response(
                {'code': 400, 'message': '今日已签到', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendance.check_in = now
        attendance.save()
        
        serializer = self.get_serializer(attendance)
        return Response(
            {'code': 200, 'message': '签到成功', 'data': serializer.data}
        )

    @action(detail=False, methods=['post'])
    def check_out(self, request):
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response(
                {'code': 400, 'message': '员工ID不能为空', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {'code': 404, 'message': '员工不存在', 'data': None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if employee.status != 'active':
            return Response(
                {'code': 400, 'message': '该员工已离职，无法打卡', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        now = datetime.now()
        today = now.date()
        
        try:
            attendance = Attendance.objects.get(employee=employee, date=today)
        except Attendance.DoesNotExist:
            return Response(
                {'code': 400, 'message': '请先签到', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not attendance.check_in:
            return Response(
                {'code': 400, 'message': '请先签到', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if attendance.check_out:
            time_diff = now - attendance.check_out.replace(tzinfo=None)
            if time_diff.total_seconds() < 60:
                return Response(
                    {'code': 429, 'message': '操作过于频繁，请稍后再试', 'data': None},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            return Response(
                {'code': 400, 'message': '今日已签退', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendance.check_out = now
        attendance.save()
        
        serializer = self.get_serializer(attendance)
        return Response(
            {'code': 200, 'message': '签退成功', 'data': serializer.data}
        )


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.select_related('employee', 'approver', 'employee__department').all().order_by('-created_at')
    serializer_class = LeaveSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_name = self.request.query_params.get('employee_name')
        department = self.request.query_params.get('department')
        status = self.request.query_params.get('status')
        leave_type = self.request.query_params.get('leave_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if employee_name:
            queryset = queryset.filter(employee__name__icontains=employee_name)
        if department:
            queryset = queryset.filter(employee__department_id=department)
        if status:
            queryset = queryset.filter(status=status)
        if leave_type:
            queryset = queryset.filter(leave_type=leave_type)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        required_fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'code': 400, 'message': f'{field} 不能为空', 'data': None},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        if end_date < start_date:
            return Response(
                {'code': 400, 'message': '结束日期不能早于开始日期', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        overlapping = Leave.objects.filter(
            employee_id=data.get('employee'),
            status__in=['pending', 'approved'],
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists()
        if overlapping:
            return Response(
                {'code': 400, 'message': '该时间段已有请假申请', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {'code': 200, 'message': '申请成功', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        approver_id = request.data.get('approver_id')
        remark = request.data.get('remark', '')

        if not approver_id:
            return Response(
                {'code': 400, 'message': '审批人ID不能为空', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if leave.status != 'pending':
            return Response(
                {'code': 400, 'message': '该请假申请已被处理，当前状态为{}'.format(leave.get_status_display()), 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            approver = Employee.objects.get(employee_id=approver_id)
        except Employee.DoesNotExist:
            return Response(
                {'code': 404, 'message': '审批人不存在', 'data': None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if approver.id == leave.employee.id:
            return Response(
                {'code': 400, 'message': '不能审批自己的请假申请', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        overlapping = Leave.objects.filter(
            employee=leave.employee,
            status='approved',
            start_date__lte=leave.end_date,
            end_date__gte=leave.start_date
        ).exclude(id=leave.id).exists()
        if overlapping:
            return Response(
                {'code': 400, 'message': '该时间段已有通过的请假申请，无法重复审批', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave.status = 'approved'
        leave.approver = approver
        leave.approval_remark = remark
        leave.save()
        
        serializer = self.get_serializer(leave)
        return Response(
            {'code': 200, 'message': '审批通过', 'data': serializer.data}
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        approver_id = request.data.get('approver_id')
        remark = request.data.get('remark', '')

        if not approver_id:
            return Response(
                {'code': 400, 'message': '审批人ID不能为空', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if leave.status != 'pending':
            return Response(
                {'code': 400, 'message': '该请假申请已被处理，当前状态为{}'.format(leave.get_status_display()), 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            approver = Employee.objects.get(employee_id=approver_id)
        except Employee.DoesNotExist:
            return Response(
                {'code': 404, 'message': '审批人不存在', 'data': None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if approver.id == leave.employee.id:
            return Response(
                {'code': 400, 'message': '不能拒绝自己的请假申请', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave.status = 'rejected'
        leave.approver = approver
        leave.approval_remark = remark
        leave.save()
        
        serializer = self.get_serializer(leave)
        return Response(
            {'code': 200, 'message': '已拒绝', 'data': serializer.data}
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        leave = self.get_object()
        
        if leave.status == 'approved':
            return Response(
                {'code': 400, 'message': '已通过的请假申请无法撤销', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if leave.status == 'rejected':
            return Response(
                {'code': 400, 'message': '已拒绝的请假申请无法撤销', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave.status = 'cancelled'
        leave.save()
        
        serializer = self.get_serializer(leave)
        return Response(
            {'code': 200, 'message': '撤销成功', 'data': serializer.data}
        )


class OvertimeViewSet(viewsets.ModelViewSet):
    queryset = Overtime.objects.select_related('employee', 'approver', 'employee__department').all().order_by('-created_at')
    serializer_class = OvertimeSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_name = self.request.query_params.get('employee_name')
        department = self.request.query_params.get('department')
        status = self.request.query_params.get('status')
        overtime_type = self.request.query_params.get('overtime_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if employee_name:
            queryset = queryset.filter(employee__name__icontains=employee_name)
        if department:
            queryset = queryset.filter(employee__department_id=department)
        if status:
            queryset = queryset.filter(status=status)
        if overtime_type:
            queryset = queryset.filter(overtime_type=overtime_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        required_fields = ['employee', 'overtime_type', 'date', 'start_time', 'end_time', 'reason']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'code': 400, 'message': f'{field} 不能为空', 'data': None},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        start_time = datetime.strptime(data.get('start_time'), '%H:%M').time()
        end_time = datetime.strptime(data.get('end_time'), '%H:%M').time()
        if end_time <= start_time:
            return Response(
                {'code': 400, 'message': '结束时间必须晚于开始时间', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        overlapping = Overtime.objects.filter(
            employee_id=data.get('employee'),
            status__in=['pending', 'approved'],
            date=data.get('date')
        ).exists()
        if overlapping:
            return Response(
                {'code': 400, 'message': '该日期已有加班申请', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {'code': 200, 'message': '申请成功', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        overtime = self.get_object()
        approver_id = request.data.get('approver_id')
        remark = request.data.get('remark', '')

        if not approver_id:
            return Response(
                {'code': 400, 'message': '审批人ID不能为空', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if overtime.status != 'pending':
            return Response(
                {'code': 400, 'message': '该加班申请已被处理，当前状态为{}'.format(overtime.get_status_display()), 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            approver = Employee.objects.get(employee_id=approver_id)
        except Employee.DoesNotExist:
            return Response(
                {'code': 404, 'message': '审批人不存在', 'data': None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if approver.id == overtime.employee.id:
            return Response(
                {'code': 400, 'message': '不能审批自己的加班申请', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        overtime.status = 'approved'
        overtime.approver = approver
        overtime.approval_remark = remark
        overtime.save()
        
        serializer = self.get_serializer(overtime)
        return Response(
            {'code': 200, 'message': '审批通过', 'data': serializer.data}
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        overtime = self.get_object()
        approver_id = request.data.get('approver_id')
        remark = request.data.get('remark', '')

        if not approver_id:
            return Response(
                {'code': 400, 'message': '审批人ID不能为空', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if overtime.status != 'pending':
            return Response(
                {'code': 400, 'message': '该加班申请已被处理，当前状态为{}'.format(overtime.get_status_display()), 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            approver = Employee.objects.get(employee_id=approver_id)
        except Employee.DoesNotExist:
            return Response(
                {'code': 404, 'message': '审批人不存在', 'data': None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if approver.id == overtime.employee.id:
            return Response(
                {'code': 400, 'message': '不能拒绝自己的加班申请', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        overtime.status = 'rejected'
        overtime.approver = approver
        overtime.approval_remark = remark
        overtime.save()
        
        serializer = self.get_serializer(overtime)
        return Response(
            {'code': 200, 'message': '已拒绝', 'data': serializer.data}
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        overtime = self.get_object()
        
        if overtime.status == 'approved':
            return Response(
                {'code': 400, 'message': '已通过的加班申请无法撤销', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if overtime.status == 'rejected':
            return Response(
                {'code': 400, 'message': '已拒绝的加班申请无法撤销', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        overtime.status = 'cancelled'
        overtime.save()
        
        serializer = self.get_serializer(overtime)
        return Response(
            {'code': 200, 'message': '撤销成功', 'data': serializer.data}
        )


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.select_related('employee', 'employee__department').all().order_by('-year', '-month', '-created_at')
    serializer_class = SalarySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_name = self.request.query_params.get('employee_name')
        department = self.request.query_params.get('department')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')

        if employee_name:
            queryset = queryset.filter(employee__name__icontains=employee_name)
        if department:
            queryset = queryset.filter(employee__department_id=department)
        if year:
            queryset = queryset.filter(year=year)
        if month:
            queryset = queryset.filter(month=month)
        return queryset

    @action(detail=False, methods=['post'])
    def batch_generate(self, request):
        year = request.data.get('year')
        month = request.data.get('month')

        if not year or not month:
            return Response(
                {'code': 400, 'message': '年份和月份不能为空', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            year = int(year)
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError()
        except (ValueError, TypeError):
            return Response(
                {'code': 400, 'message': '年份或月份格式不正确', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        employees = Employee.objects.filter(status='active')
        created_count = 0
        updated_count = 0

        for employee in employees:
            salary, created = Salary.objects.update_or_create(
                employee=employee,
                year=year,
                month=month,
                defaults={'base_salary': employee.base_salary}
            )
            salary.calculate_salary()
            salary.save()
            
            Payslip.objects.get_or_create(salary=salary)
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        return Response({
            'code': 200,
            'message': f'成功生成{created_count}条薪资记录，更新{updated_count}条薪资记录',
            'data': {'created': created_count, 'updated': updated_count}
        })


class PayslipViewSet(viewsets.ModelViewSet):
    queryset = Payslip.objects.select_related('salary', 'salary__employee', 'salary__employee__department').all().order_by('-created_at')
    serializer_class = PayslipSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_name = self.request.query_params.get('employee_name')
        department = self.request.query_params.get('department')
        issued = self.request.query_params.get('issued')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')

        if employee_name:
            queryset = queryset.filter(salary__employee__name__icontains=employee_name)
        if department:
            queryset = queryset.filter(salary__employee__department_id=department)
        if issued is not None:
            queryset = queryset.filter(issued=issued.lower() == 'true')
        if year:
            queryset = queryset.filter(salary__year=year)
        if month:
            queryset = queryset.filter(salary__month=month)
        return queryset

    @action(detail=True, methods=['post'])
    def issue(self, request, pk=None):
        payslip = self.get_object()
        
        if payslip.issued:
            return Response(
                {'code': 400, 'message': '该工资条已发放', 'data': None},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payslip.issued = True
        payslip.issued_at = datetime.now()
        payslip.save()
        
        serializer = self.get_serializer(payslip)
        return Response(
            {'code': 200, 'message': '发放成功', 'data': serializer.data}
        )


@api_view(['GET'])
def dashboard_stats(request):
    employee_count = Employee.objects.filter(status='active').count()
    today = datetime.now().date()
    
    attendance_today = Attendance.objects.filter(date=today)
    checked_in_count = attendance_today.filter(check_in__isnull=False).count()
    absent_count = attendance_today.filter(status='absent').count()
    late_count = attendance_today.filter(status='late').count()
    early_leave_count = attendance_today.filter(status='early_leave').count()
    
    pending_leave = Leave.objects.filter(status='pending').count()
    pending_overtime = Overtime.objects.filter(status='pending').count()
    
    department_stats = []
    for dept in Department.objects.all():
        dept_employees = Employee.objects.filter(department=dept, status='active')
        dept_attendance = attendance_today.filter(employee__department=dept)
        department_stats.append({
            'department_id': dept.id,
            'department_name': dept.name,
            'employee_count': dept_employees.count(),
            'checked_in_count': dept_attendance.filter(check_in__isnull=False).count(),
        })
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'employee_count': employee_count,
            'checked_in_count': checked_in_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'early_leave_count': early_leave_count,
            'pending_leave': pending_leave,
            'pending_overtime': pending_overtime,
            'department_stats': department_stats,
        }
    })


@api_view(['GET'])
def attendance_statistics(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    department = request.query_params.get('department')
    employee_id = request.query_params.get('employee_id')

    if not start_date or not end_date:
        return Response(
            {'code': 400, 'message': '开始日期和结束日期不能为空', 'data': None},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {'code': 400, 'message': '日期格式不正确，请使用 YYYY-MM-DD 格式', 'data': None},
            status=status.HTTP_400_BAD_REQUEST
        )

    if end_date_obj < start_date_obj:
        return Response(
            {'code': 400, 'message': '结束日期不能早于开始日期', 'data': None},
            status=status.HTTP_400_BAD_REQUEST
        )

    attendances = Attendance.objects.filter(date__range=[start_date_obj, end_date_obj])
    
    if department:
        attendances = attendances.filter(employee__department_id=department)
    if employee_id:
        attendances = attendances.filter(employee__employee_id=employee_id)

    total_days = (end_date_obj - start_date_obj).days + 1
    normal_count = attendances.filter(status='normal').count()
    late_count = attendances.filter(status='late').count()
    early_leave_count = attendances.filter(status='early_leave').count()
    absent_count = attendances.filter(status='absent').count()

    employee_stats = []
    employees = Employee.objects.filter(status='active')
    if department:
        employees = employees.filter(department_id=department)
    if employee_id:
        employees = employees.filter(employee_id=employee_id)

    for emp in employees:
        emp_attendances = attendances.filter(employee=emp)
        emp_normal = emp_attendances.filter(status='normal').count()
        emp_late = emp_attendances.filter(status='late').count()
        emp_early_leave = emp_attendances.filter(status='early_leave').count()
        emp_absent = emp_attendances.filter(status='absent').count()
        emp_work_days = emp_attendances.filter(status__in=['normal', 'late', 'early_leave']).count()
        attendance_rate = round(emp_work_days / total_days * 100, 2) if total_days > 0 else 0

        employee_stats.append({
            'employee_id': emp.employee_id,
            'employee_name': emp.name,
            'department_id': emp.department.id if emp.department else None,
            'department_name': emp.department.name if emp.department else None,
            'normal_count': emp_normal,
            'late_count': emp_late,
            'early_leave_count': emp_early_leave,
            'absent_count': emp_absent,
            'work_days': emp_work_days,
            'attendance_rate': attendance_rate,
        })

    department_stats = []
    departments = Department.objects.all()
    if department:
        departments = departments.filter(id=department)

    for dept in departments:
        dept_employees = Employee.objects.filter(department=dept, status='active')
        dept_employee_ids = dept_employees.values_list('id', flat=True)
        dept_attendances = attendances.filter(employee_id__in=dept_employee_ids)
        
        dept_normal = dept_attendances.filter(status='normal').count()
        dept_late = dept_attendances.filter(status='late').count()
        dept_early_leave = dept_attendances.filter(status='early_leave').count()
        dept_absent = dept_attendances.filter(status='absent').count()
        dept_work_days = dept_attendances.filter(status__in=['normal', 'late', 'early_leave']).count()
        dept_total_days = dept_employees.count() * total_days
        dept_attendance_rate = round(dept_work_days / dept_total_days * 100, 2) if dept_total_days > 0 else 0

        department_stats.append({
            'department_id': dept.id,
            'department_name': dept.name,
            'employee_count': dept_employees.count(),
            'normal_count': dept_normal,
            'late_count': dept_late,
            'early_leave_count': dept_early_leave,
            'absent_count': dept_absent,
            'work_days': dept_work_days,
            'attendance_rate': dept_attendance_rate,
        })

    total_attendance_rate = round((normal_count + late_count + early_leave_count) / (Employee.objects.filter(status='active').count() * total_days) * 100, 2) if total_days > 0 else 0

    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'start_date': start_date,
            'end_date': end_date,
            'total_days': total_days,
            'summary': {
                'normal_count': normal_count,
                'late_count': late_count,
                'early_leave_count': early_leave_count,
                'absent_count': absent_count,
                'attendance_rate': total_attendance_rate,
            },
            'employee_stats': employee_stats,
            'department_stats': department_stats,
        }
    })


@api_view(['GET'])
def salary_statistics(request):
    year = request.query_params.get('year')
    month = request.query_params.get('month')
    department = request.query_params.get('department')

    if not year or not month:
        return Response(
            {'code': 400, 'message': '年份和月份不能为空', 'data': None},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return Response(
            {'code': 400, 'message': '年份或月份格式不正确', 'data': None},
            status=status.HTTP_400_BAD_REQUEST
        )

    salaries = Salary.objects.filter(year=year, month=month)
    
    if department:
        salaries = salaries.filter(employee__department_id=department)

    total_base_salary = sum(float(s.base_salary) for s in salaries)
    total_overtime_pay = sum(float(s.overtime_pay) for s in salaries)
    total_bonus = sum(float(s.bonus) for s in salaries)
    total_deduction = sum(float(s.deduction) for s in salaries)
    total_net_salary = sum(float(s.net_salary) for s in salaries)

    department_stats = []
    departments = Department.objects.all()
    if department:
        departments = departments.filter(id=department)

    for dept in departments:
        dept_salaries = salaries.filter(employee__department=dept)
        dept_total_base = sum(float(s.base_salary) for s in dept_salaries)
        dept_total_overtime = sum(float(s.overtime_pay) for s in dept_salaries)
        dept_total_bonus = sum(float(s.bonus) for s in dept_salaries)
        dept_total_deduction = sum(float(s.deduction) for s in dept_salaries)
        dept_total_net = sum(float(s.net_salary) for s in dept_salaries)

        department_stats.append({
            'department_id': dept.id,
            'department_name': dept.name,
            'employee_count': dept_salaries.count(),
            'total_base_salary': round(dept_total_base, 2),
            'total_overtime_pay': round(dept_total_overtime, 2),
            'total_bonus': round(dept_total_bonus, 2),
            'total_deduction': round(dept_total_deduction, 2),
            'total_net_salary': round(dept_total_net, 2),
            'avg_net_salary': round(dept_total_net / dept_salaries.count(), 2) if dept_salaries.count() > 0 else 0,
        })

    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'year': year,
            'month': month,
            'employee_count': salaries.count(),
            'summary': {
                'total_base_salary': round(total_base_salary, 2),
                'total_overtime_pay': round(total_overtime_pay, 2),
                'total_bonus': round(total_bonus, 2),
                'total_deduction': round(total_deduction, 2),
                'total_net_salary': round(total_net_salary, 2),
                'avg_net_salary': round(total_net_salary / salaries.count(), 2) if salaries.count() > 0 else 0,
            },
            'department_stats': department_stats,
        }
    })