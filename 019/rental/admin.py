from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Customer, Order


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'brand', 'model', 'car_type', 'color', 'seats', 'daily_rent', 'overtime_rate', 'status']
    list_filter = ['status', 'brand', 'car_type']
    search_fields = ['plate_number', 'brand', 'model', 'car_type']
    list_per_page = 20
    list_editable = ['status']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'phone', 'id_card', 'driver_license', 'created_at']
    list_filter = ['gender']
    search_fields = ['name', 'phone', 'id_card', 'driver_license']
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_no', 'car_info', 'customer_info', 'start_date', 'end_date',
        'rental_days', 'total_amount', 'actual_amount', 'overtime_fee',
        'status_display', 'overdue_badge'
    ]
    list_filter = ['status', 'start_date', 'end_date']
    search_fields = ['order_no', 'customer__name', 'car__plate_number']
    readonly_fields = ['order_no', 'actual_start_date', 'actual_end_date', 'actual_amount', 'overtime_fee']
    list_per_page = 20
    actions = ['pick_up_car', 'return_car', 'cancel_order']

    def car_info(self, obj):
        return f"{obj.car.brand} {obj.car.model} ({obj.car.plate_number})"
    car_info.short_description = '车辆'

    def customer_info(self, obj):
        return f"{obj.customer.name} ({obj.customer.phone})"
    customer_info.short_description = '客户'

    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'picked_up': 'blue',
            'returned': 'green',
            'cancelled': 'gray',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = '状态'

    def overdue_badge(self, obj):
        if obj.status == 'picked_up' and obj.is_overdue:
            return format_html(
                '<span style="color: red; font-weight: bold; background: #ffebee; padding: 2px 6px; border-radius: 4px;">'
                '超时 {} 天</span>',
                obj.overdue_days
            )
        return '-'
    overdue_badge.short_description = '超时标记'

    def pick_up_car(self, request, queryset):
        count = 0
        for order in queryset:
            if order.pick_up_car():
                count += 1
        self.message_user(request, f"成功为 {count} 个订单执行取车操作")
    pick_up_car.short_description = "批量取车"

    def return_car(self, request, queryset):
        count = 0
        for order in queryset:
            if order.return_car():
                count += 1
        self.message_user(request, f"成功为 {count} 个订单执行还车操作，已自动结算费用")
    return_car.short_description = "批量还车（自动结算）"

    def cancel_order(self, request, queryset):
        count = 0
        for order in queryset:
            if order.cancel_order():
                count += 1
        self.message_user(request, f"成功取消 {count} 个订单")
    cancel_order.short_description = "批量取消订单"
