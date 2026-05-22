from django.contrib import admin
from .models import *


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'department', 'phone', 'created_at']
    list_filter = ['role', 'department']
    search_fields = ['name', 'phone']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'title', 'phone', 'created_at']
    list_filter = ['department']
    search_fields = ['name', 'title']


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'created_at']
    search_fields = ['name', 'phone']


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'gender', 'age', 'weight', 'owner', 'created_at']
    list_filter = ['gender', 'species']
    search_fields = ['name', 'species', 'owner__name']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'specification', 'price', 'stock', 'expiry_date', 'created_at']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['visit_no', 'pet', 'doctor', 'department', 'status', 'appointment_time', 'created_at']
    list_filter = ['status', 'department']
    search_fields = ['visit_no', 'pet__name', 'doctor__name']


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['visit', 'diagnosis', 'created_at']
    search_fields = ['visit__visit_no', 'diagnosis']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medical_record', 'medicine', 'quantity', 'dosage', 'subtotal', 'created_at']
    search_fields = ['medical_record__visit__visit_no', 'medicine__name']


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ['charge_no', 'visit', 'total_amount', 'status', 'payment_method', 'paid_at', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['charge_no', 'visit__visit_no']


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'operation', 'quantity', 'stock_before', 'stock_after', 'operator', 'created_at']
    list_filter = ['operation']
    search_fields = ['medicine__name']
