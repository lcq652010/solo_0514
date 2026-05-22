from django.contrib import admin
from .models import (
    Exhibition,
    Booth,
    Company,
    Booking,
    ConstructionDemand,
    ProgressTracker,
    Payment,
    Builder,
    ConstructionConfirm,
    ProgressStepTemplate,
    ProgressStep,
)


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'location', 'created_at']
    search_fields = ['name', 'location']
    list_filter = ['start_date', 'end_date']


@admin.register(Builder)
class BuilderAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'specialty', 'company_level', 'is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'phone']
    list_filter = ['specialty', 'is_active', 'company_level']
    list_editable = ['is_active', 'company_level']


@admin.register(ProgressStepTemplate)
class ProgressStepTemplateAdmin(admin.ModelAdmin):
    list_display = ['step_type', 'step_order', 'step_name', 'progress_percent', 'is_required']
    search_fields = ['step_name']
    list_filter = ['step_type', 'is_required']
    list_editable = ['step_order', 'progress_percent', 'is_required']


@admin.register(ProgressStep)
class ProgressStepAdmin(admin.ModelAdmin):
    list_display = ['construction', 'step_order', 'step_name', 'status', 'progress_percent', 'reported_at']
    search_fields = ['step_name', 'report_content']
    list_filter = ['status', 'construction']


@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ['exhibition', 'zone', 'booth_number', 'booth_type', 'area', 'price', 'status']
    search_fields = ['booth_number']
    list_filter = ['exhibition', 'zone', 'booth_type', 'status']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'industry', 'created_at']
    search_fields = ['name', 'contact_person', 'phone']
    list_filter = ['industry']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'company', 'booth', 'total_amount', 'status', 'booking_date']
    search_fields = ['order_number']
    list_filter = ['status', 'booking_date', 'booth__zone']
    readonly_fields = ['order_number', 'deposit_amount', 'balance_amount', 'total_amount']


@admin.register(ConstructionConfirm)
class ConstructionConfirmAdmin(admin.ModelAdmin):
    list_display = ['confirm_number', 'construction', 'plan_version', 'confirm_status', 'confirmed_at', 'created_at']
    search_fields = ['confirm_number', 'company_remark']
    list_filter = ['confirm_status', 'plan_version']
    readonly_fields = ['confirm_number']


@admin.register(ConstructionDemand)
class ConstructionDemandAdmin(admin.ModelAdmin):
    list_display = ['booking', 'builder', 'status', 'expected_complete_date', 'created_at', 'updated_at']
    search_fields = ['booking__order_number']
    list_filter = ['status', 'builder']


@admin.register(ProgressTracker)
class ProgressTrackerAdmin(admin.ModelAdmin):
    list_display = ['construction', 'stage_name', 'progress_percent', 'completed_at', 'created_at']
    search_fields = ['stage_name']
    list_filter = ['progress_percent']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'payment_type', 'amount', 'payment_method', 'payment_date']
    search_fields = ['booking__order_number', 'transaction_no']
    list_filter = ['payment_type', 'payment_method', 'payment_date']
