from rest_framework import serializers
from .models import (
    Exhibition,
    Booth,
    Company,
    Booking,
    ConstructionDemand,
    ProgressTracker,
    Payment,
    Builder,
    ConstructionConfirm,
    ProgressStepTemplate,
    ProgressStep,
)


class ExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = '__all__'


class BuilderSerializer(serializers.ModelSerializer):
    specialty_display = serializers.CharField(source='get_specialty_display', read_only=True)

    class Meta:
        model = Builder
        fields = '__all__'


class BoothSerializer(serializers.ModelSerializer):
    exhibition_name = serializers.CharField(source='exhibition.name', read_only=True)
    booth_type_display = serializers.CharField(source='get_booth_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    zone_display = serializers.CharField(source='get_zone_display', read_only=True)

    class Meta:
        model = Booth
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    booth_number = serializers.CharField(source='booth.booth_number', read_only=True)
    booth_zone = serializers.CharField(source='booth.zone', read_only=True)
    exhibition_name = serializers.CharField(source='booth.exhibition.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    booth_type = serializers.CharField(source='booth.booth_type', read_only=True)
    booth_area = serializers.DecimalField(source='booth.area', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['order_number', 'deposit_amount', 'balance_amount', 'total_amount']


class ConstructionConfirmSerializer(serializers.ModelSerializer):
    confirm_status_display = serializers.CharField(source='get_confirm_status_display', read_only=True)
    order_number = serializers.CharField(source='construction.booking.order_number', read_only=True)
    company_name = serializers.CharField(source='construction.booking.company.name', read_only=True)

    class Meta:
        model = ConstructionConfirm
        fields = '__all__'
        read_only_fields = ['confirm_number', 'created_at', 'confirmed_at']


class ConstructionDemandSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='booking.order_number', read_only=True)
    company_name = serializers.CharField(source='booking.company.name', read_only=True)
    booth_type = serializers.CharField(source='booking.booth.booth_type', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    builder_name = serializers.CharField(source='builder.name', read_only=True)
    builder_specialty = serializers.CharField(source='builder.get_specialty_display', read_only=True)
    confirms = ConstructionConfirmSerializer(many=True, read_only=True)

    class Meta:
        model = ConstructionDemand
        fields = '__all__'


class ProgressStepTemplateSerializer(serializers.ModelSerializer):
    step_type_display = serializers.CharField(source='get_step_type_display', read_only=True)

    class Meta:
        model = ProgressStepTemplate
        fields = '__all__'


class ProgressStepSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    order_number = serializers.CharField(source='construction.booking.order_number', read_only=True)

    class Meta:
        model = ProgressStep
        fields = '__all__'
        read_only_fields = ['reported_at', 'created_at']


class ProgressTrackerSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='construction.booking.order_number', read_only=True)

    class Meta:
        model = ProgressTracker
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='booking.order_number', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
