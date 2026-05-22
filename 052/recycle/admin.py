from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Item, Order, OrderItem, QualityCheck, Settlement, UserProfile, UserRole


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户资料'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'get_role', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'profile__role']
    search_fields = ['username', 'email']

    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else '无角色'
    get_role.short_description = '角色'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['subtotal']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'estimated_price', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['created_by']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'customer_name', 'customer_phone', 'address', 'status', 'total_amount', 'pickup_time', 'created_by', 'recycler', 'created_at']
    list_filter = ['status', 'created_at', 'pickup_time']
    search_fields = ['order_no', 'customer_name', 'customer_phone', 'address']
    inlines = [OrderItemInline]
    readonly_fields = ['order_no', 'total_amount', 'created_at', 'updated_at', 'picked_up_at', 'warehoused_at', 'completed_at']
    raw_id_fields = ['created_by', 'recycler']
    list_select_related = ['created_by', 'recycler']


@admin.register(QualityCheck)
class QualityCheckAdmin(admin.ModelAdmin):
    list_display = ['order', 'checker', 'result', 'actual_amount', 'check_time']
    list_filter = ['result', 'check_time']
    search_fields = ['order__order_no', 'checker']
    readonly_fields = ['check_time', 'created_at']
    raw_id_fields = ['order']


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ['order', 'settle_amount', 'operator', 'settle_time']
    list_filter = ['settle_time']
    search_fields = ['order__order_no', 'operator']
    readonly_fields = ['settle_time']
    raw_id_fields = ['order']
