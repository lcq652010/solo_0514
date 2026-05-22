from django.contrib import admin
from .models import Package, Customer, Photographer, Appointment, Order, Settlement, PhotoSelection, UserProfile


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'days', 'photos_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'email', 'wechat', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'email', 'wechat')
    raw_id_fields = ('user',)


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'level', 'is_active', 'created_at')
    list_filter = ('is_active', 'level')
    search_fields = ('name', 'phone')
    raw_id_fields = ('user',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'package', 'photographer', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('customer__name', 'photographer__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'package', 'photographer', 'shoot_date', 'status', 'total_amount', 'is_settled')
    list_filter = ('status', 'shoot_date', 'is_settled')
    search_fields = ('order_number', 'customer__name', 'photographer__name')
    readonly_fields = ('order_number',)


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('order', 'balance_amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('order__order_number',)


@admin.register(PhotoSelection)
class PhotoSelectionAdmin(admin.ModelAdmin):
    list_display = ('order', 'selected_count', 'total_count', 'is_completed', 'selected_at')
    list_filter = ('is_completed', 'selected_at')
    search_fields = ('order__order_number',)
    readonly_fields = ('selected_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'phone')
    raw_id_fields = ('user',)
