from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Sum
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta
from .models import (
    Student, Coach, Vehicle, CoachSchedule, TrainingAppointment, 
    TrainingRecord, FeeSettlement, SubjectHourConfig, StudentSubjectStats
)
from .serializers import (
    StudentSerializer, CoachSerializer, VehicleSerializer,
    CoachScheduleSerializer, TrainingAppointmentSerializer,
    TrainingRecordSerializer, FeeSettlementSerializer,
    SubjectHourConfigSerializer, StudentSubjectStatsSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = StudentSerializer
    filterset_fields = ['status', 'gender', 'license_type']
    search_fields = ['name', 'id_card', 'phone']


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all().order_by('-created_at')
    serializer_class = CoachSerializer
    filterset_fields = ['status', 'gender', 'teach_type']
    search_fields = ['name', 'id_card', 'phone', 'license_number']


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('-created_at')
    serializer_class = VehicleSerializer
    filterset_fields = ['status', 'vehicle_type']
    search_fields = ['plate_number', 'brand', 'vehicle_type']


class SubjectHourConfigViewSet(viewsets.ModelViewSet):
    queryset = SubjectHourConfig.objects.all().order_by('-created_at')
    serializer_class = SubjectHourConfigSerializer
    filterset_fields = ['is_active']
    search_fields = ['subject_name']


class StudentSubjectStatsViewSet(viewsets.ModelViewSet):
    queryset = StudentSubjectStats.objects.all().order_by('-updated_at')
    serializer_class = StudentSubjectStatsSerializer
    filterset_fields = ['student', 'subject_name', 'can_schedule_exam', 'exam_passed']
    search_fields = ['student__name', 'subject_name']
    
    @action(detail=True, methods=['post'])
    def set_required_hours(self, request, pk=None):
        stats = self.get_object()
        required_hours = float(request.data.get('required_hours', 0))
        if required_hours <= 0:
            return Response({'error': '要求学时必须大于0'}, status=status.HTTP_400_BAD_REQUEST)
        
        stats.required_hours = required_hours
        if stats.total_effective_hours >= required_hours:
            stats.can_schedule_exam = True
        stats.save()
        return Response({'status': '设置成功', 'required_hours': required_hours})
    
    @action(detail=True, methods=['post'])
    def mark_exam_passed(self, request, pk=None):
        stats = self.get_object()
        stats.exam_passed = True
        stats.can_schedule_exam = False
        stats.save()
        return Response({'status': '已标记通过'})


class CoachScheduleViewSet(viewsets.ModelViewSet):
    queryset = CoachSchedule.objects.all().order_by('-schedule_date')
    serializer_class = CoachScheduleSerializer
    filterset_fields = ['coach', 'schedule_date', 'is_booked']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        available_schedules = self.queryset.filter(is_booked=False, schedule_date__gte=timezone.now().date())
        serializer = self.get_serializer(available_schedules, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def filter_schedules(self, request):
        coach_id = request.query_params.get('coach_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.queryset
        
        if coach_id:
            queryset = queryset.filter(coach_id=coach_id)
        if start_date:
            queryset = queryset.filter(schedule_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(schedule_date__lte=end_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def export_weekly(self, request):
        week_offset = int(request.query_params.get('week_offset', 0))
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)
        
        schedules = CoachSchedule.objects.filter(
            schedule_date__range=[start_of_week, end_of_week]
        ).order_by('coach', 'schedule_date', 'start_time')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="weekly_schedule_{start_of_week}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['教练', '日期', '开始时间', '结束时间', '是否已预约'])
        
        for schedule in schedules:
            writer.writerow([
                schedule.coach.name,
                schedule.schedule_date,
                schedule.start_time,
                schedule.end_time,
                '是' if schedule.is_booked else '否'
            ])
        
        return response
    
    @action(detail=False, methods=['get'])
    def export_monthly(self, request):
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        schedules = CoachSchedule.objects.filter(
            schedule_date__year=year,
            schedule_date__month=month
        ).order_by('coach', 'schedule_date', 'start_time')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="monthly_schedule_{year}_{month}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['教练', '日期', '开始时间', '结束时间', '是否已预约'])
        
        for schedule in schedules:
            writer.writerow([
                schedule.coach.name,
                schedule.schedule_date,
                schedule.start_time,
                schedule.end_time,
                '是' if schedule.is_booked else '否'
            ])
        
        return response


class TrainingAppointmentViewSet(viewsets.ModelViewSet):
    queryset = TrainingAppointment.objects.all().order_by('-created_at')
    serializer_class = TrainingAppointmentSerializer
    filterset_fields = ['student', 'coach', 'vehicle', 'status', 'appointment_date', 'training_subject']
    search_fields = ['appointment_number', 'student__name', 'coach__name', 'training_subject']
    
    def perform_create(self, serializer):
        appointment = serializer.save()
        schedule = appointment.schedule
        schedule.is_booked = True
        schedule.save()
    
    def perform_update(self, serializer):
        appointment = serializer.save()
        if appointment.status == 'cancelled':
            schedule = appointment.schedule
            schedule.is_booked = False
            schedule.save()
    
    @action(detail=False, methods=['get'])
    def filter_appointments(self, request):
        coach_id = request.query_params.get('coach_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        subject = request.query_params.get('subject')
        status_filter = request.query_params.get('status')
        
        queryset = self.queryset
        
        if coach_id:
            queryset = queryset.filter(coach_id=coach_id)
        if start_date:
            queryset = queryset.filter(appointment_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(appointment_date__lte=end_date)
        if subject:
            queryset = queryset.filter(training_subject=subject)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        return Response({'status': '预约已确认'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        schedule = appointment.schedule
        schedule.is_booked = False
        schedule.save()
        appointment.save()
        return Response({'status': '预约已取消'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()
        return Response({'status': '预约已完成'})


class TrainingRecordViewSet(viewsets.ModelViewSet):
    queryset = TrainingRecord.objects.all().order_by('-training_date')
    serializer_class = TrainingRecordSerializer
    filterset_fields = ['student', 'coach', 'vehicle', 'training_subject', 'training_date']
    search_fields = ['student__name', 'coach__name', 'training_subject']
    
    @action(detail=False, methods=['get'])
    def filter_records(self, request):
        coach_id = request.query_params.get('coach_id')
        student_id = request.query_params.get('student_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        subject = request.query_params.get('subject')
        
        queryset = self.queryset
        
        if coach_id:
            queryset = queryset.filter(coach_id=coach_id)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if start_date:
            queryset = queryset.filter(training_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(training_date__lte=end_date)
        if subject:
            queryset = queryset.filter(training_subject=subject)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def export_hours_weekly(self, request):
        week_offset = int(request.query_params.get('week_offset', 0))
        coach_id = request.query_params.get('coach_id')
        subject = request.query_params.get('subject')
        
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)
        
        records = TrainingRecord.objects.filter(
            training_date__range=[start_of_week, end_of_week],
            clock_out_time__isnull=False
        )
        
        if coach_id:
            records = records.filter(coach_id=coach_id)
        if subject:
            records = records.filter(training_subject=subject)
        
        records = records.order_by('training_date', 'coach')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="weekly_hours_{start_of_week}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['日期', '学员', '教练', '车辆', '科目', '实际学时', '有效学时', '超出学时'])
        
        for record in records:
            writer.writerow([
                record.training_date,
                record.student.name,
                record.coach.name,
                record.vehicle.plate_number,
                record.training_subject,
                record.training_hours,
                record.effective_hours,
                record.exceeded_hours
            ])
        
        return response
    
    @action(detail=False, methods=['get'])
    def export_hours_monthly(self, request):
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        coach_id = request.query_params.get('coach_id')
        subject = request.query_params.get('subject')
        
        records = TrainingRecord.objects.filter(
            training_date__year=year,
            training_date__month=month,
            clock_out_time__isnull=False
        )
        
        if coach_id:
            records = records.filter(coach_id=coach_id)
        if subject:
            records = records.filter(training_subject=subject)
        
        records = records.order_by('training_date', 'coach')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="monthly_hours_{year}_{month}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['日期', '学员', '教练', '车辆', '科目', '实际学时', '有效学时', '超出学时'])
        
        for record in records:
            writer.writerow([
                record.training_date,
                record.student.name,
                record.coach.name,
                record.vehicle.plate_number,
                record.training_subject,
                record.training_hours,
                record.effective_hours,
                record.exceeded_hours
            ])
        
        return response
    
    @action(detail=False, methods=['get'])
    def stats_summary(self, request):
        coach_id = request.query_params.get('coach_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        subject = request.query_params.get('subject')
        
        records = TrainingRecord.objects.filter(clock_out_time__isnull=False)
        
        if coach_id:
            records = records.filter(coach_id=coach_id)
        if start_date:
            records = records.filter(training_date__gte=start_date)
        if end_date:
            records = records.filter(training_date__lte=end_date)
        if subject:
            records = records.filter(training_subject=subject)
        
        summary = records.aggregate(
            total_training_hours=Sum('training_hours'),
            total_effective_hours=Sum('effective_hours'),
            total_exceeded_hours=Sum('exceeded_hours')
        )
        
        return Response({
            'total_training_hours': summary['total_training_hours'] or 0,
            'total_effective_hours': summary['total_effective_hours'] or 0,
            'total_exceeded_hours': summary['total_exceeded_hours'] or 0,
            'record_count': records.count()
        })
    
    @action(detail=True, methods=['post'])
    def clock_in(self, request, pk=None):
        record = self.get_object()
        if record.clock_in_time:
            return Response({'error': '已经打卡过了'}, status=status.HTTP_400_BAD_REQUEST)
        record.clock_in_time = timezone.now()
        record.save()
        return Response({'status': '打卡成功', 'clock_in_time': record.clock_in_time})
    
    @action(detail=True, methods=['post'])
    def clock_out(self, request, pk=None):
        record = self.get_object()
        if not record.clock_in_time:
            return Response({'error': '请先进行开始打卡'}, status=status.HTTP_400_BAD_REQUEST)
        if record.clock_out_time:
            return Response({'error': '已经结束打卡了'}, status=status.HTTP_400_BAD_REQUEST)
        record.clock_out_time = timezone.now()
        record.save()
        
        return Response({
            'status': '结束打卡成功',
            'clock_out_time': record.clock_out_time,
            'training_hours': record.training_hours,
            'effective_hours': record.effective_hours,
            'exceeded_hours': record.exceeded_hours
        })


class FeeSettlementViewSet(viewsets.ModelViewSet):
    queryset = FeeSettlement.objects.all().order_by('-created_at')
    serializer_class = FeeSettlementSerializer
    filterset_fields = ['student', 'payment_status', 'payment_method', 'payment_date']
    search_fields = ['settlement_number', 'student__name']
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        settlement = self.get_object()
        amount = float(request.data.get('amount', 0))
        payment_method = request.data.get('payment_method', 'cash')
        
        if amount <= 0:
            return Response({'error': '支付金额必须大于0'}, status=status.HTTP_400_BAD_REQUEST)
        
        settlement.paid_amount += amount
        settlement.payment_method = payment_method
        settlement.payment_date = timezone.now().date()
        settlement.save()
        
        return Response({
            'status': '支付成功',
            'paid_amount': float(settlement.paid_amount),
            'remaining_amount': float(settlement.remaining_amount),
            'payment_status': settlement.payment_status
        })
