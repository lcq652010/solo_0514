from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Room, Guest, Order, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户角色'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')

    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return '未设置'
    get_role.short_description = '角色'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'price', 'status', 'clean_status', 'floor', 'capacity']
    list_filter = ['room_type', 'status', 'clean_status', 'floor']
    search_fields = ['room_number']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'id_card', 'phone', 'gender', 'create_time']
    search_fields = ['name', 'id_card', 'phone']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'guest', 'room', 'status', 'check_in_date', 'check_out_date', 'total_amount', 'overtime_fee']
    list_filter = ['status']
    search_fields = ['order_number', 'guest__name', 'room__room_number']
    readonly_fields = ['order_number']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
