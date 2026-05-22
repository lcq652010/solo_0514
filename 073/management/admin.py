from django.contrib import admin
from .models import (
    Student, Coach, Vehicle, CoachSchedule, TrainingAppointment, 
    TrainingRecord, FeeSettlement, SubjectHourConfig, StudentSubjectStats
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'id_card', 'phone', 'license_type', 'status', 'enrollment_date']
    search_fields = ['name', 'id_card', 'phone']
    list_filter = ['status', 'gender', 'license_type']


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'id_card', 'phone', 'teach_type', 'experience', 'status']
    search_fields = ['name', 'id_card', 'phone', 'license_number']
    list_filter = ['status', 'gender', 'teach_type']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'plate_number', 'vehicle_type', 'brand', 'status', 'current_coach']
    search_fields = ['plate_number', 'brand', 'vehicle_type']
    list_filter = ['status', 'vehicle_type']


@admin.register(CoachSchedule)
class CoachScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'coach', 'schedule_date', 'start_time', 'end_time', 'is_booked']
    search_fields = ['coach__name']
    list_filter = ['schedule_date', 'is_booked', 'coach']


@admin.register(TrainingAppointment)
class TrainingAppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment_number', 'student', 'coach', 'vehicle', 'appointment_date', 'status']
    search_fields = ['appointment_number', 'student__name', 'coach__name']
    list_filter = ['status', 'appointment_date', 'training_subject']


@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'coach', 'vehicle', 'training_date', 'training_hours', 
                    'effective_hours', 'exceeded_hours', 'training_subject']
    search_fields = ['student__name', 'coach__name', 'training_subject']
    list_filter = ['training_date', 'training_subject', 'coach']


@admin.register(FeeSettlement)
class FeeSettlementAdmin(admin.ModelAdmin):
    list_display = ['id', 'settlement_number', 'student', 'total_amount', 'paid_amount', 'remaining_amount', 'payment_status']
    search_fields = ['settlement_number', 'student__name']
    list_filter = ['payment_status', 'payment_method', 'payment_date']


@admin.register(SubjectHourConfig)
class SubjectHourConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_name', 'max_daily_hours', 'is_active']
    search_fields = ['subject_name']
    list_filter = ['is_active']


@admin.register(StudentSubjectStats)
class StudentSubjectStatsAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'subject_name', 'total_effective_hours', 'required_hours', 'can_schedule_exam']
    search_fields = ['student__name', 'subject_name']
    list_filter = ['can_schedule_exam', 'subject_name']
