from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Student, Coach, Vehicle, Schedule, TrainingReservation, ExamRegistration, Payment, StudentArchive, UserProfile, TrainingHours, TrainingArchive
from .serializers import (
    StudentSerializer, CoachSerializer, VehicleSerializer, ScheduleSerializer,
    TrainingReservationSerializer, ExamRegistrationSerializer, PaymentSerializer, 
    StudentArchiveSerializer, UserProfileSerializer, TrainingHoursSerializer, TrainingArchiveSerializer
)
import re
from datetime import datetime


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsReception(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role in ['前台', '管理员']
        except UserProfile.DoesNotExist:
            return False


class IsCoach(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role in ['教练', '管理员']
        except UserProfile.DoesNotExist:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == '管理员'
        except UserProfile.DoesNotExist:
            return False


def get_user_role(user):
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role
    except UserProfile.DoesNotExist:
        return None


def get_coach_by_user(user):
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.coach
    except UserProfile.DoesNotExist:
        return None


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsReception]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        status_param = self.request.query_params.get('status', None)
        license_type = self.request.query_params.get('license_type', None)
        phone = self.request.query_params.get('phone', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        student_id = self.request.query_params.get('student_id', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if student_id:
            queryset = queryset.filter(student_id__icontains=student_id)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if license_type:
            queryset = queryset.filter(license_type=license_type)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if start_date:
            queryset = queryset.filter(enrollment_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(enrollment_date__lte=end_date)

        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        errors = {}

        name = data.get('name', '').strip()
        if not name:
            errors['name'] = '姓名不能为空'
        elif len(name) < 2 or len(name) > 20:
            errors['name'] = '姓名长度应在2-20个字符之间'

        id_card = data.get('id_card', '').strip()
        if not id_card:
            errors['id_card'] = '身份证号不能为空'
        elif not re.match(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
            errors['id_card'] = '身份证号格式不正确'
        elif Student.objects.filter(id_card=id_card).exists():
            errors['id_card'] = '该身份证号已被注册'

        phone = data.get('phone', '').strip()
        if not phone:
            errors['phone'] = '手机号不能为空'
        elif not re.match(r'^1[3-9]\d{9}$', phone):
            errors['phone'] = '手机号格式不正确'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        errors = {}

        if 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                errors['name'] = '姓名不能为空'
            elif len(name) < 2 or len(name) > 20:
                errors['name'] = '姓名长度应在2-20个字符之间'

        if 'id_card' in data:
            id_card = data.get('id_card', '').strip()
            if not re.match(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
                errors['id_card'] = '身份证号格式不正确'
            elif Student.objects.filter(id_card=id_card).exclude(pk=self.get_object().pk).exists():
                errors['id_card'] = '该身份证号已被注册'

        if 'phone' in data:
            phone = data.get('phone', '').strip()
            if not re.match(r'^1[3-9]\d{9}$', phone):
                errors['phone'] = '手机号格式不正确'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_param = request.query_params.get('status', None)
        if status_param:
            students = Student.objects.filter(status=status_param)
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供状态参数'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        student = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Student.STATUS_CHOICES):
            student.status = new_status
            student.save()
            return Response({'message': '状态更新成功', 'status': new_status})
        return Response({'error': '无效的状态'}, status=status.HTTP_400_BAD_REQUEST)


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        status_param = self.request.query_params.get('status', None)
        teach_type = self.request.query_params.get('teach_type', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if teach_type:
            queryset = queryset.filter(teach_type__icontains=teach_type)

        return queryset.order_by('coach_id')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        errors = {}

        name = data.get('name', '').strip()
        if not name:
            errors['name'] = '姓名不能为空'

        id_card = data.get('id_card', '').strip()
        if not id_card:
            errors['id_card'] = '身份证号不能为空'
        elif not re.match(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
            errors['id_card'] = '身份证号格式不正确'
        elif Coach.objects.filter(id_card=id_card).exists():
            errors['id_card'] = '该身份证号已被注册'

        phone = data.get('phone', '').strip()
        if not phone:
            errors['phone'] = '手机号不能为空'
        elif not re.match(r'^1[3-9]\d{9}$', phone):
            errors['phone'] = '手机号格式不正确'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def active(self, request):
        coaches = Coach.objects.filter(status='在职')
        serializer = self.get_serializer(coaches, many=True)
        return Response(serializer.data)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        plate_number = self.request.query_params.get('plate_number', None)
        status_param = self.request.query_params.get('status', None)
        vehicle_type = self.request.query_params.get('vehicle_type', None)

        if plate_number:
            queryset = queryset.filter(plate_number__icontains=plate_number)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if vehicle_type:
            queryset = queryset.filter(vehicle_type__icontains=vehicle_type)

        return queryset.order_by('plate_number')

    @action(detail=False, methods=['get'])
    def available(self, request):
        vehicles = Vehicle.objects.filter(status='可用')
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsReception]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        coach_name = self.request.query_params.get('coach_name', None)
        coach_id = self.request.query_params.get('coach_id', None)
        date = self.request.query_params.get('date', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        has_available = self.request.query_params.get('has_available', None)
        vehicle_plate = self.request.query_params.get('vehicle_plate', None)

        if coach_name:
            queryset = queryset.filter(coach__name__icontains=coach_name)
        if coach_id:
            queryset = queryset.filter(coach__coach_id__icontains=coach_id)
        if vehicle_plate:
            queryset = queryset.filter(vehicle__plate_number__icontains=vehicle_plate)
        if date:
            queryset = queryset.filter(date=date)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if has_available and has_available == 'true':
                queryset = queryset.filter(current_students__lt=models.F('max_students'))

        current_coach = get_coach_by_user(self.request.user)
        if current_coach:
            queryset = queryset.filter(coach=current_coach)

        return queryset.order_by('-date', 'start_time')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        errors = {}

        coach_id = data.get('coach')
        vehicle_id = data.get('vehicle')
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if not all([coach_id, vehicle_id, date, start_time, end_time]):
            return Response({'error': '请填写完整的排班信息'}, status=status.HTTP_400_BAD_REQUEST)

        if start_time >= end_time:
            errors['time'] = '结束时间必须晚于开始时间'

        existing_schedules = Schedule.objects.filter(
            coach_id=coach_id,
            date=date
        )

        for schedule in existing_schedules:
            if (start_time < schedule.end_time and end_time > schedule.start_time):
                errors['conflict'] = '该时段与已有排班冲突'
                break

        vehicle_schedules = Schedule.objects.filter(
            vehicle_id=vehicle_id,
            date=date
        )

        for schedule in vehicle_schedules:
            if (start_time < schedule.end_time and end_time > schedule.start_time):
                errors['vehicle_conflict'] = '该车辆在此时段已被分配'
                break

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date_param = request.query_params.get('date', None)
        if date_param:
            schedules = Schedule.objects.filter(date=date_param)
            serializer = self.get_serializer(schedules, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供日期参数'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def available(self, request):
        today = timezone.now().date()
        schedules = Schedule.objects.filter(date__gte=today, current_students__lt=models.F('max_students'))
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)


class TrainingReservationViewSet(viewsets.ModelViewSet):
    queryset = TrainingReservation.objects.all()
    serializer_class = TrainingReservationSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsReception]
        elif self.action in ['start_training', 'complete_training', 'sign_in']:
            permission_classes = [IsCoach]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.query_params.get('student_name', None)
        coach_name = self.request.query_params.get('coach_name', None)
        status_param = self.request.query_params.get('status', None)
        subject = self.request.query_params.get('subject', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        student_id = self.request.query_params.get('student_id', None)
        coach_id = self.request.query_params.get('coach_id', None)

        if student_name:
            queryset = queryset.filter(student__name__icontains=student_name)
        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        if coach_name:
            queryset = queryset.filter(schedule__coach__name__icontains=coach_name)
        if coach_id:
            queryset = queryset.filter(schedule__coach__coach_id__icontains=coach_id)
        if status_param:
            if ',' in status_param:
                status_list = status_param.split(',')
                queryset = queryset.filter(status__in=status_list)
            else:
                queryset = queryset.filter(status=status_param)
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        if start_date:
            queryset = queryset.filter(schedule__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(schedule__date__lte=end_date)

        current_coach = get_coach_by_user(self.request.user)
        if current_coach:
            queryset = queryset.filter(schedule__coach=current_coach)

        return queryset.order_by('-reservation_time')

    @action(detail=True, methods=['post'])
    def sign_in(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == '待培训':
            reservation.status = '培训中'
            reservation.actual_start_time = timezone.now()
            reservation.save()
            return Response({
                'message': '签到成功，培训已开始',
                'start_time': reservation.actual_start_time,
                'status': reservation.status
            })
        return Response({'error': '当前状态无法签到'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start_training(self, request, pk=None):
        return self.sign_in(request, pk)

    @action(detail=True, methods=['post'])
    def complete_training(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == '培训中':
            reservation.status = '已完成'
            reservation.actual_end_time = timezone.now()
            reservation.training_content = request.data.get('training_content', '')
            reservation.coach_comment = request.data.get('coach_comment', '')
            reservation.save()

            schedule = reservation.schedule
            start_datetime = datetime.combine(schedule.date, schedule.start_time)
            end_datetime = datetime.combine(schedule.date, schedule.end_time)
            duration = (end_datetime - start_datetime).total_seconds() / 3600

            TrainingHours.objects.create(
                student=reservation.student,
                coach=schedule.coach,
                vehicle=schedule.vehicle,
                subject=reservation.subject,
                date=schedule.date,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                duration=duration,
                remark=f'培训预约ID: {reservation.id}'
            )

            archive, created = TrainingArchive.objects.get_or_create(
                student=reservation.student,
                subject=reservation.subject,
                defaults={
                    'total_hours': 0,
                    'completed_hours': 0,
                }
            )
            archive.completed_hours += duration
            archive.save()

            return Response({
                'message': '培训已完成，课时已记录',
                'end_time': reservation.actual_end_time,
                'duration': duration,
                'status': reservation.status
            })
        return Response({'error': '当前状态无法完成培训'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        errors = {}

        student_id = data.get('student')
        schedule_id = data.get('schedule')
        subject = data.get('subject')

        if not all([student_id, schedule_id, subject]):
            return Response({'error': '请填写完整的预约信息'}, status=status.HTTP_400_BAD_REQUEST)

        schedule = Schedule.objects.filter(pk=schedule_id).first()
        if not schedule:
            errors['schedule'] = '排班不存在'
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if schedule.current_students >= schedule.max_students:
            errors['full'] = '该时段预约已满'

        existing_reservations = TrainingReservation.objects.filter(
            student_id=student_id,
            schedule__date=schedule.date,
            status__in=['待培训', '培训中']
        )

        for reservation in existing_reservations:
            if (schedule.start_time < reservation.schedule.end_time and
                schedule.end_time > reservation.schedule.start_time):
                errors['student_conflict'] = '您在此时段已有预约'
                break

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id', None)
        if student_id:
            reservations = TrainingReservation.objects.filter(student__student_id=student_id)
            serializer = self.get_serializer(reservations, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供学员学号'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_param = request.query_params.get('status', None)
        if status_param:
            reservations = TrainingReservation.objects.filter(status=status_param)
            serializer = self.get_serializer(reservations, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供状态参数'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start_training(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == '待培训':
            reservation.status = '培训中'
            reservation.actual_start_time = timezone.now()
            reservation.save()
            return Response({'message': '培训已开始'})
        return Response({'error': '当前状态无法开始培训'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def complete_training(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == '培训中':
            reservation.status = '已完成'
            reservation.actual_end_time = timezone.now()
            reservation.training_content = request.data.get('training_content', '')
            reservation.coach_comment = request.data.get('coach_comment', '')
            reservation.save()
            return Response({'message': '培训已完成'})
        return Response({'error': '当前状态无法完成培训'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status in ['待培训', '培训中']:
            reservation.status = '已取消'
            reservation.cancel_reason = request.data.get('cancel_reason', '')
            reservation.save()
            schedule = reservation.schedule
            schedule.current_students -= 1
            schedule.save()
            return Response({'message': '预约已取消'})
        return Response({'error': '当前状态无法取消'}, status=status.HTTP_400_BAD_REQUEST)


class ExamRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ExamRegistration.objects.all()
    serializer_class = ExamRegistrationSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.query_params.get('student_name', None)
        exam_type = self.request.query_params.get('exam_type', None)
        status_param = self.request.query_params.get('status', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if student_name:
            queryset = queryset.filter(student__name__icontains=student_name)
        if exam_type:
            queryset = queryset.filter(exam_type=exam_type)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if start_date:
            queryset = queryset.filter(exam_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(exam_date__lte=end_date)

        return queryset.order_by('-exam_date', '-exam_time')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        errors = {}

        student_id = data.get('student')
        exam_type = data.get('exam_type')
        exam_date = data.get('exam_date')
        exam_time = data.get('exam_time')
        exam_location = data.get('exam_location')

        if not all([student_id, exam_type, exam_date, exam_time, exam_location]):
            return Response({'error': '请填写完整的考试信息'}, status=status.HTTP_400_BAD_REQUEST)

        existing_exams = ExamRegistration.objects.filter(
            student_id=student_id,
            exam_type=exam_type,
            status__in=['待考试']
        )

        if existing_exams.exists():
            errors['exists'] = '该科目已有待考试的登记'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id', None)
        if student_id:
            exams = ExamRegistration.objects.filter(student__student_id=student_id)
            serializer = self.get_serializer(exams, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供学员学号'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_result(self, request, pk=None):
        exam = self.get_object()
        passed = request.data.get('passed', None)
        score = request.data.get('score', None)
        if passed is not None:
            exam.status = '已通过' if passed else '未通过'
            if score:
                exam.score = score
            exam.save()
            return Response({'message': '考试结果已更新'})
        return Response({'error': '请提供是否通过参数'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.query_params.get('student_name', None)
        payment_type = self.request.query_params.get('payment_type', None)
        payment_method = self.request.query_params.get('payment_method', None)
        status_param = self.request.query_params.get('status', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if student_name:
            queryset = queryset.filter(student__name__icontains=student_name)
        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        errors = {}

        student_id = data.get('student')
        payment_type = data.get('payment_type')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        operator = data.get('operator')

        if not all([student_id, payment_type, amount, payment_method, operator]):
            return Response({'error': '请填写完整的缴费信息'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount <= 0:
                errors['amount'] = '金额必须大于0'
        except (ValueError, TypeError):
            errors['amount'] = '金额格式不正确'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id', None)
        if student_id:
            payments = Payment.objects.filter(student__student_id=student_id)
            serializer = self.get_serializer(payments, many=True)
            return Response(serializer.data)
        return Response({'error': '请提供学员学号'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.status == '待支付':
            payment.status = '已支付'
            payment.payment_time = timezone.now()
            payment.transaction_no = request.data.get('transaction_no', '')
            payment.save()
            return Response({'message': '支付已确认'})
        return Response({'error': '当前状态无法确认支付'}, status=status.HTTP_400_BAD_REQUEST)


class StudentArchiveViewSet(viewsets.ModelViewSet):
    queryset = StudentArchive.objects.all()
    serializer_class = StudentArchiveSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.query_params.get('student_name', None)
        is_complete = self.request.query_params.get('is_complete', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if student_name:
            queryset = queryset.filter(student__name__icontains=student_name)
        if is_complete is not None:
            queryset = queryset.filter(is_complete=(is_complete == 'true'))
        if start_date:
            queryset = queryset.filter(archive_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(archive_date__lte=end_date)

        return queryset.order_by('-archive_date')

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id', None)
        if student_id:
            archive = StudentArchive.objects.filter(student__student_id=student_id).first()
            if archive:
                serializer = self.get_serializer(archive)
                return Response(serializer.data)
            return Response({'error': '未找到该学员档案'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': '请提供学员学号'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        archive = self.get_object()
        archive.is_complete = True
        archive.save()
        archive.student.status = '学习中'
        archive.student.save()
        return Response({'message': '档案已标记为完整'})


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        status_param = self.request.query_params.get('status', None)
        teach_type = self.request.query_params.get('teach_type', None)
        coach_id = self.request.query_params.get('coach_id', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if coach_id:
            queryset = queryset.filter(coach_id__icontains=coach_id)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if teach_type:
            queryset = queryset.filter(teach_type__icontains=teach_type)

        return queryset.order_by('coach_id')


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role', None)
        username = self.request.query_params.get('username', None)

        if role:
            queryset = queryset.filter(role=role)
        if username:
            queryset = queryset.filter(user__username__icontains=username)

        return queryset.order_by('-created_at')


class TrainingHoursViewSet(viewsets.ModelViewSet):
    queryset = TrainingHours.objects.all()
    serializer_class = TrainingHoursSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.query_params.get('student_name', None)
        coach_name = self.request.query_params.get('coach_name', None)
        subject = self.request.query_params.get('subject', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        student_id = self.request.query_params.get('student_id', None)

        if student_name:
            queryset = queryset.filter(student__name__icontains=student_name)
        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        if coach_name:
            queryset = queryset.filter(coach__name__icontains=coach_name)
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        current_coach = get_coach_by_user(self.request.user)
        if current_coach:
            queryset = queryset.filter(coach=current_coach)

        return queryset.order_by('-date', '-start_time')


class TrainingArchiveViewSet(viewsets.ModelViewSet):
    queryset = TrainingArchive.objects.all()
    serializer_class = TrainingArchiveSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.query_params.get('student_name', None)
        subject = self.request.query_params.get('subject', None)
        status_param = self.request.query_params.get('status', None)
        student_id = self.request.query_params.get('student_id', None)

        if student_name:
            queryset = queryset.filter(student__name__icontains=student_name)
        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        archive = self.get_object()
        if archive.status == '已完成':
            archive.status = '已归档'
            archive.archive_date = timezone.now().date()
            archive.save()
            return Response({'message': '档案已归档'})
        return Response({'error': '只有已完成的档案可以归档'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        archive = self.get_object()
        if archive.status == '进行中':
            archive.status = '已完成'
            archive.complete_date = timezone.now().date()
            archive.save()
            return Response({'message': '培训已标记完成'})
        return Response({'error': '当前状态无法标记完成'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': '用户配置不存在'}, status=status.HTTP_404_NOT_FOUND)


from django.db import models