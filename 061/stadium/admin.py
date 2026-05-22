from django.contrib import admin
from .models import VenueType, Venue, Booking, TimeSlot, Payment


@admin.register(VenueType)
class VenueTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sport_type', 'description']
    list_filter = ['sport_type']
    search_fields = ['name']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'venue_type', 'size', 'price_per_hour', 'min_billing_minutes', 
                    'max_booking_hours_per_day', 'status', 'capacity', 'area']
    list_filter = ['status', 'venue_type', 'size']
    search_fields = ['name', 'code']
    list_editable = ['status', 'price_per_hour', 'min_billing_minutes', 'max_booking_hours_per_day', 'size']
    fieldsets = [
        ('基本信息', {'fields': ['name', 'code', 'venue_type', 'size', 'status']}),
        ('容量配置', {'fields': ['capacity', 'area']}),
        ('计费配置', {'fields': ['price_per_hour', 'min_billing_minutes', 'max_booking_hours_per_day']}),
        ('其他', {'fields': ['qr_code', 'description']}),
    ]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_no', 'user', 'venue', 'booking_type', 'people_count', 'start_time', 'end_time', 
                    'actual_duration_minutes_display', 'total_amount', 'status', 'verification_status', 'contact_name']
    list_filter = ['status', 'venue', 'verification_status', 'booking_type']
    search_fields = ['booking_no', 'contact_name', 'contact_phone', 'id_card']
    readonly_fields = ['booking_no', 'created_at', 'updated_at', 'verification_time', 
                      'actual_start_time', 'actual_end_time', 'actual_duration_minutes', 'billing_duration_minutes']
    date_hierarchy = 'start_time'

    fieldsets = [
        ('预约信息', {'fields': ['booking_no', 'user', 'venue', 'booking_type', 'people_count']}),
        ('时间信息', {'fields': ['start_time', 'end_time', 'actual_start_time', 'actual_end_time', 
                                'actual_duration_minutes', 'billing_duration_minutes']}),
        ('状态信息', {'fields': ['status', 'total_amount', 'check_in_method', 'check_out_method']}),
        ('联系人信息', {'fields': ['contact_name', 'contact_phone', 'id_card', 'verification_status', 'verification_time']}),
        ('备注', {'fields': ['remarks']}),
    ]

    actions = ['mark_as_checked_in', 'mark_as_checked_out', 'mark_as_verified']

    def actual_duration_minutes_display(self, obj):
        if obj.actual_duration_minutes:
            hours = obj.actual_duration_minutes // 60
            minutes = obj.actual_duration_minutes % 60
            if hours > 0:
                return f'{hours}小时{minutes}分钟'
            return f'{minutes}分钟'
        return '-'
    actual_duration_minutes_display.short_description = '实际使用时长'

    def mark_as_checked_in(self, request, queryset):
        for booking in queryset:
            booking.check_in()
    mark_as_checked_in.short_description = '批量入场'

    def mark_as_checked_out(self, request, queryset):
        for booking in queryset:
            booking.check_out()
    mark_as_checked_out.short_description = '批量离场'

    def mark_as_verified(self, request, queryset):
        from django.utils import timezone
        for booking in queryset:
            booking.verification_status = 'verified'
            booking.verification_time = timezone.now()
            booking.save()
    mark_as_verified.short_description = '批量核验通过'


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'venue', 'date', 'start_time', 'end_time', 'price', 'is_available']
    list_filter = ['is_available', 'venue', 'date']
    search_fields = ['venue__name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_no', 'booking', 'amount', 'payment_method', 'status', 'paid_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['payment_no', 'transaction_id']
    readonly_fields = ['payment_no', 'created_at']
    date_hierarchy = 'paid_at'
