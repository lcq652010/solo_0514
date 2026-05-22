from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product, Member, PurchaseOrder, PurchaseItem, SalesOrder, SalesItem, StockLog, PointsLog, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('角色信息', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('角色信息', {'fields': ('role', 'phone')}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('product_id', 'name', 'barcode')
    ordering = ('-created_at',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'name', 'phone', 'points', 'total_amount', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('member_id', 'name', 'phone')
    ordering = ('-created_at',)


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'supplier', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_no', 'supplier')
    ordering = ('-created_at',)
    inlines = [PurchaseItemInline]


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 0


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'member', 'total_amount', 'pay_amount', 'status', 'cashier', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_no', 'cashier')
    ordering = ('-created_at',)
    inlines = [SalesItemInline]


@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'type', 'quantity', 'stock_before', 'stock_after', 'related_order', 'created_at')
    list_filter = ('type',)
    search_fields = ('product__name', 'related_order')
    ordering = ('-created_at',)


@admin.register(PointsLog)
class PointsLogAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'points', 'points_before', 'points_after', 'related_order', 'created_at')
    list_filter = ('type',)
    search_fields = ('member__name', 'related_order')
    ordering = ('-created_at',)
