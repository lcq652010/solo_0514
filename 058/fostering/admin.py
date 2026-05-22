from django.contrib import admin
from django.utils import timezone
from .models import Pet, Room, Order, FeedingRecord


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'size_display', 'breed', 'age', 'weight', 'owner_name', 
                    'owner_phone', 'vaccine_expiry', 'is_vaccine_valid_display', 'created_at']
    list_filter = ['species', 'size', 'breed']
    search_fields = ['name', 'breed', 'owner_name', 'owner_phone']
    readonly_fields = ['created_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'species', 'size', 'breed', 'age', 'weight')
        }),
        ('主人信息', {
            'fields': ('owner_name', 'owner_phone')
        }),
        ('健康信息', {
            'fields': ('vaccine_expiry', 'health_status', 'special_requirements')
        }),
        ('系统信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def size_display(self, obj):
        return obj.get_size_display()
    size_display.short_description = '体型'
    
    def is_vaccine_valid_display(self, obj):
        if obj.is_vaccine_valid():
            return '✓ 有效'
        days = obj.days_until_vaccine_expiry()
        if days is None:
            return '✗ 未设置'
        return f'✗ 已过期{abs(days)}天'
    is_vaccine_valid_display.short_description = '疫苗状态'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type_display', 'suitable_size_display', 
                    'daily_price', 'overtime_multiplier', 'status', 
                    'current_pets', 'max_pets', 'available_capacity_display']
    list_filter = ['room_type', 'suitable_size', 'status']
    search_fields = ['room_number', 'description']
    fieldsets = (
        ('基本信息', {
            'fields': ('room_number', 'room_type', 'suitable_size', 'description')
        }),
        ('容量信息', {
            'fields': ('max_pets', 'current_pets')
        }),
        ('费用信息', {
            'fields': ('daily_price', 'overtime_multiplier')
        }),
        ('状态', {
            'fields': ('status',)
        }),
    )
    
    def room_type_display(self, obj):
        return obj.get_room_type_display()
    room_type_display.short_description = '房间类型'
    
    def suitable_size_display(self, obj):
        return obj.get_suitable_size_display()
    suitable_size_display.short_description = '适用体型'
    
    def available_capacity_display(self, obj):
        return obj.available_capacity()
    available_capacity_display.short_description = '可用容量'


class FeedingRecordInline(admin.TabularInline):
    model = FeedingRecord
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'pet', 'room', 'checkin_date', 'expected_checkout_date', 
                    'checkout_date', 'expected_days', 'actual_days', 'overtime_days',
                    'status_display', 'base_amount', 'overtime_amount', 'total_amount', 
                    'reminder_status_display', 'days_until_checkout_display']
    list_filter = ['status', 'reminder_status', 'room__room_type', 'pet__species', 'pet__size']
    search_fields = ['order_no', 'pet__name', 'pet__owner_name']
    readonly_fields = ['order_no', 'created_at', 'updated_at', 'actual_days', 
                      'overtime_days', 'base_amount', 'overtime_amount', 'total_amount', 'checkout_date']
    inlines = [FeedingRecordInline]
    actions = ['checkin_selected', 'checkout_selected', 'complete_selected', 'cancel_selected',
              'mark_reminder_sent', 'auto_assign_room_selected']
    fieldsets = (
        ('基本信息', {
            'fields': ('order_no', 'pet', 'room', 'status', 'reminder_status', 'reminder_sent_at')
        }),
        ('时间信息', {
            'fields': ('checkin_date', 'expected_checkout_date', 'checkout_date')
        }),
        ('寄养天数', {
            'fields': ('expected_days', 'actual_days', 'overtime_days')
        }),
        ('费用信息', {
            'fields': ('daily_price', 'base_amount', 'overtime_amount', 'total_amount')
        }),
        ('备注', {
            'fields': ('notes',)
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = '订单状态'
    
    def reminder_status_display(self, obj):
        return obj.get_reminder_status_display()
    reminder_status_display.short_description = '提醒状态'
    
    def days_until_checkout_display(self, obj):
        days = obj.get_days_until_checkout()
        if days is not None:
            if days <= 0:
                return '已到期'
            return f'{days}天'
        return '-'
    days_until_checkout_display.short_description = '距离到期'
    
    def stay_duration_display(self, obj):
        days = obj.get_stay_duration_days()
        if days is not None:
            return f'{days}天'
        return '-'
    stay_duration_display.short_description = '实际寄养时长'
    
    def checkin_selected(self, request, queryset):
        count = 0
        for order in queryset.filter(status='pending_checkin'):
            try:
                order.checkin()
                count += 1
            except Exception as e:
                self.message_user(request, f'订单{order.order_no}入住失败: {str(e)}')
        self.message_user(request, f'成功办理{count}个订单入住')
    checkin_selected.short_description = '批量办理入住'
    
    def checkout_selected(self, request, queryset):
        count = 0
        for order in queryset.filter(status='in_care'):
            try:
                order.checkout()
                count += 1
            except Exception as e:
                self.message_user(request, f'订单{order.order_no}离店失败: {str(e)}')
        self.message_user(request, f'成功办理{count}个订单离店结算')
    checkout_selected.short_description = '批量办理离店结算'
    
    def complete_selected(self, request, queryset):
        count = 0
        for order in queryset.filter(status='pending_pickup'):
            try:
                order.complete()
                count += 1
            except Exception as e:
                self.message_user(request, f'订单{order.order_no}完成失败: {str(e)}')
        self.message_user(request, f'成功完成{count}个订单')
    complete_selected.short_description = '批量完成订单'
    
    def cancel_selected(self, request, queryset):
        count = 0
        for order in queryset.filter(status__in=['pending_checkin', 'pending_pickup']):
            try:
                order.cancel()
                count += 1
            except Exception as e:
                self.message_user(request, f'订单{order.order_no}取消失败: {str(e)}')
        self.message_user(request, f'成功取消{count}个订单')
    cancel_selected.short_description = '批量取消订单'
    
    def mark_reminder_sent(self, request, queryset):
        count = 0
        for order in queryset.filter(status='in_care'):
            order.mark_reminder_sent()
            count += 1
        self.message_user(request, f'成功标记{count}个订单提醒已发送')
    mark_reminder_sent.short_description = '批量标记提醒已发送'
    
    def auto_assign_room_selected(self, request, queryset):
        success_count = 0
        fail_count = 0
        for order in queryset.filter(status='pending_checkin', room__isnull=True):
            success, message = order.auto_assign_room()
            if success:
                success_count += 1
            else:
                fail_count += 1
        self.message_user(request, f'自动分配房间完成: 成功{success_count}个, 失败{fail_count}个')
    auto_assign_room_selected.short_description = '批量自动分配房间'


@admin.register(FeedingRecord)
class FeedingRecordAdmin(admin.ModelAdmin):
    list_display = ['order', 'record_date', 'morning_feeding', 
                    'afternoon_feeding', 'evening_feeding', 'created_by']
    list_filter = ['record_date', 'morning_feeding', 'afternoon_feeding', 'evening_feeding']
    search_fields = ['order__order_no', 'created_by', 'health_notes']
    readonly_fields = ['created_at']
    fieldsets = (
        ('关联订单', {
            'fields': ('order', 'record_date')
        }),
        ('喂食记录', {
            'fields': (('morning_feeding', 'morning_notes'),
                      ('afternoon_feeding', 'afternoon_notes'),
                      ('evening_feeding', 'evening_notes'))
        }),
        ('健康备注', {
            'fields': ('health_notes',)
        }),
        ('记录信息', {
            'fields': ('created_by', 'created_at')
        }),
    )
