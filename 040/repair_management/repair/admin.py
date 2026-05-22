from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Customer, Device, RepairOrder, Notification, ArchivedOrder


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户资料'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        return obj.profile.get_role_display()
    get_role.short_description = '角色'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('created_at',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'device_type', 'brand', 'model', 'created_at')
    search_fields = ('brand', 'model', 'serial_number', 'customer__name')
    list_filter = ('device_type', 'created_at')


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'device', 'status', 'assigned_to', 'created_at', 'completed_at')
    search_fields = ('order_number', 'customer__name', 'device__brand', 'device__model')
    list_filter = ('status', 'created_at', 'completed_at', 'assigned_to')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'completed_at', 'picked_up_at', 'archived_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('order_number', 'customer', 'device', 'fault_description', 'status')
        }),
        ('分配与费用', {
            'fields': ('assigned_to', 'estimated_cost', 'actual_cost')
        }),
        ('维修详情', {
            'fields': ('diagnosis_result', 'repair_solution', 'parts_used', 'remarks')
        }),
        ('时间记录', {
            'fields': ('created_by', 'created_at', 'updated_at', 'completed_at', 'picked_up_at', 'archived_at')
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('notification_type', 'is_read', 'created_at')


@admin.register(ArchivedOrder)
class ArchivedOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_phone', 'device_info', 'picked_up_at', 'created_at')
    search_fields = ('order_number', 'customer_name', 'device_info')
    list_filter = ('created_at', 'picked_up_at')
    readonly_fields = ('original_order_id', 'order_number', 'customer_name', 'customer_phone', 'device_info', 
                       'fault_description', 'repair_solution', 'actual_cost', 'picked_up_at', 'archived_by', 'created_at')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
