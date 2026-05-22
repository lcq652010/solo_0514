from django.contrib import admin
from .models import Customer, WholesaleOrder, WholesaleOrderItem, Settlement


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_code', 'name', 'contact_person', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['customer_code', 'name']


class WholesaleOrderItemInline(admin.TabularInline):
    model = WholesaleOrderItem
    extra = 0


@admin.register(WholesaleOrder)
class WholesaleOrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'customer', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_no']
    inlines = [WholesaleOrderItemInline]


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ['settlement_no', 'wholesale_order', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['settlement_no']
