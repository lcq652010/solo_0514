from rest_framework import serializers
from .models import Institution, Device, Rental, Calibration, DamageRecord, MaintenanceRecord, ReturnAcceptance, Settlement


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DeviceSerializer(serializers.ModelSerializer):
    device_type_display = serializers.CharField(source='get_device_type_display', read_only=True)
    use_department_display = serializers.CharField(source='get_use_department_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    calibration_days_remaining = serializers.SerializerMethodField()
    calibration_status = serializers.SerializerMethodField()
    can_be_rented = serializers.SerializerMethodField()
    utilization_rate_30d = serializers.SerializerMethodField()
    total_rental_days = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'next_calibration_date']

    def get_calibration_days_remaining(self, obj):
        return obj.get_calibration_days_remaining()

    def get_calibration_status(self, obj):
        return obj.get_calibration_status()

    def get_can_be_rented(self, obj):
        return obj.can_be_rented()

    def get_utilization_rate_30d(self, obj):
        return obj.get_utilization_rate(days=30)

    def get_total_rental_days(self, obj):
        return obj.get_total_rental_days()

    def get_total_revenue(self, obj):
        return obj.get_total_rental_revenue()


class DeviceSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'model', 'serial_number', 'status', 'device_type', 'use_department']


class DeviceFilterSerializer(serializers.Serializer):
    device_type = serializers.CharField(required=False, allow_blank=True)
    use_department = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    calibration_status = serializers.CharField(required=False, allow_blank=True)


class RentalSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    device_info = DeviceSimpleSerializer(source='device', read_only=True)
    institution_info = InstitutionSerializer(source='institution', read_only=True)
    rental_days_remaining = serializers.SerializerMethodField()
    rental_countdown_status = serializers.SerializerMethodField()
    parent_rental_no = serializers.CharField(source='parent_rental.rental_no', read_only=True)
    has_renewals = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['rental_no', 'estimated_days', 'estimated_total', 'created_at', 'updated_at']

    def get_rental_days_remaining(self, obj):
        return obj.get_rental_days_remaining()

    def get_rental_countdown_status(self, obj):
        return obj.get_rental_countdown_status()

    def get_has_renewals(self, obj):
        return obj.renewals.exists()


class RentalSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'rental_no', 'status', 'start_date', 'end_date', 'device']


class RentalFilterSerializer(serializers.Serializer):
    status = serializers.CharField(required=False, allow_blank=True)
    institution = serializers.IntegerField(required=False)
    device = serializers.IntegerField(required=False)
    countdown_status = serializers.CharField(required=False, allow_blank=True)
    start_date_from = serializers.DateField(required=False)
    start_date_to = serializers.DateField(required=False)
    end_date_from = serializers.DateField(required=False)
    end_date_to = serializers.DateField(required=False)


class CalibrationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    device_info = DeviceSimpleSerializer(source='device', read_only=True)

    class Meta:
        model = Calibration
        fields = '__all__'
        read_only_fields = ['created_at']


class DamageRecordSerializer(serializers.ModelSerializer):
    damage_type_display = serializers.CharField(source='get_damage_type_display', read_only=True)
    damage_level_display = serializers.CharField(source='get_damage_level_display', read_only=True)
    device_info = DeviceSimpleSerializer(source='device', read_only=True)
    rental_no = serializers.CharField(source='rental.rental_no', read_only=True)

    class Meta:
        model = DamageRecord
        fields = '__all__'
        read_only_fields = ['created_at']


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    maintenance_type_display = serializers.CharField(source='get_maintenance_type_display', read_only=True)
    device_info = DeviceSimpleSerializer(source='device', read_only=True)
    damage_record_info = DamageRecordSerializer(source='damage_record', read_only=True)

    class Meta:
        model = MaintenanceRecord
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'report_date', 'total_cost']


class ReturnAcceptanceSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    rental_info = RentalSimpleSerializer(source='rental', read_only=True)
    damage_record_info = DamageRecordSerializer(source='damage_record', read_only=True)
    maintenance_record_info = MaintenanceRecordSerializer(source='maintenance_record', read_only=True)

    class Meta:
        model = ReturnAcceptance
        fields = '__all__'
        read_only_fields = ['created_at']


class SettlementSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    rental_info = RentalSimpleSerializer(source='rental', read_only=True)

    class Meta:
        model = Settlement
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'total_amount']
