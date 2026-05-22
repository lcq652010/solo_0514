from rest_framework import serializers
from .models import *


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Staff
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class PetSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    owner_phone = serializers.CharField(source='owner.phone', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = Pet
        fields = '__all__'


class MedicineSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Medicine
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    owner_name = serializers.CharField(source='pet.owner.name', read_only=True)
    owner_phone = serializers.CharField(source='pet.owner.phone', read_only=True)
    
    class Meta:
        model = Visit
        fields = '__all__'
        read_only_fields = ['visit_no', 'completed_at']


class MedicalRecordSerializer(serializers.ModelSerializer):
    visit_no = serializers.CharField(source='visit.visit_no', read_only=True)
    pet_name = serializers.CharField(source='visit.pet.name', read_only=True)
    doctor_name = serializers.CharField(source='visit.doctor.name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_price = serializers.DecimalField(source='medicine.price', max_digits=10, decimal_places=2, read_only=True)
    medicine_spec = serializers.CharField(source='medicine.specification', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Prescription
        fields = '__all__'


class ChargeSerializer(serializers.ModelSerializer):
    visit_no = serializers.CharField(source='visit.visit_no', read_only=True)
    pet_name = serializers.CharField(source='visit.pet.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Charge
        fields = '__all__'
        read_only_fields = ['charge_no', 'total_amount', 'paid_at']


class InventoryLogSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    operation_display = serializers.CharField(source='get_operation_display', read_only=True)
    operator_name = serializers.CharField(source='operator.name', read_only=True)
    
    class Meta:
        model = InventoryLog
        fields = '__all__'
