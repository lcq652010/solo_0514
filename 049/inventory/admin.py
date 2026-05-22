from django.contrib import admin
from .models import Inventory, StockRecord, StockAlert


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'is_low_stock', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['product__name', 'product__product_code']


@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ['product', 'record_type', 'quantity', 'before_quantity', 'after_quantity', 'related_order_no', 'created_at']
    list_filter = ['record_type', 'created_at']
    search_fields = ['product__name', 'related_order_no']


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ['product', 'alert_type', 'current_quantity', 'min_stock', 'is_handled', 'created_at']
    list_filter = ['alert_type', 'is_handled', 'created_at']
    search_fields = ['product__name']
