from django.contrib import admin
from .models import Institution, Device, Rental, Calibration, DamageRecord, MaintenanceRecord, ReturnAcceptance, Settlement


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'contact_phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'model', 'serial_number', 'device_type', 'use_department',
        'daily_rental_fee', 'status', 'get_calibration_status_display'
    ]
    list_filter = ['device_type', 'use_department', 'status', 'created_at']
    search_fields = ['name', 'model', 'serial_number', 'manufacturer']
    readonly_fields = ['created_at', 'updated_at', 'next_calibration_date']
    fieldsets = [
        ('基本信息', {'fields': ['name', 'device_type', 'use_department', 'model', 'serial_number', 'description']}),
        ('生产采购信息', {'fields': ['manufacturer', 'manufacture_date', 'purchase_date']}),
        ('租赁信息', {'fields': ['daily_rental_fee', 'status']}),
        ('校准信息', {'fields': ['calibration_cycle_days', 'last_calibration_date', 'next_calibration_date']}),
        ('系统信息', {'fields': ['created_at', 'updated_at']}),
    ]

    def get_calibration_status_display(self, obj):
        status = obj.get_calibration_status()
        status_map = {
            'normal': '正常',
            'warning': '提醒(30天内)',
            'urgent': '紧急(7天内)',
            'expired': '已过期',
        }
        return status_map.get(status, status)
    get_calibration_status_display.short_description = '校准状态'


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = [
        'rental_no', 'institution', 'device', 'start_date', 'end_date',
        'estimated_total', 'status', 'get_countdown_status_display'
    ]
    list_filter = ['status', 'created_at', 'start_date', 'end_date']
    search_fields = ['rental_no', 'contact_person', 'contact_phone']
    readonly_fields = ['rental_no', 'estimated_days', 'estimated_total', 'created_at', 'updated_at']

    def get_countdown_status_display(self, obj):
        status = obj.get_rental_countdown_status()
        status_map = {
            'normal': '正常',
            'warning': '提醒(3天内)',
            'urgent': '紧急(1天内)',
            'overdue': '已逾期',
        }
        return status_map.get(status, status)
    get_countdown_status_display.short_description = '租期状态'


@admin.register(Calibration)
class CalibrationAdmin(admin.ModelAdmin):
    list_display = ['device', 'calibration_date', 'calibrator', 'calibration_agency', 'status', 'next_calibration_date']
    list_filter = ['status', 'calibration_date', 'next_calibration_date']
    search_fields = ['calibrator', 'calibration_agency', 'certificate_no']
    readonly_fields = ['created_at']


@admin.register(ReturnAcceptance)
class ReturnAcceptanceAdmin(admin.ModelAdmin):
    list_display = ['rental', 'return_date', 'inspector', 'status', 'damage_fee']
    list_filter = ['status', 'return_date']
    search_fields = ['rental__rental_no', 'inspector']
    readonly_fields = ['created_at']


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ['rental', 'rental_days', 'total_amount', 'status', 'payment_method', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['rental__rental_no', 'invoice_no']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']


@admin.register(DamageRecord)
class DamageRecordAdmin(admin.ModelAdmin):
    list_display = ['device', 'rental', 'damage_type', 'damage_level', 'inspector', 'estimated_repair_cost', 'needs_maintenance', 'created_at']
    list_filter = ['damage_type', 'damage_level', 'needs_maintenance', 'created_at']
    search_fields = ['damage_description', 'inspector', 'device__name', 'rental__rental_no']
    readonly_fields = ['created_at']


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ['device', 'damage_record', 'maintenance_type', 'status', 'reporter', 'maintenance_person', 'start_date', 'complete_date', 'total_cost']
    list_filter = ['status', 'maintenance_type', 'start_date', 'complete_date']
    search_fields = ['maintenance_content', 'reporter', 'maintenance_person', 'device__name']
    readonly_fields = ['created_at', 'updated_at', 'report_date', 'total_cost']
