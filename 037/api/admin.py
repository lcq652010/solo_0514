from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Category, Product, Order, OrderItem, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('角色信息', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('角色信息', {'fields': ('role', 'phone')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['category', 'is_available']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'sugar', 'ice', 'toppings']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'customer_name', 'total_amount', 'status', 'is_paid', 'take_code', 
                    'is_notified', 'is_archived', 'created_at']
    list_filter = ['status', 'is_paid', 'is_notified', 'is_archived', 'created_at']
    search_fields = ['order_no', 'customer_name', 'customer_phone', 'take_code']
    readonly_fields = ['order_no', 'take_code', 'total_amount', 'paid_at', 'notified_at', 
                      'archived_at', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
