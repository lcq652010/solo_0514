from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Service, Aunt, Order, Review, OrderArchive, AuntStatistics


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar')}),
        ('权限', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'phone', 'address', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('name', 'phone')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Aunt)
class AuntAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'age', 'phone', 'status', 'rating', 'total_orders', 'experience')
    list_filter = ('gender', 'status', 'created_at')
    search_fields = ('name', 'phone', 'id_card')
    filter_horizontal = ('skills',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'customer_name', 'customer_phone', 'service', 'aunt', 'status', 'total_price', 'service_date')
    list_filter = ('status', 'service_date', 'created_at')
    search_fields = ('order_no', 'customer_name', 'customer_phone')
    readonly_fields = ('order_no', 'created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'aunt', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('order__order_no', 'aunt__name', 'content')


@admin.register(OrderArchive)
class OrderArchiveAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'customer_name', 'aunt_name', 'service_name', 'total_price', 'rating', 'archived_at')
    list_filter = ('archived_at', 'rating')
    search_fields = ('order_no', 'customer_name', 'aunt_name', 'service_name')
    readonly_fields = ('order_no', 'created_at', 'completed_at', 'archived_at')


@admin.register(AuntStatistics)
class AuntStatisticsAdmin(admin.ModelAdmin):
    list_display = ('aunt', 'total_orders', 'completed_orders', 'total_amount', 'avg_rating', 'good_reviews')
    search_fields = ('aunt__name',)
    readonly_fields = ('updated_at',)

