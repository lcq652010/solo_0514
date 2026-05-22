from django.contrib import admin
from .models import Movie, Hall, Schedule, Seat, Order

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'duration', 'release_date', 'rating', 'is_showing']
    list_filter = ['is_showing', 'genre']
    search_fields = ['title', 'director', 'actors']

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_rows', 'total_cols', 'total_seats', 'is_3d', 'is_active']
    list_filter = ['is_3d', 'is_active']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['movie', 'hall', 'show_time', 'end_time', 'price', 'is_active']
    list_filter = ['is_active', 'hall']
    search_fields = ['movie__title']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['hall', 'schedule', 'seat_code', 'row_number', 'col_number', 'is_available']
    list_filter = ['is_available', 'hall']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'schedule', 'seat_codes', 'total_price', 'customer_name', 'customer_phone', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['order_no', 'customer_name', 'customer_phone']
    readonly_fields = ['order_no']
