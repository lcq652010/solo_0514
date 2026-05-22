from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Coach, Vehicle, Schedule, TrainingReservation, ExamRegistration, Payment, StudentArchive, UserProfile, TrainingHours, TrainingArchive


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户配置'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'coach', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username', 'phone']


@admin.register(TrainingHours)
class TrainingHoursAdmin(admin.ModelAdmin):
    list_display = ['student', 'coach', 'subject', 'date', 'duration', 'created_at']
    list_filter = ['subject', 'date', 'coach']
    search_fields = ['student__name', 'coach__name']


@admin.register(TrainingArchive)
class TrainingArchiveAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'total_hours', 'completed_hours', 'status', 'created_at']
    list_filter = ['status', 'subject']
    search_fields = ['student__name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'gender', 'license_type', 'enrollment_date', 'status']
    list_filter = ['status', 'license_type', 'gender']
    search_fields = ['name', 'student_id', 'id_card', 'phone']
    readonly_fields = ['student_id', 'created_at', 'updated_at']


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ['coach_id', 'name', 'gender', 'teach_type', 'experience', 'status']
    list_filter = ['status', 'teach_type', 'gender']
    search_fields = ['name', 'coach_id', 'id_card', 'phone']
    readonly_fields = ['coach_id', 'created_at', 'updated_at']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'vehicle_type', 'brand', 'status', 'coach']
    list_filter = ['status', 'license_type']
    search_fields = ['plate_number', 'vehicle_type', 'brand']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['coach', 'vehicle', 'date', 'start_time', 'end_time', 'current_students', 'max_students']
    list_filter = ['date']
    search_fields = ['coach__name', 'vehicle__plate_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TrainingReservation)
class TrainingReservationAdmin(admin.ModelAdmin):
    list_display = ['student', 'schedule', 'subject', 'status', 'reservation_time']
    list_filter = ['status', 'subject']
    search_fields = ['student__name', 'student__student_id']
    readonly_fields = ['reservation_time', 'created_at', 'updated_at']


@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_type', 'exam_date', 'exam_location', 'status', 'score']
    list_filter = ['status', 'exam_type']
    search_fields = ['student__name', 'student__student_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'payment_type', 'amount', 'payment_method', 'status', 'payment_time']
    list_filter = ['status', 'payment_type', 'payment_method']
    search_fields = ['student__name', 'student__student_id', 'transaction_no']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StudentArchive)
class StudentArchiveAdmin(admin.ModelAdmin):
    list_display = ['student', 'archive_no', 'archive_date', 'is_complete']
    list_filter = ['is_complete']
    search_fields = ['student__name', 'student__student_id', 'archive_no']
    readonly_fields = ['archive_no', 'created_at', 'updated_at']
