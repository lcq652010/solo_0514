from django.contrib import admin
from .models import Book, Reader, Borrow


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['isbn', 'title', 'author', 'publisher', 'category', 'status', 'available_copies', 'create_time']
    list_filter = ['status', 'category']
    search_fields = ['isbn', 'title', 'author']
    readonly_fields = ['create_time', 'update_time']


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['reader_no', 'name', 'gender', 'phone', 'reader_type', 'is_active', 'register_date']
    list_filter = ['reader_type', 'gender', 'is_active']
    search_fields = ['reader_no', 'name', 'phone', 'id_card']
    readonly_fields = ['reader_no', 'register_date', 'create_time', 'update_time']


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['borrow_no', 'book', 'reader', 'borrow_date', 'due_date', 'return_date', 'status', 'fine_amount']
    list_filter = ['status']
    search_fields = ['borrow_no', 'book__title', 'reader__name', 'reader__reader_no']
    readonly_fields = ['borrow_no', 'borrow_date', 'create_time', 'update_time']
