from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseOrderItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['supplier_code', 'name', 'contact_person', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['supplier_code', 'name']


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'supplier', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_no']
    inlines = [PurchaseOrderItemInline]
